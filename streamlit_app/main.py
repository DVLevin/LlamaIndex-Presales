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
    
    # Sidebar navigation
    selected_page = render_sidebar_navigation(config)
    
    # Main content based on sidebar selection
    if selected_page == "About":
        render_about_section()
    elif selected_page == "Proposals":
        render_proposals_section(config)
    elif selected_page == "Configurations":
        render_configurations_section()


def render_sidebar_navigation(config):
    """Render LazyFlow sidebar navigation"""
    
    st.sidebar.title("🤖 AI Proposal Pipeline")
    st.sidebar.markdown("*30% cycle-time reduction*")
    
    # Main navigation
    st.sidebar.markdown("---")
    selected_page = st.sidebar.radio(
        "Navigate",
        ["About", "Proposals", "Configurations"],
        index=0,
        format_func=lambda x: {
            "About": "📋 About",
            "Proposals": "🎯 Proposals", 
            "Configurations": "⚙️ Configurations"
        }[x]
    )
    
    # Quick status indicators
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Quick Status")
    
    # API Keys status
    api_status = validate_api_keys(config)
    if all(api_status.values()):
        st.sidebar.success("🟢 APIs Ready")
    else:
        missing_keys = [key for key, status in api_status.items() if not status]
        st.sidebar.warning(f"⚠️ Setup: {', '.join(missing_keys)}")
    
    # Pipeline status
    pipeline_state = st.session_state.get("pipeline_state", "idle")
    status_colors = {
        "idle": "🔵 Ready",
        "processing": "🟡 Processing", 
        "completed": "🟢 Completed",
        "error": "🔴 Error"
    }
    st.sidebar.info(f"{status_colors.get(pipeline_state, '⚪ Unknown')}")
    
    # Quick stats
    if st.session_state.get("current_transcript"):
        st.sidebar.metric("📄 Transcript", "Uploaded")
    if st.session_state.get("knowledge_base_docs"):
        doc_count = len(st.session_state.knowledge_base_docs)
        st.sidebar.metric("📚 Knowledge Base", f"{doc_count} docs")
    if st.session_state.get("generated_documents"):
        doc_count = len(st.session_state.generated_documents)
        st.sidebar.metric("📋 Generated", f"{doc_count} docs")
    
    return selected_page


def render_about_section():
    """Render About section with business value and demo"""
    render_overview_section()


def render_proposals_section(config):
    """Render main Proposals workspace - LazyFlow single-tap generation"""
    
    st.markdown("# 🎯 Proposal Generation Workspace")
    st.markdown("**LazyFlow Design: Single-tap proposal generation with smart defaults**")
    
    # Progress indicator at top
    render_progress_indicator()
    
    # Main workflow in columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Input Center")
        render_file_upload_section()
        
        st.subheader("🤖 Smart Configuration")
        render_model_selection(config)
        render_smart_pipeline_controls()
    
    with col2:
        st.subheader("📊 Generation Progress")
        render_pipeline_progress()
        
        st.subheader("📄 Document Library")
        render_document_preview()


def render_configurations_section():
    """Render advanced Configurations section"""
    
    st.markdown("# ⚙️ Advanced Configurations")
    st.markdown("**Customize prompts, manage RAG knowledge base, and configure tools**")
    
    # Configuration tabs
    prompt_tab, rag_tab, tools_tab, api_tab = st.tabs([
        "🎯 Prompts", "📚 Knowledge Base", "🔧 Tools", "🔑 API Keys"
    ])
    
    with prompt_tab:
        render_prompt_management_section()
    
    with rag_tab:
        render_rag_management_section()
    
    with tools_tab:
        render_tools_configuration_section()
    
    with api_tab:
        render_api_configuration_section()


def render_progress_indicator():
    """Render top-level progress indicator"""
    pipeline_state = st.session_state.get("pipeline_state", "idle")
    
    if pipeline_state == "processing":
        progress = st.session_state.get("processing_progress", 0)
        st.progress(progress / 100)
        current_agent = st.session_state.get("current_agent", "Processing...")
        st.info(f"🤖 {current_agent}")
    elif pipeline_state == "completed":
        st.success("✅ Proposal generation completed!")
    elif pipeline_state == "error":
        st.error("❌ Generation failed - check configurations")


