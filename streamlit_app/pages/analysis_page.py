"""
Analysis Page - Content Analysis & Routing Recommendations  
Shows Input Router Agent analysis and AI pipeline routing decisions
"""
import streamlit as st
import json
from datetime import datetime
from streamlit_app.pages.page_navigation import get_page_navigator
from streamlit_app.storage.project_manager import get_project_manager


def render_analysis_page():
    """Render the content analysis and routing page"""
    
    st.title("🤖 Content Analysis & AI Routing")
    st.markdown("""
    **Step 2**: AI analysis of your business content and intelligent routing recommendations.
    
    The Input Router Agent analyzes your content to determine:
    - Content type and business context
    - Required AI agents and processing sequence  
    - Industry insights and stakeholder mapping
    - Similar past proposals from knowledge base
    """)
    
    # Check if we have input to analyze
    smart_input = st.session_state.get("smart_input")
    if not smart_input:
        st.error("❌ No input content found. Please go back to the Input page first.")
        if st.button("← Go to Input Page"):
            st.session_state.current_page = "input"
            st.rerun()
        return
    
    # Show input summary
    render_input_summary()
    
    st.markdown("---")
    
    # Analysis section
    render_analysis_section()
    
    # Routing recommendations
    render_routing_section()
    
    # Progress and next steps
    render_analysis_progress_section()


def render_input_summary():
    """Render summary of the input content"""
    
    smart_input = st.session_state["smart_input"]
    
    st.subheader("📄 Input Content Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Customer/Project", smart_input.get("customer_name", "Unnamed"))
    
    with col2:
        st.metric("Content Type", smart_input.get("content_type_hint", "General"))
    
    with col3:
        word_count = len(smart_input["content"].split())
        st.metric("Word Count", f"{word_count:,}")
    
    with col4:
        input_method = smart_input.get("input_method", "manual").title()
        st.metric("Input Method", input_method)
    
    # Show content preview
    with st.expander("📖 Content Preview", expanded=False):
        preview_content = smart_input["content"][:500]
        if len(smart_input["content"]) > 500:
            preview_content += "..."
        st.text_area("Input Content Preview", value=preview_content, height=150, disabled=True)


def render_analysis_section():
    """Render AI content analysis results"""
    
    st.subheader("🔍 AI Content Analysis")
    
    # Check if we already have analysis results
    if not st.session_state.get("analysis_results"):
        # Generate analysis
        if st.button("🚀 Analyze Content with AI", type="primary", use_container_width=True):
            perform_content_analysis()
            st.rerun()
        
        st.info("👆 Click above to analyze your content with the Input Router Agent")
        return
    
    # Display analysis results
    analysis = st.session_state["analysis_results"]
    
    # Core analysis metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Transcript Detected", 
            "Yes" if analysis.get("is_transcript", False) else "No",
            help="Whether this appears to be a conversation transcript"
        )
    
    with col2:
        st.metric(
            "Content Category",
            analysis.get("content_type", "general_business").replace("_", " ").title(),
            help="Primary content type classification"
        )
    
    with col3:
        st.metric(
            "Urgency Level",
            analysis.get("urgency_level", "medium").title(),
            help="Detected business urgency"
        )
    
    # Detailed analysis tabs
    analysis_tabs = st.tabs(["🏭 Business Intelligence", "🎯 Solution Mapping", "⏰ Timeline & Budget", "🔍 RAG Insights"])
    
    with analysis_tabs[0]:
        render_business_intelligence_tab(analysis)
    
    with analysis_tabs[1]:
        render_solution_mapping_tab(analysis)
    
    with analysis_tabs[2]:
        render_timeline_budget_tab(analysis)
    
    with analysis_tabs[3]:
        render_rag_insights_tab(analysis)


def render_business_intelligence_tab(analysis):
    """Render business intelligence analysis"""
    
    st.markdown("### 🏭 Business Context Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Industry Indicators:**")
        industries = analysis.get("industry_hints", [])
        if industries:
            for industry in industries:
                st.markdown(f"- 🏭 {industry.title()}")
        else:
            st.markdown("- No specific industry detected")
    
    with col2:
        st.markdown("**Stakeholder Mentions:**")
        stakeholders = analysis.get("stakeholder_mentions", [])
        if stakeholders:
            for stakeholder in stakeholders:
                st.markdown(f"- 👤 {stakeholder}")
        else:
            st.markdown("- No specific stakeholders mentioned")


