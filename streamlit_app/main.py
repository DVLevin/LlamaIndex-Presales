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
from streamlit_app.components.smart_input import render_smart_input_section
from streamlit_app.components.model_selection import render_model_selection
from streamlit_app.components.pipeline_progress import render_pipeline_progress
from streamlit_app.components.document_preview import render_document_preview
from streamlit_app.components.overview_visualization import render_overview_section
from streamlit_app.components.prompt_management import render_prompt_management_section
from streamlit_app.components.dynamic_pipeline import execute_smart_pipeline, render_pipeline_results
from streamlit_app.storage.project_manager import get_project_manager


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
    elif selected_page == "Projects":
        render_projects_section()


def render_sidebar_navigation(config):
    """Render LazyFlow sidebar navigation"""
    
    st.sidebar.title("🤖 AI Proposal Pipeline")
    st.sidebar.markdown("*30% cycle-time reduction*")
    
    # Main navigation
    st.sidebar.markdown("---")
    selected_page = st.sidebar.radio(
        "Navigate",
        ["About", "Proposals", "Projects", "Configurations"],
        index=1,  # Default to Proposals page
        format_func=lambda x: {
            "About": "📋 About",
            "Proposals": "🎯 Proposals", 
            "Projects": "📚 Projects",
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
    if st.session_state.get("smart_input"):
        input_type = st.session_state["smart_input"].get("content_type_hint", "Content")
        st.sidebar.metric("💭 Input", input_type)
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
        st.subheader("💭 Smart Input Center")
        render_smart_input_section()
        
        st.subheader("🤖 Model Configuration")
        render_model_selection(config)
        render_smart_pipeline_controls()
    
    with col2:
        st.subheader("📊 Generation Progress")
        render_pipeline_progress()
        
        st.subheader("📄 Document Library")
        render_document_preview()


def render_projects_section():
    """Render projects library section"""
    from streamlit_app.pages.projects_page import render_projects_page
    render_projects_page()


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
        st.session_state.get("smart_input") is not None
    )
    
    if ready_to_run:
        st.success("🟢 Ready for one-tap generation!")
        
        # Single-tap generation button - THIS WAS THE MISSING BUTTON!
        if st.button("🚀 Generate Proposal Package", type="primary", use_container_width=True):
            start_pipeline_execution()
            
    else:
        # Smart guidance for what's missing
        missing_items = []
        if not all(api_status.values()):
            missing_items.append("API keys (go to Configurations)")
        if not st.session_state.get("smart_input"):
            missing_items.append("business input content")
            
        st.warning(f"⚠️ Setup needed: {', '.join(missing_items)}")
        
        if st.button("🔧 Quick Setup", type="tertiary", use_container_width=True):
            if not all(api_status.values()):
                st.info("👆 Configure API keys in the Configurations tab")
    
    # Demo and reset options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎭 Demo Mode", type="tertiary", use_container_width=True):
            load_demo_data()
    
    with col2:
        if st.button("🔄 Reset", type="tertiary", use_container_width=True):
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
    """Start the smart AI pipeline execution"""
    
    # Check if we have smart input
    smart_input = st.session_state.get("smart_input")
    if not smart_input:
        st.error("❌ No input content available. Please provide business input first.")
        return
    
    st.session_state.pipeline_state = "processing"
    st.session_state.processing_progress = 0
    st.session_state.current_agent = "Starting smart pipeline..."
    
    # Execute the smart pipeline
    try:
        # Run the smart pipeline asynchronously
        import asyncio
        
        # Create event loop if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Execute the smart pipeline
        results = loop.run_until_complete(execute_smart_pipeline(smart_input))
        
        # Store results in session state
        st.session_state["pipeline_results"] = results
        st.session_state.pipeline_state = "completed"
        st.session_state.processing_progress = 100
        st.session_state.current_agent = "Smart pipeline completed"
        
        # Save to project manager
        save_pipeline_results_to_project(results, smart_input)
        
        # Show results
        st.success("🎉 Smart pipeline execution completed!")
        render_pipeline_results(results)
        
    except Exception as e:
        st.session_state.pipeline_state = "error"
        st.session_state.current_agent = f"Error: {str(e)}"
        st.error(f"❌ Pipeline execution failed: {str(e)}")


def save_pipeline_results_to_project(results, smart_input):
    """Save pipeline results as a project"""
    try:
        project_manager = get_project_manager()
        
        # Create project
        customer_name = smart_input.get("customer_name", "Customer")
        project_name = f"{customer_name} - AI Proposal"
        
        project_id = project_manager.create_project(
            name=project_name,
            customer_name=customer_name,
            input_content=smart_input["content"],
            input_metadata=smart_input
        )
        
        # Save artifacts
        generated_docs = results.get("generated_documents", {})
        for doc_type, content in generated_docs.items():
            project_manager.save_artifact(
                project_id=project_id,
                artifact_type=doc_type,
                title=doc_type.replace("_", " ").title(),
                content=content,
                format="markdown",
                agent_generated="ai_pipeline"
            )
        
        # Update project status
        project_manager.update_project_progress(
            project_id=project_id,
            progress_step="completed",
            status="completed"
        )
        
        st.session_state["current_project_id"] = project_id
        st.success(f"✅ Project saved: {project_name}")
        
    except Exception as e:
        st.warning(f"⚠️ Results generated but project save failed: {str(e)}")


def load_demo_data():
    """Load demo data for testing"""
    demo_transcript = """Customer Discovery Call - Acme Manufacturing Corp

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
"""
    
    st.session_state["smart_input"] = {
        "content": demo_transcript,
        "format": "Customer Transcript",
        "customer_name": "Acme Manufacturing Corp",
        "content_type_hint": "Customer Transcript",
        "input_method": "demo",
        "timestamp": datetime.now().isoformat()
    }
    
    st.success("🎭 Demo data loaded! Ready to generate proposal.")
    st.balloons()


def reset_pipeline_state():
    """Reset pipeline state to initial values"""
    st.session_state.pipeline_state = "idle"
    st.session_state.processing_progress = 0
    st.session_state.current_agent = ""
    st.session_state.generated_documents = {}
    if "smart_input" in st.session_state:
        del st.session_state["smart_input"]
    if "pipeline_results" in st.session_state:
        del st.session_state["pipeline_results"]


if __name__ == "__main__":
    main()