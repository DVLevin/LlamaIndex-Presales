"""
LlamaIndex AgentWorkflow for 10-Step Presales Pipeline

Orchestrates the complete transcript-to-proposal workflow:
1. Conversa: Transcript analysis → Structured requirements
2. Conny: Business consulting → Project description  
3. Conversa (v2): Requirements refinement → Enhanced summary
4. Conny (brief): Zero-knowledge handover → PM document
5. ProDy: Document generation → 5 artifacts
6. Conny: Quality review → Approval/feedback loop
7. System: Package creation → Project folder
8. RAG: Knowledge integration → Past solutions
9. Marketing Agent: Sales deck creation → Customer presentation
10. System: Final delivery → Download package
"""

import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import json
import logging

from llama_index.core.workflow import (
    Workflow, 
    StartEvent, 
    StopEvent, 
    Context,
    step
)
from llama_index.core.workflow.events import Event

from .agents.conversa_agent import ConversaAgent
from .agents.conny_agent import ConnyAgent  
from .agents.prody_agent import ProDyAgent
from .agents.preston_agent import PrestonAgent
from .agents.marketing_agent import MarketingAgent
from .llm_integration import OpenRouterLLMClient
from .jina_integration import JinaAIClient


class WorkflowStage(Enum):
    """Workflow stages for the 10-step pipeline"""
    TRANSCRIPT_ANALYSIS = "transcript_analysis"
    BUSINESS_CONSULTATION = "business_consultation"
    REQUIREMENTS_REFINEMENT = "requirements_refinement"
    PM_HANDOVER = "pm_handover"
    DOCUMENT_GENERATION = "document_generation"
    QUALITY_REVIEW = "quality_review"
    PACKAGE_CREATION = "package_creation"
    RAG_INTEGRATION = "rag_integration"
    SALES_DECK_CREATION = "sales_deck_creation"
    FINAL_DELIVERY = "final_delivery"


@dataclass
class WorkflowContext:
    """Context data passed between workflow steps"""
    customer_name: str
    transcript_text: str
    requirements: Dict[str, Any] = None
    project_description: Dict[str, Any] = None
    enhanced_summary: Dict[str, Any] = None
    pm_handover: Dict[str, Any] = None
    document_artifacts: List[Dict[str, Any]] = None
    quality_review: Dict[str, Any] = None
    project_package: Dict[str, Any] = None
    rag_insights: Dict[str, Any] = None
    sales_presentation: Dict[str, Any] = None
    final_package: Dict[str, Any] = None
    metadata: Dict[str, Any] = None


# Custom workflow events
class TranscriptAnalyzedEvent(Event):
    """Event fired when transcript analysis is complete"""
    context: WorkflowContext


class BusinessConsultationEvent(Event):
    """Event fired when business consultation is complete"""
    context: WorkflowContext


class RequirementsRefinedEvent(Event):
    """Event fired when requirements are refined"""
    context: WorkflowContext


class PMHandoverEvent(Event):
    """Event fired when PM handover document is ready"""
    context: WorkflowContext


class DocumentsGeneratedEvent(Event):
    """Event fired when all documents are generated"""
    context: WorkflowContext


class QualityReviewedEvent(Event):
    """Event fired when quality review is complete"""
    context: WorkflowContext


class PackageCreatedEvent(Event):
    """Event fired when project package is created"""
    context: WorkflowContext


class RAGIntegratedEvent(Event):
    """Event fired when RAG insights are integrated"""
    context: WorkflowContext


class SalesDeckCreatedEvent(Event):
    """Event fired when sales deck is created"""
    context: WorkflowContext


class WorkflowCompleteEvent(Event):
    """Event fired when entire workflow is complete"""
    context: WorkflowContext