def render_solution_mapping_tab(analysis):
    """Render solution type mapping"""
    
    st.markdown("### 🎯 Solution Type Mapping")
    
    solution_indicators = analysis.get("solution_indicators", [])
    
    if solution_indicators:
        cols = st.columns(min(len(solution_indicators), 3))
        for i, solution in enumerate(solution_indicators):
            with cols[i % 3]:
                st.info(f"💡 **{solution.title()}**\nSolution type detected")
    else:
        st.info("🔍 No specific solution types detected - general business analysis will be performed")


def render_timeline_budget_tab(analysis):
    """Render timeline and budget analysis"""
    
    st.markdown("### ⏰ Timeline & Budget Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Timeline Mentions:**")
        timeline_mentions = analysis.get("timeline_mentions", [])
        if timeline_mentions:
            for timeline in timeline_mentions:
                st.markdown(f"- 📅 {timeline}")
        else:
            st.markdown("- No specific timeline mentioned")
    
    with col2:
        st.markdown("**Budget Indicators:**")
        budget_indicators = analysis.get("budget_indicators", [])
        if budget_indicators:
            for budget in budget_indicators:
                st.markdown(f"- 💰 {budget}")
        else:
            st.markdown("- No budget information detected")


def render_rag_insights_tab(analysis):
    """Render RAG knowledge base insights"""
    
    st.markdown("### 🔍 Knowledge Base Insights")
    
    # RAG search terms
    st.markdown("**Generated Search Terms:**")
    rag_terms = analysis.get("rag_search_terms", [])
    if rag_terms:
        for term in rag_terms:
            st.code(term, language=None)
    
    st.markdown("**Similar Past Proposals (Mock):**")
    st.info("🚧 RAG system integration coming soon. This will show similar past proposals from your knowledge base.")
    
    # Mock similar proposals
    mock_proposals = [
        {"title": "Manufacturing Digital Transformation", "similarity": 87, "customer": "TechMfg Corp"},
        {"title": "Supply Chain Optimization Platform", "similarity": 74, "customer": "Global Industries"},
        {"title": "ERP Integration & Analytics", "similarity": 68, "customer": "Precision Manufacturing"}
    ]
    
    for proposal in mock_proposals:
        with st.expander(f"📄 {proposal['title']} ({proposal['similarity']}% match)"):
            st.markdown(f"**Customer**: {proposal['customer']}")
            st.markdown(f"**Similarity**: {proposal['similarity']}%")
            st.markdown("**Key Elements**: Integration, Analytics, Manufacturing")
            st.button(f"Use as Reference", key=f"ref_{proposal['title']}")


def render_routing_section():
    """Render AI agent routing recommendations"""
    
    st.markdown("---")
    st.subheader("🗺️ AI Agent Routing Strategy")
    
    if not st.session_state.get("analysis_results"):
        st.info("Complete content analysis first to see routing recommendations.")
        return
    
    analysis = st.session_state["analysis_results"]
    agents_routing = analysis.get("agents_routing", {})
    
    # Agent workflow visualization
    st.markdown("**Recommended Agent Sequence:**")
    
    agents_info = [
        {
            "key": "conversa",
            "name": "Conversa",
            "icon": "🎧",
            "description": "Transcript analysis and requirement extraction",
            "recommended": agents_routing.get("conversa", False)
        },
        {
            "key": "conny", 
            "name": "Conny",
            "icon": "💼",
            "description": "Business consulting and solution architecture",
            "recommended": agents_routing.get("conny", True)
        },
        {
            "key": "prody",
            "name": "ProDy",
            "icon": "📋",
            "description": "Document generation and project management",
            "recommended": agents_routing.get("prody", True)
        },
        {
            "key": "marketing",
            "name": "Marketing Agent",
            "icon": "🎨",
            "description": "Customer-facing sales deck creation",
            "recommended": agents_routing.get("marketing", True)
        }
    ]
    
    for i, agent in enumerate(agents_info):
        if agent["recommended"]:
            st.success(f"**Step {i+1}**: {agent['icon']} **{agent['name']}** - {agent['description']}")
        else:
            st.info(f"**Skip**: {agent['icon']} **{agent['name']}** - {agent['description']} (Not needed for this content)")
    
    # Customization options
    with st.expander("🛠️ Customize Agent Sequence", expanded=False):
        st.markdown("**Override automatic routing if needed:**")
        
        for agent in agents_info:
            current_value = agents_routing.get(agent["key"], agent["recommended"])
            new_value = st.checkbox(
                f"{agent['icon']} Include {agent['name']}",
                value=current_value,
                key=f"custom_{agent['key']}",
                help=agent["description"]
            )
            agents_routing[agent["key"]] = new_value
        
        if st.button("💾 Save Custom Routing"):
            st.session_state["analysis_results"]["agents_routing"] = agents_routing
            st.success("Custom routing saved!")
            st.rerun()


