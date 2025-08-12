"""
Projects Page - Project Library & History Management
Browse, search, and manage saved proposal projects and artifacts
"""
import streamlit as st
from datetime import datetime, timedelta
from streamlit_app.storage.project_manager import get_project_manager
from streamlit_app.pages.page_navigation import get_page_navigator


def render_projects_page():
    """Render the project library and management page"""
    
    st.title("📚 Project Library")
    st.markdown("""
    **Project Management Hub**: Browse your proposal history, search past projects, and manage saved artifacts.
    
    Every AI-generated proposal is automatically saved as a searchable project with version history.
    """)
    
    project_manager = get_project_manager()
    
    # Project overview stats
    render_project_overview_stats()
    
    st.markdown("---")
    
    # Search and filter controls
    search_term, status_filter = render_search_and_filters()
    
    # Project list or search results
    render_project_list(search_term, status_filter)
    
    # Project details modal (if project selected)
    render_project_details()


def render_project_overview_stats():
    """Render project overview statistics"""
    
    st.subheader("📊 Project Overview")
    
    project_manager = get_project_manager()
    
    # Get project counts by status
    all_projects = project_manager.list_projects(limit=1000)  # Get all for stats
    
    total_projects = len(all_projects)
    completed_projects = len([p for p in all_projects if p["status"] == "completed"])
    in_progress_projects = len([p for p in all_projects if p["status"] == "in_progress"])
    draft_projects = len([p for p in all_projects if p["status"] == "draft"])
    
    # Total artifacts count
    total_artifacts = sum(p.get("artifact_count", 0) for p in all_projects)
    
    # Recent activity (last 7 days)
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    recent_projects = len([p for p in all_projects if p["updated_at"] > week_ago])
    
    # Display metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Projects", total_projects)
    
    with col2:
        st.metric("Completed", completed_projects)
    
    with col3:
        st.metric("In Progress", in_progress_projects)
    
    with col4:
        st.metric("Total Documents", total_artifacts)
    
    with col5:
        st.metric("Recent Activity", f"{recent_projects} this week")
    
    # Quick stats visualization
    if total_projects > 0:
        status_data = {
            "Completed": completed_projects,
            "In Progress": in_progress_projects,
            "Draft": draft_projects
        }
        
        # Simple progress visualization
        completion_rate = (completed_projects / total_projects) * 100 if total_projects > 0 else 0
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.progress(completion_rate / 100)
            st.caption(f"Project Completion Rate: {completion_rate:.1f}%")
        
        with col2:
            if recent_projects > 0:
                st.success(f"🚀 Active ({recent_projects} recent)")
            else:
                st.info("📊 All projects current")


def render_search_and_filters():
    """Render search and filter controls"""
    
    st.subheader("🔍 Find Projects")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "Search projects and documents",
            placeholder="Enter customer name, keywords, or document content...",
            help="Search across project names, customer names, and document content"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All", "completed", "in_progress", "draft"],
            format_func=lambda x: x.title() if x != "All" else "All Projects"
        )
    
    with col3:
        sort_order = st.selectbox(
            "Sort by",
            options=["recent", "name", "customer", "status"],
            format_func=lambda x: {
                "recent": "Most Recent",
                "name": "Project Name", 
                "customer": "Customer Name",
                "status": "Status"
            }[x]
        )
    
    # Quick filter buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🆕 Recent Projects", use_container_width=True):
            st.session_state["projects_filter"] = "recent"
    
    with col2:
        if st.button("✅ Completed Only", use_container_width=True):
            st.session_state["projects_filter"] = "completed"
    
    with col3:
        if st.button("⚡ In Progress", use_container_width=True):
            st.session_state["projects_filter"] = "in_progress"
    
    with col4:
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.session_state["projects_filter"] = None
            st.rerun()
    
    return search_term, status_filter


