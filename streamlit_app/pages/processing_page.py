"""
Processing Page - AI Agent Pipeline Execution
Real-time monitoring of multi-agent proposal generation (Conversa → Conny → ProDy → Marketing)
"""
import streamlit as st
import asyncio
import json
from datetime import datetime
from streamlit_app.pages.page_navigation import get_page_navigator  
from streamlit_app.storage.project_manager import get_project_manager
from streamlit_app.components.dynamic_pipeline import execute_smart_pipeline


def render_processing_page():
    """Render the AI agent processing page with real-time monitoring"""
    
    st.title("⚡ AI Agent Processing Pipeline")
    st.markdown("""
    **Step 3**: Watch as specialized AI agents collaborate to transform your input into a complete proposal package.
    
    **Agent Sequence**: Conversa → Conny → ProDy → Marketing Agent
    """)
    
    # Check prerequisites
    if not st.session_state.get("smart_input") or not st.session_state.get("analysis_results"):
        st.error("❌ Missing prerequisites. Please complete Input and Analysis steps first.")
        render_prerequisites_help()
        return
    
    # Show processing overview
    render_processing_overview()
    
    st.markdown("---")
    
    # Processing control and monitoring
    render_processing_control()
    
    # Real-time progress monitoring
    render_progress_monitoring()
    
    # Results section (if completed)
    render_processing_results()