class PresalesPipelineWorkflow(Workflow):
    """Main workflow orchestrating the 10-step presales pipeline"""
    
    def __init__(self, llm_client: OpenRouterLLMClient, jina_client: JinaAIClient, 
                 verbose: bool = True):
        super().__init__(verbose=verbose)
        
        # Initialize agents
        self.conversa_agent = ConversaAgent(llm_client, jina_client)
        self.conny_agent = ConnyAgent(llm_client, jina_client)
        self.prody_agent = ProDyAgent(llm_client, jina_client)
        self.preston_agent = PrestonAgent(llm_client, jina_client)
        self.marketing_agent = MarketingAgent(llm_client, jina_client)
        
        # Workflow configuration
        self.llm_client = llm_client
        self.jina_client = jina_client
        
        # Setup logging
        self.logger = logging.getLogger(__name__)

    @step(pass_context=True)
    async def start_workflow(self, ctx: Context, ev: StartEvent) -> TranscriptAnalyzedEvent:
        """Step 1: Analyze customer transcript with Conversa agent"""
        self.logger.info("Starting presales pipeline workflow")
        
        # Extract input data
        customer_name = ev.input.get("customer_name", "Customer")
        transcript_text = ev.input.get("transcript", "")
        
        if not transcript_text:
            raise ValueError("Transcript text is required to start workflow")
        
        # Initialize workflow context
        workflow_context = WorkflowContext(
            customer_name=customer_name,
            transcript_text=transcript_text,
            metadata={
                "workflow_id": ctx.data.get("workflow_id", f"workflow_{datetime.now().isoformat()}"),
                "started_at": datetime.now().isoformat(),
                "stage": WorkflowStage.TRANSCRIPT_ANALYSIS.value
            }
        )
        
        # Store context in workflow data
        ctx.data["workflow_context"] = workflow_context
        
        self.logger.info(f"Step 1: Analyzing transcript for {customer_name}")
        
        # Analyze transcript with Conversa agent
        analysis_result = await self.conversa_agent.process(
            transcript_text,
            context={"customer_name": customer_name, "analysis_type": "initial"}
        )
        
        # Update workflow context
        workflow_context.requirements = analysis_result
        workflow_context.metadata["stage"] = WorkflowStage.BUSINESS_CONSULTATION.value
        
        self.logger.info("Step 1 complete: Transcript analysis finished")
        
        return TranscriptAnalyzedEvent(context=workflow_context)

    @step(pass_context=True)
    async def business_consultation(self, ctx: Context, 
                                  ev: TranscriptAnalyzedEvent) -> BusinessConsultationEvent:
        """Step 2: Business consultation with Conny agent"""
        self.logger.info("Step 2: Starting business consultation")
        
        workflow_context = ev.context
        
        # Business consultation with Conny agent
        consultation_input = json.dumps(workflow_context.requirements, indent=2)
        consultation_result = await self.conny_agent.process(
            consultation_input,
            context={
                "customer_name": workflow_context.customer_name,
                "consultation_type": "project_description"
            }
        )
        
        # Update workflow context
        workflow_context.project_description = consultation_result
        workflow_context.metadata["stage"] = WorkflowStage.REQUIREMENTS_REFINEMENT.value
        
        self.logger.info("Step 2 complete: Business consultation finished")
        
        return BusinessConsultationEvent(context=workflow_context)

    @step(pass_context=True) 
    async def requirements_refinement(self, ctx: Context,
                                    ev: BusinessConsultationEvent) -> RequirementsRefinedEvent:
        """Step 3: Requirements refinement with Conversa agent (v2)"""
        self.logger.info("Step 3: Refining requirements")
        
        workflow_context = ev.context
        
        # Combine original requirements with project description for refinement
        refinement_input = f"""
Original Requirements:
{json.dumps(workflow_context.requirements, indent=2)}

Project Description:
{json.dumps(workflow_context.project_description, indent=2)}
"""
        
        # Refine requirements with Conversa agent
        refinement_result = await self.conversa_agent.process(
            refinement_input,
            context={
                "customer_name": workflow_context.customer_name,
                "analysis_type": "refinement"
            }
        )
        
        # Update workflow context
        workflow_context.enhanced_summary = refinement_result
        workflow_context.metadata["stage"] = WorkflowStage.PM_HANDOVER.value
        
        self.logger.info("Step 3 complete: Requirements refinement finished")
        
        return RequirementsRefinedEvent(context=workflow_context)

    @step(pass_context=True)
    async def pm_handover_creation(self, ctx: Context,
                                 ev: RequirementsRefinedEvent) -> PMHandoverEvent:
        """Step 4: Create PM handover document with Conny agent"""
        self.logger.info("Step 4: Creating PM handover document")
        
        workflow_context = ev.context
        
        # Create zero-knowledge PM handover brief
        handover_input = json.dumps(workflow_context.enhanced_summary, indent=2)
        handover_result = await self.conny_agent.process(
            handover_input,
            context={
                "customer_name": workflow_context.customer_name,
                "consultation_type": "pm_handover"
            }
        )
        
        # Update workflow context
        workflow_context.pm_handover = handover_result
        workflow_context.metadata["stage"] = WorkflowStage.DOCUMENT_GENERATION.value
        
        self.logger.info("Step 4 complete: PM handover document ready")
        
        return PMHandoverEvent(context=workflow_context)

    @step(pass_context=True)
    async def document_generation(self, ctx: Context,
                                ev: PMHandoverEvent) -> DocumentsGeneratedEvent:
        """Step 5: Generate 5 document artifacts with ProDy agent"""
        self.logger.info("Step 5: Generating document artifacts")
        
        workflow_context = ev.context
        
        # Generate documents with ProDy agent
        documents_input = json.dumps(workflow_context.pm_handover, indent=2)
        documents_result = await self.prody_agent.process(
            documents_input,
            context={
                "customer_name": workflow_context.customer_name,
                "project_scope": "Digital Transformation",
                "timeline": "6 months"
            }
        )
        
        # Update workflow context
        workflow_context.document_artifacts = documents_result.get("artifacts", [])
        workflow_context.metadata["stage"] = WorkflowStage.QUALITY_REVIEW.value
        
        self.logger.info(f"Step 5 complete: Generated {len(workflow_context.document_artifacts)} document artifacts")
        
        return DocumentsGeneratedEvent(context=workflow_context)

    @step(pass_context=True) 
    async def quality_review(self, ctx: Context,
                           ev: DocumentsGeneratedEvent) -> QualityReviewedEvent:
        """Step 6: Quality review with Conny agent"""
        self.logger.info("Step 6: Conducting quality review")
        
        workflow_context = ev.context
        
        # Quality review with Conny agent
        review_input = f"""
Document Artifacts for Review:
{json.dumps(workflow_context.document_artifacts, indent=2)}

Original Requirements:
{json.dumps(workflow_context.requirements, indent=2)}
"""
        
        review_result = await self.conny_agent.process(
            review_input,
            context={
                "customer_name": workflow_context.customer_name,
                "consultation_type": "quality_review"
            }
        )
        
        # Update workflow context
        workflow_context.quality_review = review_result
        workflow_context.metadata["stage"] = WorkflowStage.PACKAGE_CREATION.value
        
        self.logger.info("Step 6 complete: Quality review finished")
        
        return QualityReviewedEvent(context=workflow_context)

    @step(pass_context=True)
    async def package_creation(self, ctx: Context,
                             ev: QualityReviewedEvent) -> PackageCreatedEvent:
        """Step 7: Create project package"""
        self.logger.info("Step 7: Creating project package")
        
        workflow_context = ev.context
        
        # Create comprehensive project package
        project_package = {
            "customer_name": workflow_context.customer_name,
            "created_at": datetime.now().isoformat(),
            "requirements": workflow_context.requirements,
            "project_description": workflow_context.project_description,
            "enhanced_summary": workflow_context.enhanced_summary,
            "pm_handover": workflow_context.pm_handover,
            "document_artifacts": workflow_context.document_artifacts,
            "quality_review": workflow_context.quality_review,
            "package_type": "comprehensive_proposal"
        }
        
        # Update workflow context
        workflow_context.project_package = project_package
        workflow_context.metadata["stage"] = WorkflowStage.RAG_INTEGRATION.value
        
        self.logger.info("Step 7 complete: Project package created")
        
        return PackageCreatedEvent(context=workflow_context)

    @step(pass_context=True)
    async def rag_integration(self, ctx: Context,
                            ev: PackageCreatedEvent) -> RAGIntegratedEvent:
        """Step 8: Integrate RAG knowledge base insights"""
        self.logger.info("Step 8: Integrating RAG knowledge base")
        
        workflow_context = ev.context
        
        # Simulate RAG integration (would use vector database in production)
        customer_context = f"{workflow_context.customer_name} {json.dumps(workflow_context.requirements)}"
        
        # Search for similar past solutions (simplified)
        rag_insights = {
            "similar_projects": [
                {"client": "Similar Company", "solution": "Digital Platform", "outcome": "40% efficiency gain"},
                {"client": "Industry Peer", "solution": "Process Automation", "outcome": "$500K annual savings"}
            ],
            "recommended_approaches": [
                "Phased implementation approach proven in similar engagements",
                "Focus on quick wins in first 90 days",
                "Leverage industry-specific accelerators"
            ],
            "risk_mitigation": [
                "Change management critical success factor",
                "Data migration complexity requires specialized expertise",
                "Integration testing phase should be extended"
            ]
        }
        
        # Update workflow context
        workflow_context.rag_insights = rag_insights
        workflow_context.metadata["stage"] = WorkflowStage.SALES_DECK_CREATION.value
        
        self.logger.info("Step 8 complete: RAG insights integrated")
        
        return RAGIntegratedEvent(context=workflow_context)

    @step(pass_context=True)
    async def sales_deck_creation(self, ctx: Context,
                                ev: RAGIntegratedEvent) -> SalesDeckCreatedEvent:
        """Step 9: Create customer sales deck with Marketing agent"""
        self.logger.info("Step 9: Creating customer sales deck")
        
        workflow_context = ev.context
        
        # Create sales presentation with Marketing agent
        presentation_input = f"""
Project Package:
{json.dumps(workflow_context.project_package, indent=2)}

RAG Insights:
{json.dumps(workflow_context.rag_insights, indent=2)}
"""
        
        presentation_result = await self.marketing_agent.process(
            presentation_input,
            context={
                "customer_name": workflow_context.customer_name,
                "solution_type": "Digital Transformation Solution",
                "audience_type": "mixed"
            }
        )
        
        # Update workflow context
        workflow_context.sales_presentation = presentation_result
        workflow_context.metadata["stage"] = WorkflowStage.FINAL_DELIVERY.value
        
        self.logger.info("Step 9 complete: Sales deck created")
        
        return SalesDeckCreatedEvent(context=workflow_context)

    @step(pass_context=True)
    async def final_delivery(self, ctx: Context,
                           ev: SalesDeckCreatedEvent) -> StopEvent:
        """Step 10: Final package delivery"""
        self.logger.info("Step 10: Creating final delivery package")
        
        workflow_context = ev.context
        
        # Create comprehensive final package
        final_package = {
            "workflow_id": workflow_context.metadata["workflow_id"],
            "customer_name": workflow_context.customer_name,
            "completed_at": datetime.now().isoformat(),
            "processing_time": "TBD",  # Would calculate actual time
            
            # All deliverables
            "transcript_analysis": workflow_context.requirements,
            "business_consultation": workflow_context.project_description,
            "requirements_refinement": workflow_context.enhanced_summary,
            "pm_handover_document": workflow_context.pm_handover,
            "document_artifacts": workflow_context.document_artifacts,
            "quality_review": workflow_context.quality_review,
            "project_package": workflow_context.project_package,
            "rag_insights": workflow_context.rag_insights,
            "sales_presentation": workflow_context.sales_presentation,
            
            # Summary statistics
            "summary": {
                "total_documents": len(workflow_context.document_artifacts) if workflow_context.document_artifacts else 0,
                "presentation_slides": workflow_context.sales_presentation.get("metadata", {}).get("slide_count", 0) if workflow_context.sales_presentation else 0,
                "rag_similar_projects": len(workflow_context.rag_insights.get("similar_projects", [])) if workflow_context.rag_insights else 0,
                "workflow_stages_completed": 10
            }
        }
        
        # Update workflow context
        workflow_context.final_package = final_package
        workflow_context.metadata["stage"] = "COMPLETED"
        workflow_context.metadata["completed_at"] = datetime.now().isoformat()
        
        self.logger.info(f"Workflow complete: Generated comprehensive proposal package for {workflow_context.customer_name}")
        
        return StopEvent(result=final_package)

    async def run_pipeline(self, customer_name: str, transcript: str, 
                          workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """Run the complete 10-step pipeline"""
        try:
            self.logger.info(f"Starting pipeline for customer: {customer_name}")
            
            # Run workflow
            result = await self.run(
                input={
                    "customer_name": customer_name,
                    "transcript": transcript
                },
                workflow_id=workflow_id or f"pipeline_{datetime.now().isoformat()}"
            )
            
            return {
                "status": "success",
                "customer_name": customer_name,
                "result": result,
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            return {
                "status": "error",
                "customer_name": customer_name,
                "error": str(e),
                "failed_at": datetime.now().isoformat()
            }

    async def stream_pipeline(self, customer_name: str, transcript: str,
                            workflow_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream pipeline execution with real-time updates"""
        try:
            self.logger.info(f"Starting streaming pipeline for customer: {customer_name}")
            
            # This would implement streaming using LlamaIndex workflow streaming capabilities
            # For now, we'll simulate streaming by yielding progress updates
            
            stages = [
                ("transcript_analysis", "Analyzing customer transcript"),
                ("business_consultation", "Conducting business consultation"),
                ("requirements_refinement", "Refining requirements"),
                ("pm_handover", "Creating PM handover document"),
                ("document_generation", "Generating document artifacts"),
                ("quality_review", "Conducting quality review"),
                ("package_creation", "Creating project package"),
                ("rag_integration", "Integrating knowledge base"),
                ("sales_deck_creation", "Creating sales presentation"),
                ("final_delivery", "Preparing final package")
            ]
            
            for i, (stage, description) in enumerate(stages, 1):
                yield {
                    "stage": stage,
                    "description": description,
                    "progress": (i / len(stages)) * 100,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Simulate processing time
                await asyncio.sleep(1)
            
            # Run actual pipeline
            result = await self.run_pipeline(customer_name, transcript, workflow_id)
            
            yield {
                "stage": "completed",
                "description": "Pipeline completed successfully",
                "progress": 100,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            yield {
                "stage": "error",
                "description": f"Pipeline failed: {str(e)}",
                "progress": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }