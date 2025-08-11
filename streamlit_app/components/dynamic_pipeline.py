"""
Dynamic Pipeline Router Component
Intelligently routes business input through optimized agent workflows
"""
import streamlit as st
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Import AI components (when ready)
try:
    from ai.src.agents.input_router_agent import InputRouterAgent
    from ai.src.rag_system import ProposalRAGSystem
    from ai.src.workflow import PresalesPipelineWorkflow
    from ai.src.llm_integration import OpenRouterClient
    from ai.src.jina_integration import JinaAIClient
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


async def execute_smart_pipeline(smart_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the intelligent pipeline with dynamic routing
    
    Args:
        smart_input: Smart input data from the input component
        
    Returns:
        Complete pipeline results with routing information
    """
    if not AI_AVAILABLE:
        return await execute_mock_smart_pipeline(smart_input)
    
    try:
        st.info("🤖 Initializing AI pipeline...")
        
        # Initialize components
        router_agent = InputRouterAgent()
        rag_system = ProposalRAGSystem()
        llm_client = OpenRouterClient()
        jina_client = JinaAIClient()
        
        # Step 1: Analyze input and create routing plan
        st.info("🔍 Analyzing business input...")
        routing_info = await router_agent.process(
            input_data=smart_input["content"],
            context={
                "customer_name": smart_input.get("customer_name", "Business Input"),
                "content_type_hint": smart_input.get("content_type_hint", "Auto-detect"),
                "input_method": smart_input.get("input_method", "text")
            }
        )
        
        # Step 2: Get relevant past proposal context
        st.info("📚 Finding similar past proposals...")
        proposal_context = await rag_system.get_proposal_context(routing_info)
        
        # Step 3: Execute dynamic agent workflow
        st.info("🚀 Executing optimized agent workflow...")
        pipeline_result = await execute_dynamic_workflow(
            smart_input, routing_info, proposal_context, llm_client, jina_client
        )
        
        # Step 4: Save results to knowledge base for future use
        if pipeline_result.get("status") == "success":
            proposal_id = rag_system.add_proposal_to_knowledge_base(
                proposal_data=pipeline_result["result"],
                customer_name=smart_input.get("customer_name", "Business Input"),
                industry=routing_info.get("industry", "unknown"),
                solution_types=routing_info.get("solution_types", []),
                outcome="pending"
            )
            pipeline_result["proposal_id"] = proposal_id
        
        return {
            "status": "success",
            "routing_info": routing_info,
            "proposal_context": proposal_context,
            "pipeline_result": pipeline_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        st.error(f"❌ Pipeline execution failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


async def execute_dynamic_workflow(smart_input: Dict[str, Any],
                                 routing_info: Dict[str, Any],
                                 proposal_context: Dict[str, Any],
                                 llm_client,
                                 jina_client) -> Dict[str, Any]:
    """Execute the workflow based on dynamic routing decisions"""
    
    try:
        # Get agent routing plan
        agent_routing = routing_info.get("agent_routing", {})
        
        # Create workflow with enhanced context
        workflow = PresalesPipelineWorkflow(llm_client, jina_client)
        
        # Prepare enhanced input with routing context
        enhanced_input = {
            "customer_name": smart_input.get("customer_name", "Business Input"),
            "content": smart_input["content"],
            "routing_info": routing_info,
            "proposal_context": proposal_context,
            "business_metadata": {
                "industry": routing_info.get("industry"),
                "solution_types": routing_info.get("solution_types", []),
                "urgency_level": routing_info.get("urgency_level"),
                "company_size": routing_info.get("company_size")
            }
        }
        
        # Execute workflow with dynamic routing
        if routing_info.get("transcript", False):
            # Full transcript processing workflow
            st.info("📊 Processing as customer transcript...")
            result = await workflow.run_pipeline(
                customer_name=enhanced_input["customer_name"],
                transcript=enhanced_input["content"]
            )
        else:
            # Strategic/general business input workflow
            st.info("💡 Processing as strategic business input...")
            result = await execute_strategic_workflow(enhanced_input, agent_routing, workflow)
        
        return result
        
    except Exception as e:
        raise Exception(f"Dynamic workflow execution failed: {str(e)}")


async def execute_strategic_workflow(enhanced_input: Dict[str, Any],
                                   agent_routing: Dict[str, Any],
                                   workflow) -> Dict[str, Any]:
    """Execute workflow for strategic/non-transcript inputs"""
    
    try:
        # Skip Conversa if not a transcript
        if not agent_routing.get("conversa", {}).get("execute", False):
            st.info("⏭️ Skipping transcript analysis (not a transcript)")
            
            # Start with Conny for business consulting
            # This would be a modified workflow that starts with strategic analysis
            result = await workflow.run_pipeline(
                customer_name=enhanced_input["customer_name"],
                transcript=f"Strategic Input Analysis:\n\n{enhanced_input['content']}"
            )
        else:
            # Run full workflow
            result = await workflow.run_pipeline(
                customer_name=enhanced_input["customer_name"],
                transcript=enhanced_input["content"]
            )
        
        return result
        
    except Exception as e:
        raise Exception(f"Strategic workflow execution failed: {str(e)}")


async def execute_mock_smart_pipeline(smart_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute mock pipeline when AI components are not available"""
    
    # Simulate processing steps
    progress_steps = [
        ("🔍 Analyzing input content", 0.1),
        ("🎯 Creating routing plan", 0.2), 
        ("📚 Searching similar proposals", 0.3),
        ("🤖 Executing optimized workflow", 0.5),
        ("📄 Generating documents", 0.8),
        ("✅ Finalizing results", 1.0)
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step_name, progress in progress_steps:
        status_text.info(step_name)
        progress_bar.progress(progress)
        await asyncio.sleep(0.5)  # Simulate processing time
    
    # Create mock routing analysis
    mock_routing_info = create_mock_routing_analysis(smart_input)
    
    # Create mock proposal context
    mock_proposal_context = create_mock_proposal_context(mock_routing_info)
    
    # Create mock pipeline results
    mock_pipeline_result = create_mock_pipeline_result(smart_input, mock_routing_info)
    
    status_text.success("🎉 Smart pipeline execution complete!")
    
    return {
        "status": "success",
        "routing_info": mock_routing_info,
        "proposal_context": mock_proposal_context,
        "pipeline_result": mock_pipeline_result,
        "timestamp": datetime.now().isoformat(),
        "mode": "mock"
    }


def create_mock_routing_analysis(smart_input: Dict[str, Any]) -> Dict[str, Any]:
    """Create mock routing analysis for demonstration"""
    
    content = smart_input.get("content", "")
    content_hint = smart_input.get("content_type_hint", "Auto-detect")
    
    # Simple content analysis
    is_transcript = any(pattern in content.lower() for pattern in [
        "customer:", "client:", "rep:", "q:", "a:", "interviewer:"
    ])
    
    # Detect industry hints
    industry_keywords = {
        "technology": ["software", "platform", "api", "cloud", "digital"],
        "manufacturing": ["production", "factory", "supply chain", "inventory"],
        "healthcare": ["patient", "medical", "clinical", "hospital"],
        "finance": ["banking", "financial", "trading", "payment"],
        "retail": ["store", "customer experience", "e-commerce", "shopping"]
    }
    
    detected_industry = "unknown"
    for industry, keywords in industry_keywords.items():
        if any(keyword in content.lower() for keyword in keywords):
            detected_industry = industry
            break
    
    return {
        "timestamp": datetime.now().isoformat(),
        "analysis_confidence": "high",
        "transcript": is_transcript,
        "content_type": content_hint.lower().replace(" ", "_"),
        "industry": detected_industry,
        "solution_types": ["automation", "optimization"],
        "urgency_level": "medium",
        "company_size": "unknown",
        "agent_routing": {
            "conversa": {"execute": is_transcript, "priority": 1},
            "conny": {"execute": True, "priority": 2},
            "prody": {"execute": True, "priority": 3},
            "preston": {"execute": False, "priority": 4},
            "marketing": {"execute": True, "priority": 5}
        },
        "rag_search_terms": ["business solution", "process optimization", detected_industry],
        "stakeholders": {
            "decision_makers": ["VP", "Director"],
            "influencers": ["Manager", "Team Lead"]
        }
    }


def create_mock_proposal_context(routing_info: Dict[str, Any]) -> Dict[str, Any]:
    """Create mock proposal context for demonstration"""
    
    industry = routing_info.get("industry", "unknown")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "similar_proposals": [
            {
                "customer_name": "Acme Corp",
                "industry": industry,
                "relevance_score": 0.85,
                "summary": f"Digital transformation project in {industry} sector",
                "outcome": "won"
            },
            {
                "customer_name": "TechStart Inc",
                "industry": "technology", 
                "relevance_score": 0.72,
                "summary": "Process automation and optimization initiative",
                "outcome": "won"
            }
        ],
        "reusable_content": [
            {
                "type": "successful_approach",
                "content": "Phased implementation with pilot program",
                "source": "Similar won proposal"
            }
        ],
        "lessons_learned": [
            "Executive sponsorship is critical for success",
            "Start with pilot program to demonstrate value",
            "Focus on quick wins in first 90 days"
        ],
        "implementation_patterns": [
            "3-phase approach: Assessment → Pilot → Scale",
            "Change management integrated throughout",
            "Weekly stakeholder check-ins"
        ]
    }


def create_mock_pipeline_result(smart_input: Dict[str, Any], routing_info: Dict[str, Any]) -> Dict[str, Any]:
    """Create mock pipeline result for demonstration"""
    
    customer_name = smart_input.get("customer_name", "Business Input")
    industry = routing_info.get("industry", "technology")
    
    return {
        "status": "success",
        "customer_name": customer_name,
        "result": {
            "final_package": {
                "document_artifacts": [
                    {
                        "type": "problem_overview",
                        "title": f"{customer_name} - Problem Analysis",
                        "content": f"# Problem Overview for {customer_name}\n\nBased on the {industry} industry analysis..."
                    },
                    {
                        "type": "solution_approach",
                        "title": f"{customer_name} - Recommended Solution",
                        "content": f"# Solution Approach for {customer_name}\n\nRecommended implementation strategy..."
                    },
                    {
                        "type": "investment_proposal",
                        "title": f"{customer_name} - Investment Proposal",
                        "content": f"# Investment Proposal for {customer_name}\n\nROI analysis and budget recommendations..."
                    },
                    {
                        "type": "sales_presentation",
                        "title": f"{customer_name} - Executive Presentation",
                        "content": f"# Executive Presentation for {customer_name}\n\nStrategic overview and value proposition..."
                    }
                ],
                "summary": {
                    "total_documents": 4,
                    "processing_time": "2.5 minutes",
                    "agents_executed": ["Input Router", "Conny", "ProDy", "Marketing"],
                    "rag_matches": 2
                }
            }
        },
        "completed_at": datetime.now().isoformat()
    }


def render_pipeline_results(results: Dict[str, Any]):
    """Render the results of the smart pipeline execution"""
    
    if results.get("status") != "success":
        st.error(f"❌ Pipeline failed: {results.get('error', 'Unknown error')}")
        return
    
    # Show routing analysis
    with st.expander("🔍 Input Analysis Results", expanded=True):
        routing_info = results.get("routing_info", {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Content Type", routing_info.get("content_type", "Unknown"))
            st.metric("Industry", routing_info.get("industry", "Unknown").title())
        
        with col2:
            st.metric("Transcript", "Yes" if routing_info.get("transcript") else "No")
            st.metric("Urgency", routing_info.get("urgency_level", "Unknown").title())
        
        with col3:
            solution_types = routing_info.get("solution_types", [])
            st.metric("Solution Types", f"{len(solution_types)} identified")
            agents_count = sum(1 for agent_info in routing_info.get("agent_routing", {}).values() 
                             if agent_info.get("execute", False))
            st.metric("Agents Executed", agents_count)
    
    # Show similar proposals found
    with st.expander("📚 Similar Past Proposals", expanded=False):
        proposal_context = results.get("proposal_context", {})
        similar_proposals = proposal_context.get("similar_proposals", [])
        
        if similar_proposals:
            for i, proposal in enumerate(similar_proposals):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{proposal.get('customer_name', 'Unknown')}**")
                    st.markdown(proposal.get("summary", "No summary available"))
                
                with col2:
                    score = proposal.get("relevance_score", 0)
                    st.metric("Relevance", f"{score:.0%}")
                
                with col3:
                    outcome = proposal.get("outcome", "unknown")
                    outcome_color = "🟢" if outcome == "won" else "🔴" if outcome == "lost" else "⚪"
                    st.markdown(f"{outcome_color} {outcome.title()}")
        else:
            st.info("No similar past proposals found")
    
    # Show generated documents
    with st.expander("📄 Generated Documents", expanded=True):
        pipeline_result = results.get("pipeline_result", {})
        final_package = pipeline_result.get("result", {}).get("final_package", {})
        documents = final_package.get("document_artifacts", [])
        
        if documents:
            for doc in documents:
                with st.container():
                    st.markdown(f"### 📋 {doc.get('title', 'Document')}")
                    
                    # Document preview
                    with st.expander("Preview", expanded=False):
                        st.markdown(doc.get("content", "No content available")[:500] + "...")
                    
                    # Download button
                    if st.button(f"📥 Download {doc.get('type', 'document')}", key=f"download_{doc.get('type')}"):
                        st.download_button(
                            label="Download as Markdown",
                            data=doc.get("content", ""),
                            file_name=f"{doc.get('type', 'document')}.md",
                            mime="text/markdown"
                        )
        else:
            st.info("No documents generated")
    
    # Show summary metrics
    summary = final_package.get("summary", {})
    if summary:
        st.markdown("### 📊 Pipeline Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Documents Generated", summary.get("total_documents", 0))
        
        with col2:
            st.metric("Processing Time", summary.get("processing_time", "Unknown"))
        
        with col3:
            agents_executed = summary.get("agents_executed", [])
            st.metric("Agents Used", len(agents_executed))
        
        with col4:
            st.metric("Similar Proposals", summary.get("rag_matches", 0))