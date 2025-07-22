"""
Overview Visualization Component
Welcome screen with system explanation and mock examples
"""
import streamlit as st
from typing import Dict, List
import json


def render_overview_section():
    """Render the main overview and welcome section"""
    
    # Hero section
    render_hero_section()
    
    # System visualization
    render_system_flow_diagram()
    
    # Key capabilities
    render_capabilities_section()
    
    # Mock example walkthrough
    render_mock_example()


def render_hero_section():
    """Render hero section with main value proposition"""
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🚀 AI-Powered Proposal Pipeline</h1>
        <h3>Transform customer conversations into winning proposals in minutes, not days</h3>
        <p style="font-size: 1.2em; margin-top: 1rem;">
            <strong>Goal: 30% reduction in proposal cycle-time</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_system_flow_diagram():
    """Render system flow visualization"""
    
    st.markdown("### 🔄 **How It Works: 10-Step AI Pipeline**")
    
    # Create columns for the flow
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ```mermaid
        graph TD
            A[📄 Customer Transcript] --> B[🎯 Conversa Agent]
            B --> |Analysis| C[🏗️ Conny Agent]
            C --> |Project Description| D[📋 ProDy Agent]
            D --> |5 Documents| E[🎨 Marketing Agent]
            E --> F[📦 Complete Proposal Package]
            
            G[📚 Company Knowledge] --> C
            G --> D
            G --> E
            
            style A fill:#e1f5fe
            style F fill:#c8e6c9
            style G fill:#fff3e0
        ```
        """)
    
    # Step-by-step breakdown
    st.markdown("### 📊 **Pipeline Steps Breakdown**")
    
    steps_data = get_pipeline_steps_detailed()
    
    for i, step in enumerate(steps_data, 1):
        with st.expander(f"**Step {i}: {step['title']}**", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**🤖 Agent:** {step['agent']}")
                st.markdown(f"**📝 What it does:** {step['description']}")
                st.markdown(f"**🎯 Output:** {step['output']}")
                
                if step.get('tools'):
                    st.markdown("**🔧 Tools used:**")
                    for tool in step['tools']:
                        st.markdown(f"- {tool}")
            
            with col2:
                # Show processing time estimate
                st.metric("⏱️ Est. Time", step.get('time_estimate', '30-60s'))
                
                # Show complexity level
                complexity_colors = {
                    "Simple": "🟢",
                    "Medium": "🟡", 
                    "Complex": "🔴"
                }
                complexity = step.get('complexity', 'Medium')
                st.markdown(f"**📈 Complexity:** {complexity_colors.get(complexity, '⚪')} {complexity}")


def render_capabilities_section():
    """Render key system capabilities"""
    
    st.markdown("### ⚡ **Key Capabilities**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Intelligent Analysis**
        - Extract key requirements from transcripts
        - Identify stakeholders and decision criteria
        - Analyze pain points and opportunities
        - Match to past successful solutions
        """)
    
    with col2:
        st.markdown("""
        **📋 Professional Documentation**
        - Problem overview with business impact
        - Process visualization with Mermaid diagrams
        - Investment proposal with ROI analysis
        - Customer-ready sales presentations
        """)
    
    with col3:
        st.markdown("""
        **🚀 Speed & Quality**
        - 5-minute end-to-end processing
        - Multiple LLM model options
        - Company knowledge base integration
        - Professional templates and formatting
        """)
    
    # ROI metrics
    st.markdown("### 📈 **Expected ROI Impact**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏰ Time Reduction", "30%", "vs manual process")
    
    with col2:
        st.metric("📄 Documents Generated", "6", "professional outputs")
    
    with col3:
        st.metric("🎯 Processing Time", "5 min", "typical transcript")
    
    with col4:
        st.metric("💼 Proposal Quality", "95%+", "consistency score")


def render_mock_example():
    """Render mock example walkthrough"""
    
    st.markdown("### 🎭 **Mock Example: See It In Action**")
    
    example_tab, walkthrough_tab = st.tabs(["📋 Sample Scenario", "🔍 Step-by-Step Walkthrough"])
    
    with example_tab:
        render_sample_scenario()
    
    with walkthrough_tab:
        render_step_walkthrough()