def render_analysis_progress_section():
    """Render progress and next step actions"""
    
    st.markdown("---")
    st.subheader("⚡ Ready for AI Processing?")
    
    analysis_complete = st.session_state.get("analysis_results") is not None
    navigator = get_page_navigator()
    
    if analysis_complete:
        analysis = st.session_state["analysis_results"]
        
        # Show processing summary
        st.success("✅ Content analysis completed!")
        
        agents_to_run = [k for k, v in analysis.get("agents_routing", {}).items() if v]
        estimated_time = len(agents_to_run) * 2  # Rough estimate
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Agents to Execute", len(agents_to_run))
        with col2:
            st.metric("Estimated Time", f"{estimated_time} minutes")
        with col3:
            st.metric("Expected Documents", "5+ artifacts")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start AI Processing", type="primary", use_container_width=True):
                navigator.mark_page_completed("analysis")
                st.session_state.current_page = "processing"
                st.success("✅ Analysis saved! Starting AI agent pipeline...")
                st.rerun()
        
        with col2:
            if st.button("📊 View Processing Plan", use_container_width=True):
                show_processing_plan(analysis)
    
    else:
        st.warning("⚠️ Complete the content analysis above to continue.")
        
        # Quick analysis shortcut
        if st.button("⚡ Quick Analysis", use_container_width=True):
            perform_content_analysis()
            st.rerun()


def perform_content_analysis():
    """Perform AI content analysis (mock implementation)"""
    
    smart_input = st.session_state.get("smart_input")
    if not smart_input:
        return
    
    # Show progress
    with st.spinner("🤖 Analyzing content with Input Router Agent..."):
        import time
        time.sleep(2)  # Simulate processing
        
        # Import analysis function from smart_input component
        from streamlit_app.components.smart_input import generate_preview_analysis
        analysis_results = generate_preview_analysis(smart_input["content"])
        
        # Add agent routing recommendations
        is_transcript = analysis_results.get("is_transcript", False)
        content_type = analysis_results.get("content_type", "general_business")
        
        # Smart routing based on content
        agents_routing = {
            "conversa": is_transcript,  # Only if transcript
            "conny": True,  # Always needed for business consulting
            "prody": True,  # Always needed for document generation
            "marketing": True  # Always create customer-facing materials
        }
        
        analysis_results["agents_routing"] = agents_routing
        
        # Save to session state
        st.session_state["analysis_results"] = analysis_results
        
        # Update project if exists
        if st.session_state.get("current_project_id"):
            project_manager = get_project_manager()
            project_manager.update_project_progress(
                project_id=st.session_state["current_project_id"],
                progress_step="processing"
            )
    
    st.success("✅ Content analysis completed!")


def show_processing_plan(analysis):
    """Show detailed processing plan"""
    
    st.info("📋 **Processing Plan**: The following agents will execute in sequence based on your content analysis.")
    
    agents_routing = analysis.get("agents_routing", {})
    
    for i, (agent_key, should_run) in enumerate(agents_routing.items()):
        if should_run:
            agent_names = {
                "conversa": "🎧 Conversa (Transcript Analysis)",
                "conny": "💼 Conny (Business Consulting)", 
                "prody": "📋 ProDy (Document Generation)",
                "marketing": "🎨 Marketing Agent (Sales Materials)"
            }
            
            st.markdown(f"**Step {i+1}**: {agent_names.get(agent_key, agent_key)}")
    
    st.markdown("**Expected Output**: Problem overview, process documentation, investment proposal, sales deck, and implementation roadmap.")