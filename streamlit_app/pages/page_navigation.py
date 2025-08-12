"""
Multi-Page Navigation System
Aligned with AI agent process steps with shared progress tracking
"""
import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ProcessStep(Enum):
    """Process steps aligned with AI agent workflow"""
    INPUT = "input"
    ANALYSIS = "analysis" 
    PROCESSING = "processing"
    REVIEW = "review"
    PROJECTS = "projects"


@dataclass
class PageConfig:
    """Configuration for each page in the process"""
    key: str
    title: str
    icon: str
    description: str
    step: ProcessStep
    requires_input: bool = False
    requires_analysis: bool = False
    requires_processing: bool = False


# Page configurations aligned with agent workflow
PAGE_CONFIGS = [
    PageConfig(
        key="input",
        title="Smart Input",
        icon="💭",
        description="Enter business content (transcripts, ideas, requirements)",
        step=ProcessStep.INPUT
    ),
    PageConfig(
        key="analysis", 
        title="Content Analysis",
        icon="🤖",
        description="AI analysis and routing recommendations",
        step=ProcessStep.ANALYSIS,
        requires_input=True
    ),
    PageConfig(
        key="processing",
        title="AI Processing",
        icon="⚡",
        description="Multi-agent pipeline execution (Conversa → Conny → ProDy → Marketing)",
        step=ProcessStep.PROCESSING,
        requires_input=True,
        requires_analysis=True
    ),
    PageConfig(
        key="review",
        title="Document Review",
        icon="📋",
        description="Review, edit, and finalize generated documents",
        step=ProcessStep.REVIEW,
        requires_input=True,
        requires_processing=True
    ),
    PageConfig(
        key="projects",
        title="Project Library",
        icon="📚",
        description="Manage saved projects and proposal history",
        step=ProcessStep.PROJECTS
    )
]


class PageNavigator:
    """Manages multi-page navigation with progress tracking"""
    
    def __init__(self):
        self.pages = {config.key: config for config in PAGE_CONFIGS}
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for page navigation"""
        if "current_page" not in st.session_state:
            st.session_state.current_page = "input"
        
        if "page_progress" not in st.session_state:
            st.session_state.page_progress = {
                "input": False,
                "analysis": False, 
                "processing": False,
                "review": False
            }
        
        if "current_project_id" not in st.session_state:
            st.session_state.current_project_id = None
    
    def render_sidebar_navigation(self):
        """Render sidebar with page navigation and progress"""
        
        st.sidebar.title("🤖 AI Proposal Pipeline")
        st.sidebar.markdown("*Multi-Agent Proposal Generation*")
        
        # Progress overview
        self._render_progress_overview()
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🗺️ Process Flow")
        
        # Page navigation buttons
        current_page = st.session_state.current_page
        
        for config in PAGE_CONFIGS:
            # Determine if page is accessible
            is_accessible = self._is_page_accessible(config)
            is_current = current_page == config.key
            is_completed = st.session_state.page_progress.get(config.key, False)
            
            # Button styling
            if is_current:
                button_type = "primary"
            elif is_completed:
                button_type = "secondary"
            else:
                button_type = "tertiary"
            
            # Status indicator
            if is_completed:
                status = "✅"
            elif is_current:
                status = "👉"
            elif is_accessible:
                status = "🔵"
            else:
                status = "⚪"
            
            # Navigation button
            button_text = f"{status} {config.icon} {config.title}"
            
            if is_accessible:
                if st.sidebar.button(
                    button_text,
                    key=f"nav_{config.key}",
                    type=button_type,
                    use_container_width=True,
                    disabled=False
                ):
                    st.session_state.current_page = config.key
                    st.rerun()
            else:
                st.sidebar.button(
                    button_text,
                    key=f"nav_{config.key}_disabled",
                    type="tertiary",
                    disabled=True,
                    use_container_width=True
                )
            
            # Show description for current or next accessible page
            if is_current or (not is_accessible and self._is_next_page(config.key)):
                st.sidebar.caption(f"└─ {config.description}")
        
        # Quick actions
        st.sidebar.markdown("---")
        self._render_quick_actions()
    
    def _render_progress_overview(self):
        """Render overall progress indicator"""
        
        completed_steps = sum(1 for step in st.session_state.page_progress.values() if step)
        total_steps = len(st.session_state.page_progress)
        progress_percent = (completed_steps / total_steps) * 100
        
        st.sidebar.subheader("📊 Overall Progress")
        st.sidebar.progress(progress_percent / 100)
        st.sidebar.caption(f"{completed_steps}/{total_steps} steps completed")
        
        # Current project info
        if st.session_state.get("current_project_id"):
            project_name = st.session_state.get("project_name", "Unnamed Project")
            st.sidebar.info(f"🎯 **Current Project**: {project_name}")
    
    def _render_quick_actions(self):
        """Render quick action buttons"""
        
        st.sidebar.subheader("🚀 Quick Actions")
        
        # Start new project
        if st.sidebar.button("🆕 New Project", use_container_width=True):
            self.start_new_project()
        
        # Continue where left off
        if st.session_state.get("page_progress", {}).get("input", False):
            if st.sidebar.button("▶️ Continue Process", use_container_width=True):
                next_page = self._get_next_incomplete_page()
                if next_page:
                    st.session_state.current_page = next_page
                    st.rerun()
        
        # Demo mode
        if st.sidebar.button("🎭 Demo Mode", use_container_width=True):
            self.load_demo_data()
    
    def _is_page_accessible(self, config: PageConfig) -> bool:
        """Check if a page is accessible based on requirements"""
        
        if config.key == "projects":  # Projects page is always accessible
            return True
        
        if config.requires_input and not st.session_state.get("smart_input"):
            return False
        
        if config.requires_analysis and not st.session_state.page_progress.get("analysis", False):
            return False
        
        if config.requires_processing and not st.session_state.page_progress.get("processing", False):
            return False
        
        return True
    
    def _is_next_page(self, page_key: str) -> bool:
        """Check if this is the next page user should visit"""
        
        # Get current progress
        progress = st.session_state.page_progress
        
        if page_key == "input" and not progress.get("input", False):
            return True
        elif page_key == "analysis" and progress.get("input", False) and not progress.get("analysis", False):
            return True
        elif page_key == "processing" and progress.get("analysis", False) and not progress.get("processing", False):
            return True
        elif page_key == "review" and progress.get("processing", False) and not progress.get("review", False):
            return True
        
        return False
    
    def _get_next_incomplete_page(self) -> Optional[str]:
        """Get the next incomplete page in sequence"""
        
        progress = st.session_state.page_progress
        
        for config in PAGE_CONFIGS[:-1]:  # Exclude projects page
            if not progress.get(config.key, False) and self._is_page_accessible(config):
                return config.key
        
        return None
    
    def get_current_page_config(self) -> PageConfig:
        """Get configuration for current page"""
        current_page = st.session_state.current_page
        return self.pages[current_page]
    
    def mark_page_completed(self, page_key: str):
        """Mark a page as completed"""
        st.session_state.page_progress[page_key] = True
    
    def start_new_project(self):
        """Start a new project - reset all state"""
        
        # Reset page progress
        st.session_state.page_progress = {
            "input": False,
            "analysis": False,
            "processing": False,
            "review": False
        }
        
        # Reset current data
        st.session_state.current_project_id = None
        st.session_state.smart_input = None
        st.session_state.analysis_results = None
        st.session_state.pipeline_results = None
        st.session_state.generated_documents = {}
        
        # Go to input page
        st.session_state.current_page = "input"
        st.success("🆕 Started new project!")
        st.rerun()
    
    def load_demo_data(self):
        """Load demo data for testing"""
        
        # Demo smart input
        st.session_state.smart_input = {
            "content": """Customer Discovery Call - Acme Manufacturing Corp