def render_smart_pipeline_controls():
    """Render smart pipeline controls with LazyFlow principles"""
    
    st.subheader("🚀 Generation Controls")
    
    config = load_config()
    api_status = validate_api_keys(config)
    
    # Smart readiness check
    ready_to_run = (
        all(api_status.values()) and 
        st.session_state.get("current_transcript") is not None
    )
    
    if ready_to_run:
        st.success("🟢 Ready for one-tap generation!")
        
        # Single-tap generation button
        if st.button("🚀 Generate Proposal Package", type="primary", use_container_width=True):
            start_pipeline_execution()
            
    else:
        # Smart guidance for what's missing
        missing_items = []
        if not all(api_status.values()):
            missing_items.append("API keys (go to Configurations)")
        if not st.session_state.get("current_transcript"):
            missing_items.append("customer transcript")
            
        st.warning(f"⚠️ Setup needed: {', '.join(missing_items)}")
        
        if st.button("🔧 Quick Setup", use_container_width=True):
            if not all(api_status.values()):
                st.info("👆 Configure API keys in the sidebar or Configurations section")
    
    # Demo and reset options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎭 Demo Mode", use_container_width=True):
            from streamlit_app.components.mock_data import load_mock_documents_to_session
            load_mock_documents_to_session()
            st.success("🎉 Demo data loaded!")
            st.balloons()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_pipeline_state()
            st.success("Reset complete!")
            st.rerun()


def render_rag_management_section():
    """Render RAG knowledge base management (placeholder)"""
    st.markdown("### 📚 Knowledge Base Management")
    st.info("🚧 **Coming Soon**: Multi-tenant document storage")
    
    st.markdown("**Planned Features:**")
    st.markdown("- **Company Knowledge**: Organization-wide proposals and case studies")
    st.markdown("- **Customer Projects**: Client-specific documents (like Claude Projects)")
    st.markdown("- **Auto-Categorization**: ML-powered document classification")
    st.markdown("- **Smart Search**: Vector-based document retrieval")
    
    # Current knowledge base preview
    if st.session_state.get("knowledge_base_docs"):
        st.markdown("**Current Knowledge Base:**")
        for i, doc in enumerate(st.session_state.knowledge_base_docs):
            st.markdown(f"- {doc['filename']} ({doc['char_count']:,} chars)")


def render_tools_configuration_section():
    """Render tools configuration (placeholder)"""
    st.markdown("### 🔧 AI Tools Configuration")
    st.info("🚧 **Coming Soon**: Custom tool management")
    
    st.markdown("**Planned Features:**")
    st.markdown("- **Tool Library**: Pre-built analysis and generation tools")
    st.markdown("- **Custom Tools**: User-defined business logic")
    st.markdown("- **Tool Chaining**: Automated tool sequence optimization")
    st.markdown("- **Performance Metrics**: Tool success rates and optimization")


def render_api_configuration_section():
    """Render API key configuration"""
    st.markdown("### 🔑 API Keys Configuration")
    
    config = load_config()
    api_status = validate_api_keys(config)
    
    # OpenRouter configuration
    st.subheader("OpenRouter LLM Service")
    openrouter_status = "✅ Configured" if api_status["openrouter"] else "❌ Missing"
    st.markdown(f"**Status**: {openrouter_status}")
    
    openrouter_key = st.text_input(
        "OpenRouter API Key",
        value=config.openrouter_api_key if config.openrouter_api_key else "",
        type="password",
        placeholder="sk-or-v1-...",
        help="Required for LLM model access"
    )
    
    # Jina AI configuration  
    st.subheader("Jina AI Embeddings & Reranking")
    jina_status = "✅ Configured" if api_status["jina"] else "❌ Missing"
    st.markdown(f"**Status**: {jina_status}")
    
    jina_key = st.text_input(
        "Jina AI API Key", 
        value=config.jina_api_key if config.jina_api_key else "",
        type="password",
        placeholder="jina_...",
        help="Required for embeddings and document reranking"
    )
    
    # Save button
    if st.button("💾 Save API Configuration", type="primary"):
        save_api_keys(openrouter_key, jina_key)
        st.success("✅ API keys saved successfully!")
        st.rerun()
    
    # Configuration help
    with st.expander("ℹ️ How to get API keys"):
        st.markdown("**OpenRouter API Key:**")
        st.markdown("1. Visit [OpenRouter.ai](https://openrouter.ai)")
        st.markdown("2. Sign up and navigate to API Keys")
        st.markdown("3. Generate a new API key")
        
        st.markdown("**Jina AI API Key:**")
        st.markdown("1. Visit [Jina.ai](https://jina.ai)")
        st.markdown("2. Create account and go to API section") 
        st.markdown("3. Generate API key for embeddings")




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