def render_sample_scenario():
    """Render sample business scenario"""
    
    st.markdown("#### 🏢 **Sample Customer Scenario: Acme Corp Digital Transformation**")
    
    # Sample transcript preview
    with st.expander("📄 **Sample Customer Transcript** (Click to expand)", expanded=False):
        sample_transcript = get_sample_transcript()
        st.text_area(
            "Customer Discovery Call Transcript",
            value=sample_transcript,
            height=200,
            disabled=True
        )
    
    # Expected outputs preview
    st.markdown("#### 📦 **Expected Output Package:**")
    
    output_cols = st.columns(2)
    
    with output_cols[0]:
        st.markdown("""
        **📋 Documents Generated:**
        1. **Problem Overview** - Current state analysis
        2. **Process Overview** - Solution methodology
        3. **Process Visualization** - Before/after diagrams
        4. **Investment Proposal** - Budget & timeline
        5. **Next Steps** - Action plan
        6. **Sales Presentation** - Customer-facing deck
        """)
    
    with output_cols[1]:
        # Sample output preview
        with st.expander("📄 Sample: Problem Overview", expanded=False):
            st.markdown(get_sample_problem_overview())
        
        with st.expander("📊 Sample: Process Diagram", expanded=False):
            st.code(get_sample_mermaid_diagram(), language="mermaid")
    
    # Try it button
    if st.button("🚀 **Try This Example**", type="primary", use_container_width=True):
        load_sample_data_to_session()
        st.success("✅ Sample data loaded! Switch to the 'Input & Configuration' section to see it in action.")
        st.balloons()


