"""
LlamaIndex Pre-sales Pipeline - Streamlit Main Application
Transform customer transcripts into comprehensive proposal packages
"""
import streamlit as st
import os
import sys
from typing import Optional, Dict, Any
import asyncio
import json
from datetime import datetime

# Add project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from streamlit_app.config import load_config, save_api_keys, validate_api_keys, initialize_session_state
from streamlit_app.components.file_upload import render_file_upload_section
from streamlit_app.components.model_selection import render_model_selection
from streamlit_app.components.pipeline_progress import render_pipeline_progress
from streamlit_app.components.document_preview import render_document_preview
from streamlit_app.components.overview_visualization import render_overview_section
from streamlit_app.components.prompt_management import render_prompt_management_section


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="LlamaIndex Pre-sales Pipeline",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Load configuration
    config = load_config()
    
    # Sidebar configuration
    render_sidebar_configuration(config)
    
    # Main navigation tabs
    overview_tab, input_tab, config_tab, progress_tab = st.tabs([
        "🏠 Overview", "📁 Input & Config", "⚙️ Prompts & Templates", "📊 Progress & Output"
    ])
    
    with overview_tab:
        render_overview_section()
    
    with input_tab:
        # Input and configuration section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📁 Upload Files")
            render_file_upload_section()
        
        with col2:
            st.subheader("🤖 Model Configuration")
            render_model_selection(config)
            
            st.subheader("🚀 Pipeline Controls")
            render_pipeline_controls()
    
    with config_tab:
        render_prompt_management_section()
    
    with progress_tab:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Pipeline Progress")
            render_pipeline_progress()
        
        with col2:
            st.subheader("📄 Document Preview")
            render_document_preview()


def render_sidebar_configuration(config):
    """Render sidebar with API configuration"""
    
    st.sidebar.title("⚙️ Configuration")
    
    # API Keys section
    st.sidebar.subheader("🔑 API Keys")
    
    # Check current API key status
    api_status = validate_api_keys(config)
    
    with st.sidebar.expander("Configure API Keys", expanded=not all(api_status.values())):
        
        # OpenRouter API Key
        openrouter_status = "✅" if api_status["openrouter"] else "❌"
        st.markdown(f"**OpenRouter** {openrouter_status}")
        openrouter_key = st.text_input(
            "OpenRouter API Key",
            value=config.openrouter_api_key if config.openrouter_api_key else "",
            type="password",
            placeholder="sk-or-v1-...",
            help="Required for LLM access"
        )
        
        # Jina API Key  
        jina_status = "✅" if api_status["jina"] else "❌"
        st.markdown(f"**Jina AI** {jina_status}")
        jina_key = st.text_input(
            "Jina AI API Key", 
            value=config.jina_api_key if config.jina_api_key else "",
            type="password",
            placeholder="jina_...",
            help="Required for embeddings and reranking"
        )
        
        # Save button
        if st.button("💾 Save API Keys"):
            save_api_keys(openrouter_key, jina_key)
            st.success("API keys saved successfully!")
            st.rerun()
    
    # Pipeline configuration
    st.sidebar.subheader("🔧 Pipeline Settings")
    
    # Agent configuration
    with st.sidebar.expander("Agent Configuration"):
        st.markdown("**Available Agents:**")
        st.markdown("- 🎯 **Conversa**: Transcript Analysis")
        st.markdown("- 🏗️ **Conny**: Business Consulting") 
        st.markdown("- 📋 **ProDy**: Document Generation")
        st.markdown("- 🎨 **Marketing**: Sales Deck Creation")
        
        enable_advanced_mode = st.checkbox("Enable Advanced Configuration", value=False)
        
        if enable_advanced_mode:
            st.info("Advanced agent prompt configuration - Coming soon!")
    
    # System status
    st.sidebar.subheader("📊 System Status")
    
    # API key validation status
    if all(api_status.values()):
        st.sidebar.success("🟢 All APIs configured")
    else:
        missing_keys = [key for key, status in api_status.items() if not status]
        st.sidebar.error(f"🔴 Missing: {', '.join(missing_keys)}")
    
    # Pipeline status
    pipeline_state = st.session_state.get("pipeline_state", "idle")
    status_colors = {
        "idle": "🔵 Ready",
        "processing": "🟡 Processing", 
        "completed": "🟢 Completed",
        "error": "🔴 Error"
    }
    st.sidebar.info(f"Pipeline: {status_colors.get(pipeline_state, '⚪ Unknown')}")


def render_pipeline_controls():
    """Render pipeline execution controls"""
    
    st.subheader("🚀 Pipeline Execution")
    
    config = load_config()
    api_status = validate_api_keys(config)
    
    # Check if ready to run
    ready_to_run = (
        all(api_status.values()) and 
        st.session_state.get("current_transcript") is not None
    )
    
    if not ready_to_run:
        missing_items = []
        if not all(api_status.values()):
            missing_items.append("API keys")
        if not st.session_state.get("current_transcript"):
            missing_items.append("transcript file")
            
        st.warning(f"⚠️ Please configure: {', '.join(missing_items)}")
    
    # Pipeline execution button
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "🚀 Start Pipeline", 
            disabled=not ready_to_run,
            type="primary" if ready_to_run else "secondary",
            use_container_width=True
        ):
            if ready_to_run:
                start_pipeline_execution()
            else:
                st.error("Cannot start pipeline - missing requirements")
    
    with col2:
        if st.button("🎭 Demo Complete Pipeline", type="secondary", use_container_width=True):
            from streamlit_app.components.mock_data import load_mock_documents_to_session
            load_mock_documents_to_session()
            st.success("🎉 Demo pipeline completed! Check the 'Progress & Output' tab to see generated documents.")
            st.balloons()
    
    # Reset button
    if st.button("🔄 Reset Pipeline", use_container_width=True):
        reset_pipeline_state()
        st.success("Pipeline reset successfully!")
        st.rerun()


def start_pipeline_execution():
    """Start the AI pipeline execution"""
    
    st.session_state.pipeline_state = "processing"
    st.session_state.processing_progress = 0
    st.session_state.current_agent = "Initializing..."
    
    # TODO: Connect to actual AI pipeline
    st.info("🚀 Pipeline execution started! (Integration with AI agents coming next)")
    
    # Placeholder for actual pipeline integration
    st.session_state.pipeline_state = "completed"
    st.session_state.processing_progress = 100
    st.session_state.current_agent = "Completed"
    

def reset_pipeline_state():
    """Reset pipeline state to initial values"""
    st.session_state.pipeline_state = "idle"
    st.session_state.processing_progress = 0
    st.session_state.current_agent = ""
    st.session_state.generated_documents = {}


if __name__ == "__main__":
    main()