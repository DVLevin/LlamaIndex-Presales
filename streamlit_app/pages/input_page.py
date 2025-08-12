"""
Input Page - Smart Business Input Collection
First step in the AI proposal generation process
"""
import streamlit as st
from datetime import datetime
from streamlit_app.components.smart_input import render_smart_input_section
from streamlit_app.pages.page_navigation import get_page_navigator
from streamlit_app.storage.project_manager import get_project_manager


def render_input_page():
    """Render the smart input collection page"""
    
    st.title("💭 Smart Business Input")
    st.markdown("""
    **Step 1**: Enter your business content to start the AI proposal generation process.
    
    The system accepts any type of business content:
    - Customer discovery transcripts
    - Strategic planning documents  
    - Competitive analysis notes
    - Solution requirements
    - Ideas and brainstorming content
    """)
    
    # Show current project info if exists
    if st.session_state.get("current_project_id"):
        project_name = st.session_state.get("project_name", "Current Project")
        st.info(f"🎯 **Working on**: {project_name}")
    
    st.markdown("---")
    
    # Smart input interface
    render_smart_input_section()
    
    # Progress and next steps
    render_input_progress_section()


def render_input_progress_section():
    """Render progress tracking and next step actions"""
    
    has_input = st.session_state.get("smart_input") is not None
    navigator = get_page_navigator()
    
    st.markdown("---")
    st.subheader("🚀 Ready to Process?")
    
    if has_input:
        # Show input summary
        smart_input = st.session_state["smart_input"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Content Length", f"{len(smart_input['content'].split()):,} words")
        with col2:
            st.metric("Input Type", smart_input.get("content_type_hint", "General"))
        with col3:
            st.metric("Customer/Project", smart_input.get("customer_name", "Unnamed"))
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save & Continue to Analysis", type="primary", use_container_width=True):
                save_current_input_as_project()
                navigator.mark_page_completed("input")
                st.session_state.current_page = "analysis"
                st.success("✅ Input saved! Moving to content analysis...")
                st.rerun()
        
        with col2:
            if st.button("🔍 Quick Preview Analysis", use_container_width=True):
                show_quick_analysis_preview()
        
        # Show preview if requested
        if st.session_state.get("show_quick_preview", False):
            render_quick_preview_section()
    
    else:
        st.warning("⚠️ Please enter business content above to continue to the next step.")
        
        # Template quick actions
        st.markdown("**Quick Start Options:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎧 Load Discovery Call Template", use_container_width=True):
                load_discovery_template()
        
        with col2:
            if st.button("📈 Load Strategic Initiative Template", use_container_width=True):
                load_strategy_template()
        
        with col3:
            if st.button("🎭 Load Demo Data", use_container_width=True):
                navigator.load_demo_data()


def save_current_input_as_project():
    """Save current input as a new project"""
    
    if not st.session_state.get("smart_input"):
        return
    
    smart_input = st.session_state["smart_input"]
    project_manager = get_project_manager()
    
    # Create project name
    customer_name = smart_input.get("customer_name", "Business Input")
    content_hint = smart_input.get("content_type_hint", "General")
    project_name = f"{customer_name} - {content_hint}"
    
    # Create project
    project_id = project_manager.create_project(
        name=project_name,
        customer_name=customer_name,
        input_content=smart_input["content"],
        input_metadata={
            "format": smart_input.get("format", "unknown"),
            "content_type_hint": content_hint,
            "input_method": smart_input.get("input_method", "manual"),
            "timestamp": smart_input.get("timestamp", datetime.now().isoformat())
        }
    )
    
    # Save to session state
    st.session_state.current_project_id = project_id
    st.session_state.project_name = project_name
    
    # Update project progress
    project_manager.update_project_progress(
        project_id=project_id,
        progress_step="analysis", 
        status="in_progress"
    )


def show_quick_analysis_preview():
    """Show quick analysis preview"""
    st.session_state.show_quick_preview = True


def render_quick_preview_section():
    """Render quick analysis preview section"""
    
    smart_input = st.session_state.get("smart_input")
    if not smart_input:
        return
    
    st.markdown("---")
    st.subheader("🔍 Quick Analysis Preview")
    st.markdown("*This gives you a preview of how the AI will analyze your content*")
    
    # Import the analysis preview from smart_input component
    from streamlit_app.components.smart_input import render_input_analysis_preview
    render_input_analysis_preview(smart_input["content"])
    
    # Hide preview button
    if st.button("Hide Preview"):
        st.session_state.show_quick_preview = False
        st.rerun()


def load_discovery_template():
    """Load customer discovery call template"""
    
    template_content = """# Customer Discovery Call - [Customer Name]
**Date**: {date}
**Participants**: [Names and roles]

## Current Challenges
Customer: "[Describe the main pain points and challenges they're facing]"

## Current Process/System
Customer: "[How they currently handle the process that needs improvement]"

## Desired Outcomes
Customer: "[What they want to achieve with a solution]"

## Budget & Timeline  
Customer: "[Budget range and timeline expectations]"

## Technical Requirements
Customer: "[Any specific technical needs or constraints]"

## Next Steps
[Agreed follow-up actions]
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    
    st.session_state["smart_input"] = {
        "content": template_content,
        "format": "Template",
        "customer_name": "Customer Discovery Call",
        "content_type_hint": "Customer Transcript",
        "input_method": "template",
        "timestamp": datetime.now().isoformat()
    }
    
    st.success("🎧 Discovery call template loaded! Edit as needed above.")
    st.rerun()


def load_strategy_template():
    """Load strategic initiative template"""
    
    template_content = """# Strategic Initiative - [Initiative Name]
**Date**: {date}
**Stakeholders**: [Key people involved]

## Business Context
[Why this initiative matters now]

## Problem Statement  
[Clear definition of what we're solving]

## Proposed Solution Approach
[High-level solution concept]

## Success Metrics
- [Metric 1]
- [Metric 2] 
- [Metric 3]

## Resource Requirements
- **Team Size**: [Number of people]
- **Timeline**: [Duration]
- **Budget**: [Investment required]

## Implementation Phases
1. **Phase 1**: [Description]
2. **Phase 2**: [Description]
3. **Phase 3**: [Description]
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    
    st.session_state["smart_input"] = {
        "content": template_content,
        "format": "Template", 
        "customer_name": "Strategic Initiative",
        "content_type_hint": "Strategic Planning",
        "input_method": "template",
        "timestamp": datetime.now().isoformat()
    }
    
    st.success("📈 Strategic initiative template loaded! Edit as needed above.")
    st.rerun()