def render_step_walkthrough():
    """Render step-by-step walkthrough"""
    
    st.markdown("#### 🔍 **How You Would Use This System:**")
    
    walkthrough_steps = [
        {
            "step": 1,
            "title": "Upload Customer Transcript",
            "description": "Upload your customer discovery call transcript (TXT, DOCX, or PDF)",
            "action": "📁 Drag & drop or browse for your transcript file",
            "tip": "💡 Works with recorded call transcripts, meeting notes, or customer interview summaries"
        },
        {
            "step": 2,
            "title": "Upload Company Knowledge",
            "description": "Add relevant company documents to enhance proposal quality",
            "action": "📚 Upload past proposals, case studies, solution briefs",
            "tip": "💡 More documents = better matching to past successful solutions"
        },
        {
            "step": 3,
            "title": "Select AI Model",
            "description": "Choose your preferred language model for processing",
            "action": "🤖 Pick from GPT-4o, Claude-3.5-Sonnet, Llama, or GPT-4o-mini",
            "tip": "💡 GPT-4o for quality, GPT-4o-mini for speed, Claude for analysis"
        },
        {
            "step": 4,
            "title": "Start Pipeline",
            "description": "Launch the 10-step AI agent pipeline",
            "action": "🚀 Click 'Start Pipeline' and watch real-time progress",
            "tip": "💡 Takes 3-7 minutes depending on transcript length and complexity"
        },
        {
            "step": 5,
            "title": "Review & Download",
            "description": "Preview generated documents and download complete package",
            "action": "📄 Review each document, download individually or as ZIP",
            "tip": "💡 Edit and customize documents as needed for your specific context"
        }
    ]
    
    for step_info in walkthrough_steps:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"""
                <div style="background: #667eea; color: white; border-radius: 50%; 
                           width: 60px; height: 60px; display: flex; align-items: center; 
                           justify-content: center; font-size: 1.5em; font-weight: bold; margin: 10px auto;">
                    {step_info['step']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"### {step_info['title']}")
                st.markdown(step_info['description'])
                st.markdown(f"**👆 Your action:** {step_info['action']}")
                st.markdown(f"{step_info['tip']}")
        
        if step_info['step'] < 5:
            st.markdown("---")


def get_pipeline_steps_detailed() -> List[Dict]:
    """Get detailed pipeline steps information"""
    
    return [
        {
            "title": "Transcript Analysis",
            "agent": "Conversa",
            "description": "Analyze customer transcript and extract key requirements, stakeholders, pain points",
            "output": "Structured requirements analysis with business context",
            "tools": ["Transcript Parser", "Requirement Extractor", "Stakeholder Analyzer"],
            "time_estimate": "45s",
            "complexity": "Medium"
        },
        {
            "title": "Project Description",
            "agent": "Conny",
            "description": "Create comprehensive project description based on analysis",
            "output": "Business-ready project overview document",
            "tools": ["Solution Matcher", "RAG Knowledge Search", "Business Analyzer"],
            "time_estimate": "60s",
            "complexity": "Complex"
        },
        {
            "title": "Enhanced Summary",
            "agent": "Conversa",
            "description": "Refine and enhance summary with additional context and details",
            "output": "Enhanced summary v2 with deeper insights",
            "tools": ["Content Enhancer", "Context Analyzer"],
            "time_estimate": "30s",
            "complexity": "Simple"
        },
        {
            "title": "PM Handover Brief",
            "agent": "Conny",
            "description": "Generate zero-knowledge brief for project manager handover",
            "output": "Complete PM handover document with technical details",
            "tools": ["Technical Briefer", "Handover Template"],
            "time_estimate": "45s",
            "complexity": "Medium"
        },
        {
            "title": "Problem Overview",
            "agent": "ProDy",
            "description": "Generate professional problem overview document",
            "output": "Problem overview markdown with business impact analysis",
            "tools": ["Document Generator", "Business Impact Analyzer"],
            "time_estimate": "60s",
            "complexity": "Medium"
        },
        {
            "title": "Process Overview",
            "agent": "ProDy",
            "description": "Create detailed process overview and methodology",
            "output": "Process overview markdown with implementation approach",
            "tools": ["Process Designer", "Methodology Matcher"],
            "time_estimate": "60s",
            "complexity": "Medium"
        },
        {
            "title": "Process Visualization",
            "agent": "ProDy",
            "description": "Generate process diagrams and visualizations",
            "output": "Mermaid diagrams showing before/after process flows",
            "tools": ["Mermaid Generator", "Process Visualizer"],
            "time_estimate": "45s",
            "complexity": "Complex"
        },
        {
            "title": "Investment Proposal",
            "agent": "ProDy",
            "description": "Create comprehensive investment proposal with ROI analysis",
            "output": "Investment proposal markdown with budget and timeline",
            "tools": ["ROI Calculator", "Budget Estimator", "Timeline Planner"],
            "time_estimate": "75s",
            "complexity": "Complex"
        },
        {
            "title": "Next Steps",
            "agent": "ProDy",
            "description": "Generate actionable next steps and decision points",
            "output": "Next steps markdown with clear action items",
            "tools": ["Action Planner", "Decision Mapper"],
            "time_estimate": "30s",
            "complexity": "Simple"
        },
        {
            "title": "Sales Presentation",
            "agent": "Marketing",
            "description": "Create customer-facing sales presentation deck",
            "output": "Sales presentation markdown with value proposition",
            "tools": ["Presentation Builder", "Value Prop Generator"],
            "time_estimate": "90s",
            "complexity": "Complex"
        }
    ]


def get_sample_transcript() -> str:
    """Get sample customer transcript"""
    
    return """Customer Discovery Call - Acme Corp Digital Transformation
Date: 2024-01-15
Participants: John Smith (CTO), Sarah Johnson (VP Operations), Mike Chen (Sales Rep)

[00:05] Mike: Thanks for taking the time today. Can you tell me about your current challenges?

[00:07] John: We're struggling with our legacy inventory management system. It's completely manual, takes 3-4 hours daily just to update stock levels, and we're seeing 15% inventory discrepancies.

[00:12] Sarah: The biggest pain point is that our sales team can't see real-time inventory. They're promising customers products we don't have, leading to order cancellations and unhappy customers.

[00:18] Mike: How is this impacting your business?

[00:20] John: We estimate we're losing about $50K monthly in revenue due to stockouts and overselling. Plus our warehouse staff is spending 20 hours/week on manual data entry instead of value-add activities.

[00:28] Sarah: We've looked at some solutions but they seem complex and expensive. Our budget is around $150K for the initial implementation, and we need something that integrates with our existing Salesforce CRM.

[00:35] Mike: What would success look like for you?