def render_project_list(search_term, status_filter):
    """Render list of projects based on search/filter criteria"""
    
    st.subheader("📋 Projects")
    
    project_manager = get_project_manager()
    
    # Apply filters and search
    if search_term:
        projects = project_manager.search_projects(search_term)
        if projects:
            st.info(f"🔍 Found {len(projects)} projects matching '{search_term}'")
        else:
            st.warning(f"No projects found matching '{search_term}'")
            return
    else:
        # Apply status filter
        filter_status = None if status_filter == "All" else status_filter
        projects = project_manager.list_projects(status_filter=filter_status)
    
    if not projects:
        render_no_projects_message()
        return
    
    # Display projects
    for project in projects:
        render_project_card(project)


def render_no_projects_message():
    """Render message when no projects found"""
    
    st.info("📂 **No projects found**")
    
    st.markdown("**Get started:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🆕 Create New Project", type="primary", use_container_width=True):
            navigator = get_page_navigator()
            navigator.start_new_project()
    
    with col2:
        if st.button("🎭 Load Demo Project", use_container_width=True):
            create_demo_project()


def render_project_card(project):
    """Render individual project card"""
    
    project_id = project["id"]
    
    # Project card container
    with st.container():
        # Header row
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            # Project title and customer
            st.markdown(f"### 📄 {project['name']}")
            st.markdown(f"**Customer**: {project['customer_name']}")
        
        with col2:
            # Status badge
            status = project["status"]
            status_colors = {
                "completed": "success",
                "in_progress": "info", 
                "draft": "warning"
            }
            status_icons = {
                "completed": "✅",
                "in_progress": "⚡",
                "draft": "📝"
            }
            
            if status == "completed":
                st.success(f"{status_icons[status]} {status.title()}")
            elif status == "in_progress":
                st.info(f"{status_icons[status]} {status.replace('_', ' ').title()}")
            else:
                st.warning(f"{status_icons[status]} {status.title()}")
        
        with col3:
            # Action buttons
            if st.button("👁️ View", key=f"view_{project_id}"):
                st.session_state["selected_project_id"] = project_id
                st.rerun()
        
        # Details row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Documents", project.get("artifact_count", 0))
        
        with col2:
            progress_step = project.get("progress_step", "input")
            st.metric("Stage", progress_step.title())
        
        with col3:
            created_date = datetime.fromisoformat(project["created_at"]).strftime("%Y-%m-%d")
            st.metric("Created", created_date)
        
        with col4:
            # Time ago calculation
            updated_dt = datetime.fromisoformat(project["updated_at"])
            time_ago = get_time_ago(updated_dt)
            st.metric("Updated", time_ago)
        
        # Quick actions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✏️ Resume", key=f"resume_{project_id}", use_container_width=True):
                resume_project(project_id)
        
        with col2:
            if st.button("📦 Export", key=f"export_{project_id}", use_container_width=True):
                export_project(project_id, project["name"])
        
        with col3:
            if st.button("📋 Copy", key=f"copy_{project_id}", use_container_width=True):
                copy_project(project_id)
        
        with col4:
            if st.button("🗑️ Delete", key=f"delete_{project_id}", use_container_width=True):
                delete_project(project_id, project["name"])
        
        # Show match context if search result
        if project.get("match_type") == "artifact":
            st.caption(f"🔍 **Match found in**: {project.get('matched_artifact', 'document')}")
        
        st.markdown("---")