def render_prerequisites_help():
    """Show help for missing prerequisites"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Go to Input Page", use_container_width=True):
            st.session_state.current_page = "input"
            st.rerun()
    
    with col2:
        if st.button("← Go to Analysis Page", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()


def render_processing_overview():
    """Render processing overview and agent sequence"""
    
    st.subheader("🎯 Processing Overview")
    
    analysis = st.session_state.get("analysis_results", {})
    agents_routing = analysis.get("agents_routing", {})
    smart_input = st.session_state.get("smart_input", {})
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_agents = sum(1 for v in agents_routing.values() if v)
        st.metric("Active Agents", active_agents)
    
    with col2:
        estimated_time = active_agents * 2  # 2 minutes per agent estimate
        st.metric("Est. Time", f"{estimated_time} min")
    
    with col3:
        st.metric("Customer", smart_input.get("customer_name", "Unknown"))
    
    with col4:
        expected_docs = 5 if agents_routing.get("prody", False) else 2
        st.metric("Expected Docs", expected_docs)
    
    # Agent sequence visualization
    render_agent_sequence_viz()


def render_agent_sequence_viz():
    """Render visual agent sequence flow"""
    
    st.markdown("### 🗺️ Agent Processing Flow")
    
    analysis = st.session_state.get("analysis_results", {})
    agents_routing = analysis.get("agents_routing", {})
    
    # Current processing state
    current_agent = st.session_state.get("current_processing_agent", "")
    completed_agents = st.session_state.get("completed_agents", [])
    
    agents_info = [
        {
            "key": "conversa",
            "name": "Conversa",
            "icon": "🎧", 
            "description": "Transcript Analysis & Requirements",
            "outputs": ["Structured requirements", "Stakeholder mapping"]
        },
        {
            "key": "conny",
            "name": "Conny", 
            "icon": "💼",
            "description": "Business Consulting & Architecture",
            "outputs": ["Solution architecture", "Implementation strategy"]
        },
        {
            "key": "prody",
            "name": "ProDy",
            "icon": "📋", 
            "description": "Document Generation & PM",
            "outputs": ["Problem overview", "Process docs", "Investment proposal", "Roadmap"]
        },
        {
            "key": "marketing",
            "name": "Marketing Agent",
            "icon": "🎨",
            "description": "Customer-Facing Materials",
            "outputs": ["Sales deck", "Executive summary", "Value proposition"]
        }
    ]
    
    # Progress visualization
    for i, agent in enumerate(agents_info):
        if not agents_routing.get(agent["key"], False):
            continue  # Skip agents not in routing
        
        # Determine status
        if agent["key"] in completed_agents:
            status_color = "success"
            status_text = "✅ Completed"
        elif agent["key"] == current_agent:
            status_color = "info"
            status_text = "⚡ Processing..."
        elif any(a in completed_agents for a in [ag["key"] for ag in agents_info[:i]]):
            status_color = "warning"
            status_text = "⏳ Queued"
        else:
            status_color = "secondary"
            status_text = "⚪ Waiting"
        
        # Render agent card
        if status_color == "success":
            st.success(f"**{agent['icon']} {agent['name']}** - {status_text}")
        elif status_color == "info":
            st.info(f"**{agent['icon']} {agent['name']}** - {status_text}")
        elif status_color == "warning":
            st.warning(f"**{agent['icon']} {agent['name']}** - {status_text}")
        else:
            st.secondary(f"**{agent['icon']} {agent['name']}** - {status_text}")
        
        # Show expected outputs
        with st.expander(f"📋 Expected Outputs from {agent['name']}", expanded=False):
            st.markdown(f"**Primary Function**: {agent['description']}")
            st.markdown("**Expected Artifacts**:")
            for output in agent["outputs"]:
                st.markdown(f"- {output}")


def render_processing_control():
    """Render processing control buttons and status"""
    
    st.subheader("🚀 Processing Control")
    
    # Check current processing status
    is_processing = st.session_state.get("pipeline_state") == "processing"
    is_completed = st.session_state.get("pipeline_state") == "completed"
    
    if not is_processing and not is_completed:
        # Start processing
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start AI Pipeline", type="primary", use_container_width=True):
                start_pipeline_execution()
        
        with col2:
            if st.button("🎭 Demo Mode (Fast)", use_container_width=True):
                start_demo_pipeline()
    
    elif is_processing:
        # Show stop/pause controls during processing
        st.info("⚡ **Pipeline is running!** Monitor progress below...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.pipeline_state = "paused"
                st.warning("Pipeline paused.")
                st.rerun()
        
        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.session_state.pipeline_state = "stopped"
                st.error("Pipeline stopped.")
                st.rerun()
        
        with col3:
            if st.button("🔄 Refresh Status", use_container_width=True):
                st.rerun()
    
    elif is_completed:
        # Completed - show results and actions
        st.success("✅ **Pipeline completed successfully!**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 View Results", type="primary", use_container_width=True):
                st.session_state.current_page = "review"
                navigator = get_page_navigator()
                navigator.mark_page_completed("processing")
                st.rerun()
        
        with col2:
            if st.button("💾 Export Package", use_container_width=True):
                export_results_package()
        
        with col3:
            if st.button("🔄 Run Again", use_container_width=True):
                restart_pipeline()


def render_progress_monitoring():
    """Render real-time progress monitoring"""
    
    is_processing = st.session_state.get("pipeline_state") == "processing"
    
    if not is_processing:
        return
    
    st.markdown("---")
    st.subheader("📊 Real-Time Progress")
    
    # Overall progress bar
    progress = st.session_state.get("processing_progress", 0)
    st.progress(progress / 100)
    
    current_agent = st.session_state.get("current_processing_agent", "Starting...")
    st.info(f"🤖 **Current Activity**: {current_agent}")
    
    # Detailed agent progress
    with st.expander("🔍 Detailed Progress", expanded=True):
        completed_agents = st.session_state.get("completed_agents", [])
        
        for agent in ["conversa", "conny", "prody", "marketing"]:
            analysis = st.session_state.get("analysis_results", {})
            if not analysis.get("agents_routing", {}).get(agent, False):
                continue
            
            if agent in completed_agents:
                st.success(f"✅ {agent.title()} - Completed")
            elif agent == st.session_state.get("current_processing_agent", ""):
                st.info(f"⚡ {agent.title()} - Processing...")
            else:
                st.secondary(f"⚪ {agent.title()} - Waiting")
    
    # Live log (mock)
    with st.expander("📝 Processing Log", expanded=False):
        log_entries = st.session_state.get("processing_log", [])
        for entry in log_entries[-10:]:  # Show last 10 entries
            timestamp = entry.get("timestamp", "")
            message = entry.get("message", "")
            st.text(f"[{timestamp}] {message}")


def render_processing_results():
    """Render processing results if completed"""
    
    if st.session_state.get("pipeline_state") != "completed":
        return
    
    st.markdown("---")
    st.subheader("🎉 Processing Results")
    
    results = st.session_state.get("pipeline_results")
    if not results:
        st.warning("No results found.")
        return
    
    # Import results rendering from dynamic_pipeline
    from streamlit_app.components.dynamic_pipeline import render_pipeline_results
    render_pipeline_results(results)


def start_pipeline_execution():
    """Start the actual AI pipeline execution"""
    
    st.session_state.pipeline_state = "processing"
    st.session_state.processing_progress = 0
    st.session_state.current_processing_agent = "Initializing pipeline..."
    st.session_state.completed_agents = []
    st.session_state.processing_log = [
        {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": "Pipeline started"}
    ]
    
    smart_input = st.session_state.get("smart_input")
    
    # Execute the smart pipeline
    try:
        import asyncio
        
        # Create event loop if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Execute pipeline with progress updates
        st.info("🚀 Starting AI agent pipeline...")
        
        # This would be the actual pipeline execution
        # For now, we'll simulate with the existing smart pipeline
        results = loop.run_until_complete(execute_smart_pipeline(smart_input))
        
        # Store results
        st.session_state["pipeline_results"] = results
        st.session_state.pipeline_state = "completed"
        st.session_state.processing_progress = 100
        st.session_state.current_processing_agent = "All agents completed"
        
        # Save artifacts to project
        save_pipeline_results_to_project(results)
        
        st.success("🎉 Pipeline execution completed!")
        st.rerun()
        
    except Exception as e:
        st.session_state.pipeline_state = "error"
        st.session_state.current_processing_agent = f"Error: {str(e)}"
        st.error(f"❌ Pipeline execution failed: {str(e)}")


def start_demo_pipeline():
    """Start demo pipeline with mock results"""
    
    st.session_state.pipeline_state = "processing"
    
    # Simulate quick processing
    import time
    
    agents = ["conversa", "conny", "prody", "marketing"] 
    analysis = st.session_state.get("analysis_results", {})
    active_agents = [agent for agent in agents if analysis.get("agents_routing", {}).get(agent, False)]
    
    progress_placeholder = st.empty()
    
    for i, agent in enumerate(active_agents):
        st.session_state.current_processing_agent = f"{agent.title()} processing..."
        st.session_state.processing_progress = int((i / len(active_agents)) * 100)
        
        progress_placeholder.info(f"⚡ {agent.title()} is processing...")
        time.sleep(1)  # Quick demo
        
        st.session_state.completed_agents = active_agents[:i+1]
    
    # Generate mock results
    mock_results = {
        "analysis_summary": "Demo analysis completed",
        "generated_documents": {
            "problem_overview": "# Problem Overview\n\nDemo problem analysis...",
            "solution_architecture": "# Solution Architecture\n\nDemo solution design...",
            "investment_proposal": "# Investment Proposal\n\nDemo investment analysis...",
            "implementation_roadmap": "# Implementation Roadmap\n\nDemo roadmap...",
            "sales_deck": "# Executive Summary\n\nDemo sales presentation..."
        },
        "mermaid_diagrams": [
            {"title": "Process Flow", "code": "graph TD\nA[Start] --> B[Process]\nB --> C[End]"}
        ]
    }
    
    st.session_state["pipeline_results"] = mock_results
    st.session_state.pipeline_state = "completed"
    st.session_state.processing_progress = 100
    st.session_state.current_processing_agent = "Demo completed"
    
    progress_placeholder.success("🎉 Demo pipeline completed!")
    st.balloons()
    st.rerun()


def save_pipeline_results_to_project(results):
    """Save pipeline results as artifacts in current project"""
    
    project_id = st.session_state.get("current_project_id")
    if not project_id:
        return
    
    project_manager = get_project_manager()
    generated_docs = results.get("generated_documents", {})
    
    # Save each generated document as an artifact
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
        progress_step="review",
        status="completed"
    )


def export_results_package():
    """Export processing results as downloadable package"""
    
    project_id = st.session_state.get("current_project_id")
    if not project_id:
        st.warning("No project to export.")
        return
    
    project_manager = get_project_manager()
    zip_data = project_manager.export_project_to_zip(project_id)
    
    if zip_data:
        project_name = st.session_state.get("project_name", "proposal").replace(" ", "_")
        filename = f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
        
        st.download_button(
            label="📦 Download Complete Package",
            data=zip_data,
            file_name=filename,
            mime="application/zip"
        )
        
        st.success("✅ Package ready for download!")


def restart_pipeline():
    """Restart the pipeline from beginning"""
    
    st.session_state.pipeline_state = "idle"
    st.session_state.processing_progress = 0
    st.session_state.current_processing_agent = ""
    st.session_state.completed_agents = []
    st.session_state.processing_log = []
    
    st.info("🔄 Pipeline reset. Ready to start again.")
    st.rerun()