[00:37] John: Real-time inventory visibility, automated stock updates, integration with Salesforce, and reducing manual work by at least 70%. If we could cut our inventory discrepancies to under 2% and eliminate stockouts, that would be transformational.

[00:45] Sarah: Timeline is important too - we need to be live before Q4 holiday season, so implementation by September.

[Additional 20 minutes of detailed technical discussion...]"""


def get_sample_problem_overview() -> str:
    """Get sample problem overview document"""
    
    return """# Problem Overview: Acme Corp Inventory Management Transformation

## Executive Summary
Acme Corp is experiencing significant operational inefficiencies and revenue losses due to their legacy manual inventory management system, requiring urgent digital transformation to maintain competitiveness.

## Current State Analysis
- **Manual inventory updates**: 3-4 hours daily labor
- **Inventory discrepancies**: 15% error rate
- **Revenue loss**: $50K monthly due to stockouts/overselling
- **Staff inefficiency**: 20 hours/week on manual data entry
- **Customer impact**: Order cancellations due to inventory visibility issues

## Business Impact
- **Financial**: $600K annual revenue loss potential
- **Operational**: Significant staff time waste on non-value activities  
- **Customer**: Trust erosion due to unreliable product availability
- **Competitive**: Falling behind in market responsiveness

## Success Criteria
- Reduce inventory discrepancies to <2%
- Achieve 70%+ reduction in manual work
- Real-time inventory visibility across all channels
- Seamless Salesforce CRM integration
- Implementation complete by September 2024

## Investment Parameters
- Budget: $150K initial implementation
- Timeline: 6-month implementation window
- ROI Target: Break-even within 12 months through eliminated losses"""


def get_sample_mermaid_diagram() -> str:
    """Get sample Mermaid diagram"""
    
    return """graph TD
    subgraph "Current Process (Manual)"
        A1[Sales Order] --> B1[Manual Inventory Check]
        B1 --> C1[Phone/Email Warehouse]
        C1 --> D1[Manual Count]
        D1 --> E1[Update Spreadsheet]
        E1 --> F1[Notify Sales]
        F1 --> G1[Customer Response]
    end
    
    subgraph "Proposed Process (Automated)"  
        A2[Sales Order] --> B2[Real-time API Check]
        B2 --> C2[Instant Availability]
        C2 --> D2[Auto-Reserve Inventory]
        D2 --> E2[CRM Update]
        E2 --> F2[Customer Confirmation]
    end
    
    G1 -.->|3-4 hours| A2
    F2 -.->|2-3 minutes| X[Happy Customer]
    
    style A1 fill:#ffcdd2
    style G1 fill:#ffcdd2
    style A2 fill:#c8e6c9
    style F2 fill:#c8e6c9"""


def load_sample_data_to_session():
    """Load sample data into session state"""
    
    # Load sample transcript
    st.session_state.current_transcript = {
        "filename": "acme_corp_discovery_call.txt",
        "content": get_sample_transcript(),
        "upload_time": "2024-01-15T10:30:00",
        "file_type": "text/plain"
    }
    
    # Load sample knowledge base documents
    sample_kb_docs = [
        {
            "filename": "inventory_management_case_study.md",
            "content": "# Inventory Management Success Story\n\nClient achieved 85% reduction in manual work and $2M annual savings through automated inventory system...",
            "upload_time": "2024-01-15T10:31:00",
            "file_type": "text/markdown",
            "char_count": 1250
        },
        {
            "filename": "salesforce_integration_guide.pdf",
            "content": "Salesforce Integration Best Practices\n\nThis document outlines proven approaches for integrating inventory systems with Salesforce CRM...",
            "upload_time": "2024-01-15T10:32:00", 
            "file_type": "application/pdf",
            "char_count": 3400
        }
    ]
    
    st.session_state.knowledge_base_docs = sample_kb_docs
    
    # Set selected model
    st.session_state.selected_model = {
        "name": "gpt-4o",
        "model_id": "openai/gpt-4o"
    }
    
    # Also load mock generated documents to show what the output looks like
    from streamlit_app.components.mock_data import load_mock_documents_to_session
    load_mock_documents_to_session()