def render_project_details():
    """Render detailed project view modal"""
    
    selected_project_id = st.session_state.get("selected_project_id")
    if not selected_project_id:
        return
    
    project_manager = get_project_manager()
    project = project_manager.get_project(selected_project_id)
    
    if not project:
        st.error("Project not found.")
        st.session_state["selected_project_id"] = None
        return
    
    # Project details modal
    st.markdown("---")
    st.markdown(f"## 📄 Project Details: {project.name}")
    
    # Close button
    if st.button("❌ Close Details"):
        st.session_state["selected_project_id"] = None
        st.rerun()
    
    # Project metadata
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Project Information")
        st.markdown(f"**Customer**: {project.customer_name}")
        st.markdown(f"**Status**: {project.status.title()}")
        st.markdown(f"**Progress Step**: {project.progress_step.title()}")
        st.markdown(f"**Created**: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
        st.markdown(f"**Last Updated**: {project.updated_at.strftime('%Y-%m-%d %H:%M')}")
    
    with col2:
        st.markdown("### 🤖 AI Processing")
        agents_completed = project.agents_completed or []
        if agents_completed:
            st.markdown("**Completed Agents**:")
            for agent in agents_completed:
                st.markdown(f"- ✅ {agent.title()}")
        else:
            st.markdown("*No agents completed yet*")
    
    # Original input
    st.markdown("### 💭 Original Input")
    with st.expander("📖 View Original Input", expanded=False):
        st.text_area(
            "Original Business Input",
            value=project.input_content,
            height=200,
            disabled=True
        )
    
    # Artifacts
    st.markdown("### 📋 Generated Documents")
    
    if project.artifacts:
        for artifact in project.artifacts:
            with st.expander(f"📄 {artifact.title} (v{artifact.version})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Type**: {artifact.artifact_type}")
                    st.markdown(f"**Format**: {artifact.format}")
                    st.markdown(f"**Generated by**: {artifact.agent_generated or 'Unknown'}")
                    st.markdown(f"**Created**: {artifact.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.markdown(f"**Updated**: {artifact.updated_at.strftime('%Y-%m-%d %H:%M')}")
                
                with col2:
                    word_count = len(artifact.content.split())
                    st.metric("Word Count", f"{word_count:,}")
                
                # Content preview
                preview = artifact.content[:300]
                if len(artifact.content) > 300:
                    preview += "..."
                st.text_area(
                    "Content Preview",
                    value=preview,
                    height=100,
                    disabled=True,
                    key=f"preview_{artifact.id}"
                )
                
                # Actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📄 Download",
                        data=artifact.content,
                        file_name=f"{artifact.title}.{artifact.format}",
                        mime="text/markdown" if artifact.format == "markdown" else "text/plain",
                        key=f"download_{artifact.id}"
                    )
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{artifact.id}"):
                        edit_artifact(project.id, artifact)
                
                with col3:
                    if st.button("📋 View Full", key=f"view_{artifact.id}"):
                        view_full_artifact(artifact)
    
    else:
        st.info("No documents generated yet.")
    
    # Project actions
    st.markdown("### 🔧 Project Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✏️ Resume Project", type="primary", use_container_width=True):
            resume_project(project.id)
    
    with col2:
        if st.button("📦 Export Project", use_container_width=True):
            export_project(project.id, project.name)
    
    with col3:
        if st.button("📋 Duplicate Project", use_container_width=True):
            copy_project(project.id)
    
    with col4:
        if st.button("🗑️ Delete Project", use_container_width=True):
            delete_project(project.id, project.name)


def resume_project(project_id):
    """Resume working on a project"""
    
    project_manager = get_project_manager()
    project = project_manager.get_project(project_id)
    
    if not project:
        st.error("Project not found.")
        return
    
    # Load project into session state
    st.session_state.current_project_id = project_id
    st.session_state.project_name = project.name
    
    # Restore input
    st.session_state.smart_input = {
        "content": project.input_content,
        "customer_name": project.customer_name,
        **project.input_metadata
    }
    
    # Restore progress state
    progress_mapping = {
        "input": {"input": True},
        "analysis": {"input": True, "analysis": True},
        "processing": {"input": True, "analysis": True, "processing": True},
        "review": {"input": True, "analysis": True, "processing": True, "review": True},
        "completed": {"input": True, "analysis": True, "processing": True, "review": True}
    }
    
    st.session_state.page_progress = progress_mapping.get(project.progress_step, {"input": True})
    
    # Determine which page to go to
    if project.progress_step == "completed" or project.artifacts:
        st.session_state.current_page = "review"
    elif project.progress_step == "processing":
        st.session_state.current_page = "processing"
    elif project.progress_step == "analysis":
        st.session_state.current_page = "analysis"
    else:
        st.session_state.current_page = "input"
    
    st.success(f"✅ Resumed project: {project.name}")
    st.rerun()


def export_project(project_id, project_name):
    """Export project as ZIP"""
    
    project_manager = get_project_manager()
    zip_data = project_manager.export_project_to_zip(project_id)
    
    if zip_data:
        filename = f"{project_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.zip"
        
        st.download_button(
            label="📦 Download Project ZIP",
            data=zip_data,
            file_name=filename,
            mime="application/zip",
            key=f"export_download_{project_id}"
        )
        
        st.success("✅ Project package ready for download!")


def copy_project(project_id):
    """Create a copy of the project"""
    
    project_manager = get_project_manager()
    original_project = project_manager.get_project(project_id)
    
    if not original_project:
        st.error("Project not found.")
        return
    
    # Create new project
    new_name = f"{original_project.name} (Copy)"
    new_project_id = project_manager.create_project(
        name=new_name,
        customer_name=original_project.customer_name,
        input_content=original_project.input_content,
        input_metadata=original_project.input_metadata
    )
    
    # Copy artifacts
    for artifact in original_project.artifacts:
        project_manager.save_artifact(
            project_id=new_project_id,
            artifact_type=artifact.artifact_type,
            title=artifact.title,
            content=artifact.content,
            format=artifact.format,
            agent_generated=f"copied_from_{artifact.agent_generated}"
        )
    
    st.success(f"✅ Created copy: {new_name}")
    st.rerun()


def delete_project(project_id, project_name):
    """Delete a project with confirmation"""
    
    # Confirmation check
    confirm_key = f"delete_confirm_{project_id}"
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False
    
    if not st.session_state[confirm_key]:
        st.warning(f"⚠️ **Confirm deletion** of '{project_name}'?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes, Delete", key=f"confirm_delete_{project_id}"):
                st.session_state[confirm_key] = True
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", key=f"cancel_delete_{project_id}"):
                pass
    
    else:
        # Perform deletion
        project_manager = get_project_manager()
        success = project_manager.delete_project(project_id)
        
        if success:
            st.success(f"✅ Deleted project: {project_name}")
            # Clear confirmation state
            del st.session_state[confirm_key]
            st.rerun()
        else:
            st.error("❌ Failed to delete project.")


def edit_artifact(project_id, artifact):
    """Edit an artifact (redirect to review page)"""
    
    # Load project and go to review page
    st.session_state.current_project_id = project_id
    st.session_state.selected_document = artifact.artifact_type
    st.session_state.current_page = "review"
    
    st.info(f"✏️ Opening '{artifact.title}' for editing...")
    st.rerun()


def view_full_artifact(artifact):
    """View full artifact content"""
    
    st.markdown("---")
    st.markdown(f"## 📄 {artifact.title}")
    
    if st.button("❌ Close"):
        st.rerun()
    
    # Render content based on format
    if artifact.format == "markdown":
        st.markdown(artifact.content)
    else:
        st.text(artifact.content)
    
    # Download option
    st.download_button(
        "📄 Download Document",
        data=artifact.content,
        file_name=f"{artifact.title}.{artifact.format}",
        mime="text/markdown" if artifact.format == "markdown" else "text/plain"
    )


def create_demo_project():
    """Create a demo project for testing"""
    
    navigator = get_page_navigator()
    navigator.load_demo_data()
    
    # Create demo project
    project_manager = get_project_manager()
    
    demo_project_id = project_manager.create_project(
        name="Demo Manufacturing Project",
        customer_name="Acme Manufacturing Corp",
        input_content=st.session_state["smart_input"]["content"],
        input_metadata=st.session_state["smart_input"]
    )
    
    # Add demo artifacts
    demo_artifacts = {
        "problem_overview": "# Problem Overview\n\nAcme Manufacturing faces integration challenges...",
        "solution_architecture": "# Solution Architecture\n\nRecommended cloud-based integration platform...", 
        "investment_proposal": "# Investment Proposal\n\n$500K investment for 12-month implementation...",
        "sales_deck": "# Executive Summary\n\nTransform manufacturing operations with AI..."
    }
    
    for artifact_type, content in demo_artifacts.items():
        project_manager.save_artifact(
            project_id=demo_project_id,
            artifact_type=artifact_type,
            title=artifact_type.replace("_", " ").title(),
            content=content,
            format="markdown",
            agent_generated="demo"
        )
    
    project_manager.update_project_progress(
        project_id=demo_project_id,
        progress_step="completed",
        status="completed"
    )
    
    st.success("🎭 Demo project created!")
    st.rerun()


def get_time_ago(dt):
    """Get human-readable time ago string"""
    
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "Just now"