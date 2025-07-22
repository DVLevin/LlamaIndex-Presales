"""
Pipeline Progress Component for Streamlit Application
Real-time progress tracking for AI agent pipeline
"""
import streamlit as st
from typing import Dict, List, Optional
import time
from datetime import datetime


def render_pipeline_progress():
    """Render real-time pipeline progress interface"""
    
    pipeline_state = st.session_state.get("pipeline_state", "idle")
    
    if pipeline_state == "idle":
        render_idle_state()
    elif pipeline_state == "processing":
        render_processing_state()
    elif pipeline_state == "completed":
        render_completed_state()
    elif pipeline_state == "error":
        render_error_state()


def render_idle_state():
    """Render pipeline in idle state"""
    
    st.info("🔵 Pipeline ready to start")
    
    # Show pipeline overview
    st.markdown("### 🔄 10-Step AI Pipeline Overview")
    
    pipeline_steps = get_pipeline_steps()
    
    for i, step in enumerate(pipeline_steps):
        st.markdown(f"{i+1}. **{step['agent']}**: {step['description']}")
    
    st.markdown("---")
    st.markdown("*Upload a transcript and configure your model to begin*")


def render_processing_state():
    """Render pipeline in processing state"""
    
    st.markdown("### 🚀 Pipeline Processing")
    
    # Progress bar
    progress = st.session_state.get("processing_progress", 0)
    progress_bar = st.progress(progress / 100)
    
    # Current step
    current_agent = st.session_state.get("current_agent", "Processing...")
    st.info(f"🤖 Current: {current_agent}")
    
    # Processing steps with status
    pipeline_steps = get_pipeline_steps()
    
    for i, step in enumerate(pipeline_steps):
        step_progress = min(100, max(0, progress - (i * 10)))
        
        if step_progress >= 100:
            st.success(f"✅ {step['agent']}: {step['description']}")
        elif step_progress > 0:
            st.warning(f"🟡 {step['agent']}: {step['description']} ({step_progress}%)")
        else:
            st.info(f"⏳ {step['agent']}: {step['description']}")
    
    # Processing time
    start_time = st.session_state.get("pipeline_start_time")
    if start_time:
        elapsed = time.time() - start_time
        st.text(f"⏱️ Processing time: {elapsed:.1f}s")
    
    # Auto-refresh for real-time updates
    time.sleep(1)
    st.rerun()


def render_completed_state():
    """Render pipeline completion state"""
    
    st.success("✅ Pipeline completed successfully!")
    
    # Processing summary
    processing_time = st.session_state.get("total_processing_time", "N/A")
    st.info(f"⏱️ Total processing time: {processing_time}")
    
    # Generated documents summary
    generated_docs = st.session_state.get("generated_documents", {})
    
    if generated_docs:
        st.markdown("### 📄 Generated Documents")
        
        doc_count = len(generated_docs)
        st.success(f"🎉 {doc_count} documents generated successfully!")
        
        # Document list
        for doc_type, doc_info in generated_docs.items():
            st.markdown(f"- **{doc_type}**: {doc_info.get('title', 'Untitled')}")
    
    # Next steps
    st.markdown("### 🎯 Next Steps")
    st.markdown("1. Review generated documents in the preview section")
    st.markdown("2. Download individual documents or complete package")
    st.markdown("3. Make any necessary edits or refinements")
    st.markdown("4. Share with stakeholders for review")
    
    # Reset option
    if st.button("🔄 Process Another Transcript"):
        reset_pipeline()


def render_error_state():
    """Render pipeline error state"""
    
    st.error("❌ Pipeline encountered an error")
    
    error_details = st.session_state.get("pipeline_error", {})
    
    if error_details:
        st.markdown("**Error Details:**")
        st.code(error_details.get("message", "Unknown error"))
        
        if error_details.get("step"):
            st.markdown(f"**Failed at:** {error_details['step']}")
        
        if error_details.get("timestamp"):
            st.markdown(f"**Time:** {error_details['timestamp']}")
    
    # Recovery options
    st.markdown("### 🔧 Recovery Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Retry Pipeline"):
            retry_pipeline()
    
    with col2:
        if st.button("🏠 Reset to Start"):
            reset_pipeline()
    
    with col3:
        if st.button("📋 Copy Error Details"):
            copy_error_details()


def get_pipeline_steps() -> List[Dict]:
    """Get pipeline step definitions"""
    
    return [
        {
            "agent": "Conversa",
            "description": "Analyze transcript and extract requirements",
            "expected_output": "Structured requirements analysis"
        },
        {
            "agent": "Conny", 
            "description": "Create project description from analysis",
            "expected_output": "Project description document"
        },
        {
            "agent": "Conversa",
            "description": "Enhance summary with additional context",
            "expected_output": "Enhanced summary v2"
        },
        {
            "agent": "Conny",
            "description": "Generate zero-knowledge brief for PM",
            "expected_output": "PM handover document"
        },
        {
            "agent": "ProDy",
            "description": "Generate problem overview document",
            "expected_output": "Problem overview (.md)"
        },
        {
            "agent": "ProDy",
            "description": "Generate process overview document", 
            "expected_output": "Process overview (.md)"
        },
        {
            "agent": "ProDy",
            "description": "Create process visualization diagrams",
            "expected_output": "Process visualization (.md + Mermaid)"
        },
        {
            "agent": "ProDy",
            "description": "Generate investment proposal",
            "expected_output": "Investment proposal (.md)"
        },
        {
            "agent": "ProDy",
            "description": "Create next steps document",
            "expected_output": "Next steps (.md)"
        },
        {
            "agent": "Marketing",
            "description": "Generate customer sales deck",
            "expected_output": "Sales presentation (.md)"
        }
    ]


def update_pipeline_progress(step: int, agent: str, message: str = ""):
    """Update pipeline progress state"""
    
    st.session_state["processing_progress"] = step * 10
    st.session_state["current_agent"] = f"{agent} - {message}" if message else agent
    
    # Log progress
    if "pipeline_log" not in st.session_state:
        st.session_state["pipeline_log"] = []
    
    st.session_state["pipeline_log"].append({
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "agent": agent,
        "message": message
    })


def reset_pipeline():
    """Reset pipeline to initial state"""
    
    st.session_state["pipeline_state"] = "idle"
    st.session_state["processing_progress"] = 0
    st.session_state["current_agent"] = ""
    st.session_state["generated_documents"] = {}
    st.session_state["pipeline_error"] = {}
    st.session_state["pipeline_log"] = []
    
    st.success("Pipeline reset successfully!")
    st.rerun()


def retry_pipeline():
    """Retry pipeline from last successful step"""
    
    st.session_state["pipeline_state"] = "processing"
    st.session_state["pipeline_error"] = {}
    
    st.info("Retrying pipeline...")
    st.rerun()


def copy_error_details():
    """Copy error details to clipboard"""
    
    error_details = st.session_state.get("pipeline_error", {})
    
    if error_details:
        error_text = f"""
Pipeline Error Details:
- Message: {error_details.get('message', 'Unknown')}
- Step: {error_details.get('step', 'Unknown')}
- Time: {error_details.get('timestamp', 'Unknown')}
- Model: {st.session_state.get('selected_model', {}).get('name', 'Unknown')}
        """.strip()
        
        # Note: Actual clipboard copy requires JavaScript/browser API
        st.code(error_text)
        st.info("Error details displayed above - please copy manually")
    else:
        st.warning("No error details available")