**Participants**: 
- Sarah Johnson (CTO, Acme Manufacturing)
- Mike Davis (VP Operations, Acme Manufacturing)  
- John Smith (Sales Rep, Our Company)

## Current Challenges
Sarah: "Our biggest pain point is managing our supply chain data. We have systems that don't talk to each other - our inventory management, production planning, and supplier portals are all separate. This creates a lot of manual work and delays."

Mike: "The lack of real-time visibility is killing us. When we have a production issue, it takes hours to figure out the ripple effect on our delivery commitments. We need something that gives us a unified view."

## Current Process  
Sarah: "Right now, our production team manually exports data from three different systems every morning and creates Excel reports. It takes about 2 hours each day. Then they email these reports to different departments."

Mike: "And by the time everyone gets the reports, the data is already outdated. We're making decisions on stale information."

## Desired Outcomes
Sarah: "We want real-time dashboards that show our entire supply chain status. Production capacity, inventory levels, supplier delivery status, all in one place."

Mike: "The goal is to reduce our production planning cycle from 24 hours to 2 hours, and eliminate the manual reporting completely."

## Budget & Timeline
Sarah: "We have budget approved for up to $500K for this project. We need to have something operational by Q2 2025 because that's when our new product line launches."

Mike: "The board is very focused on operational efficiency this year, so this project has executive support."

## Technical Requirements
Sarah: "We're using SAP for ERP, Oracle for inventory, and a custom supplier portal built in .NET. Everything needs to integrate with these existing systems."

Mike: "We also need mobile access for our floor managers. They need to see production status and make adjustments from the factory floor."

## Next Steps
John: "I'll prepare a detailed proposal showing how our AI-powered supply chain optimization platform can address these challenges. We'll include integration architecture, implementation timeline, and ROI projections."

Sarah: "Perfect. We'd like to see this by next Friday if possible. Also include some customer case studies from similar manufacturing companies."
            """,
            "format": "Customer Transcript",
            "customer_name": "Acme Manufacturing Corp",
            "content_type_hint": "Customer Transcript",
            "input_method": "demo",
            "timestamp": "2024-01-15T10:30:00"
        }
        
        # Mark input as completed
        self.mark_page_completed("input")
        
        # Load mock analysis results
        st.session_state.analysis_results = {
            "is_transcript": True,
            "content_type": "customer_transcript",
            "industry_hints": ["manufacturing", "technology"],
            "solution_indicators": ["integration", "analytics", "automation"],
            "urgency_level": "high",
            "budget_indicators": ["$500K"],
            "timeline_mentions": ["Q2 2025"],
            "agents_routing": {
                "conversa": True,
                "conny": True, 
                "prody": True,
                "marketing": True
            }
        }
        
        st.session_state.current_page = "analysis"
        st.success("🎭 Demo data loaded! Ready to explore the process.")
        st.balloons()
        st.rerun()


# Global navigator instance
_navigator = None

def get_page_navigator() -> PageNavigator:
    """Get singleton page navigator instance"""
    global _navigator
    if _navigator is None:
        _navigator = PageNavigator()
    return _navigator