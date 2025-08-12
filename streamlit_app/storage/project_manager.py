"""
Project Manager - Persistent Storage for AI-Generated Proposals
Saves all AI outputs as structured projects with searchable artifacts
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectArtifact:
    """Individual document artifact within a project"""
    id: str
    project_id: str
    artifact_type: str  # "problem_overview", "process_overview", "investment_proposal", etc.
    title: str
    content: str
    format: str  # "markdown", "mermaid", "json"
    agent_generated: str  # Which agent created it
    created_at: datetime
    updated_at: datetime
    version: int


@dataclass 
class Project:
    """Complete proposal project container"""
    id: str
    name: str
    customer_name: str
    status: str  # "in_progress", "completed", "draft"
    input_content: str
    input_metadata: Dict[str, Any]
    progress_step: str  # Current process step
    agents_completed: List[str]
    created_at: datetime
    updated_at: datetime
    artifacts: List[ProjectArtifact]


class ProjectManager:
    """Manages persistent storage of AI-generated projects and artifacts"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            storage_dir = Path(__file__).parent
            storage_dir.mkdir(exist_ok=True)
            db_path = storage_dir / "projects.db"
        
        self.db_path = str(db_path)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Projects table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    status TEXT DEFAULT 'draft',
                    input_content TEXT,
                    input_metadata TEXT,  -- JSON
                    progress_step TEXT DEFAULT 'input',
                    agents_completed TEXT DEFAULT '[]',  -- JSON array
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Artifacts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    artifact_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    format TEXT DEFAULT 'markdown',
                    agent_generated TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                )
            """)
            
            # Search index for full-text search
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS artifacts_fts USING fts5(
                    artifact_id,
                    title,
                    content,
                    content='artifacts',
                    content_rowid='rowid'
                )
            """)
            
            conn.commit()
    
    def create_project(self, name: str, customer_name: str, input_content: str, 
                      input_metadata: Dict[str, Any] = None) -> str:
        """Create a new project and return its ID"""
        
        project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(name) % 10000:04d}"
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO projects 
                (id, name, customer_name, input_content, input_metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id, name, customer_name, input_content,
                json.dumps(input_metadata or {}), now, now
            ))
            conn.commit()
        
        return project_id
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a complete project with all artifacts"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Get project data
            project_row = conn.execute("""
                SELECT id, name, customer_name, status, input_content, input_metadata,
                       progress_step, agents_completed, created_at, updated_at
                FROM projects WHERE id = ?
            """, (project_id,)).fetchone()
            
            if not project_row:
                return None
            
            # Get artifacts
            artifact_rows = conn.execute("""
                SELECT id, project_id, artifact_type, title, content, format,
                       agent_generated, created_at, updated_at, version
                FROM artifacts WHERE project_id = ? 
                ORDER BY created_at ASC
            """, (project_id,)).fetchall()
            
            # Build project object
            artifacts = []
            for row in artifact_rows:
                artifacts.append(ProjectArtifact(
                    id=row[0], project_id=row[1], artifact_type=row[2],
                    title=row[3], content=row[4], format=row[5],
                    agent_generated=row[6], 
                    created_at=datetime.fromisoformat(row[7]),
                    updated_at=datetime.fromisoformat(row[8]),
                    version=row[9]
                ))
            
            return Project(
                id=project_row[0], name=project_row[1], customer_name=project_row[2],
                status=project_row[3], input_content=project_row[4],
                input_metadata=json.loads(project_row[5] or '{}'),
                progress_step=project_row[6], 
                agents_completed=json.loads(project_row[7] or '[]'),
                created_at=datetime.fromisoformat(project_row[8]),
                updated_at=datetime.fromisoformat(project_row[9]),
                artifacts=artifacts
            )
    
    def update_project_progress(self, project_id: str, progress_step: str, 
                               agents_completed: List[str] = None, status: str = None):
        """Update project progress tracking"""
        
        updates = ["updated_at = ?", "progress_step = ?"]
        params = [datetime.now().isoformat(), progress_step]
        
        if agents_completed is not None:
            updates.append("agents_completed = ?")
            params.append(json.dumps(agents_completed))
        
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        
        params.append(project_id)  # For WHERE clause
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"""
                UPDATE projects SET {', '.join(updates)}
                WHERE id = ?
            """, params)
            conn.commit()
    
    def save_artifact(self, project_id: str, artifact_type: str, title: str,
                     content: str, format: str = "markdown", 
                     agent_generated: str = None) -> str:
        """Save or update a project artifact"""
        
        # Check if artifact already exists
        with sqlite3.connect(self.db_path) as conn:
            existing = conn.execute("""
                SELECT id, version FROM artifacts 
                WHERE project_id = ? AND artifact_type = ?
            """, (project_id, artifact_type)).fetchone()
            
            now = datetime.now().isoformat()
            
            if existing:
                # Update existing artifact
                artifact_id, current_version = existing
                new_version = current_version + 1
                
                conn.execute("""
                    UPDATE artifacts SET 
                    title = ?, content = ?, format = ?, agent_generated = ?,
                    updated_at = ?, version = ?
                    WHERE id = ?
                """, (title, content, format, agent_generated, now, new_version, artifact_id))
                
            else:
                # Create new artifact
                artifact_id = f"art_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(title) % 1000:03d}"
                
                conn.execute("""
                    INSERT INTO artifacts 
                    (id, project_id, artifact_type, title, content, format, 
                     agent_generated, created_at, updated_at, version)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (artifact_id, project_id, artifact_type, title, content, 
                      format, agent_generated, now, now))
            
            # Update search index
            conn.execute("""
                INSERT OR REPLACE INTO artifacts_fts (artifact_id, title, content)
                VALUES (?, ?, ?)
            """, (artifact_id, title, content))
            
            conn.commit()
        
        return artifact_id
    
    def list_projects(self, status_filter: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """List all projects with summary information"""
        
        query = """
            SELECT p.id, p.name, p.customer_name, p.status, p.progress_step,
                   p.created_at, p.updated_at, COUNT(a.id) as artifact_count
            FROM projects p
            LEFT JOIN artifacts a ON p.id = a.project_id
        """
        params = []
        
        if status_filter:
            query += " WHERE p.status = ?"
            params.append(status_filter)
        
        query += " GROUP BY p.id ORDER BY p.updated_at DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
            
            return [
                {
                    "id": row[0], "name": row[1], "customer_name": row[2],
                    "status": row[3], "progress_step": row[4],
                    "created_at": row[5], "updated_at": row[6],
                    "artifact_count": row[7]
                }
                for row in rows
            ]
    
    def search_projects(self, search_term: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search projects and artifacts by content"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Search in project names and customer names
            project_results = conn.execute("""
                SELECT DISTINCT p.id, p.name, p.customer_name, p.status, p.progress_step,
                       p.created_at, p.updated_at
                FROM projects p
                WHERE p.name LIKE ? OR p.customer_name LIKE ? OR p.input_content LIKE ?
                ORDER BY p.updated_at DESC
                LIMIT ?
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", limit)).fetchall()
            
            # Search in artifacts using FTS
            artifact_results = conn.execute("""
                SELECT DISTINCT p.id, p.name, p.customer_name, p.status, p.progress_step,
                       p.created_at, p.updated_at, a.title, a.artifact_type
                FROM artifacts_fts fts
                JOIN artifacts a ON fts.artifact_id = a.id
                JOIN projects p ON a.project_id = p.id
                WHERE artifacts_fts MATCH ?
                ORDER BY p.updated_at DESC
                LIMIT ?
            """, (search_term, limit)).fetchall()
            
            # Combine and deduplicate results
            all_results = {}
            for row in project_results:
                all_results[row[0]] = {
                    "id": row[0], "name": row[1], "customer_name": row[2],
                    "status": row[3], "progress_step": row[4],
                    "created_at": row[5], "updated_at": row[6],
                    "match_type": "project"
                }
            
            for row in artifact_results:
                if row[0] not in all_results:
                    all_results[row[0]] = {
                        "id": row[0], "name": row[1], "customer_name": row[2],
                        "status": row[3], "progress_step": row[4],
                        "created_at": row[5], "updated_at": row[6],
                        "match_type": "artifact",
                        "matched_artifact": f"{row[7]} ({row[8]})"
                    }
            
            return list(all_results.values())[:limit]
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project and all its artifacts"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Delete artifacts first (due to foreign key)
            conn.execute("DELETE FROM artifacts WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM artifacts_fts WHERE artifact_id IN "
                        "(SELECT id FROM artifacts WHERE project_id = ?)", (project_id,))
            
            # Delete project
            result = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            
            return result.rowcount > 0
    
    def export_project_to_zip(self, project_id: str) -> bytes:
        """Export complete project as ZIP file"""
        
        import io
        import zipfile
        
        project = self.get_project(project_id)
        if not project:
            return None
        
        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add project metadata
            zip_file.writestr("project_info.json", json.dumps({
                "id": project.id,
                "name": project.name,
                "customer_name": project.customer_name,
                "status": project.status,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
                "agents_completed": project.agents_completed,
                "progress_step": project.progress_step
            }, indent=2))
            
            # Add original input
            zip_file.writestr("original_input.txt", project.input_content)
            
            # Add all artifacts
            for artifact in project.artifacts:
                filename = f"{artifact.artifact_type}_{artifact.title.replace(' ', '_')}.{artifact.format}"
                zip_file.writestr(f"artifacts/{filename}", artifact.content)
        
        return zip_buffer.getvalue()


# Global project manager instance
_project_manager = None

def get_project_manager() -> ProjectManager:
    """Get singleton project manager instance"""
    global _project_manager
    if _project_manager is None:
        _project_manager = ProjectManager()
    return _project_manager