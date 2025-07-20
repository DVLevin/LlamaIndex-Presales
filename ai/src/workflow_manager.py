"""
Workflow Manager - Integration layer between backend and LlamaIndex workflow

Manages workflow execution, state persistence, and real-time updates
"""

import asyncio
from typing import Dict, Any, Optional, AsyncGenerator, List
import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict

from .workflow import PresalesPipelineWorkflow, WorkflowStage
from .llm_integration import OpenRouterLLMClient
from .jina_integration import JinaAIClient
from .config import AISettings


@dataclass 
class WorkflowExecution:
    """Represents a workflow execution instance"""
    workflow_id: str
    customer_name: str
    status: str  # pending, running, completed, failed
    current_stage: str
    progress_percent: float
    started_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class WorkflowManager:
    """Manages workflow execution and state"""
    
    def __init__(self, ai_settings: AISettings):
        self.ai_settings = ai_settings
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI clients
        self.llm_client = OpenRouterLLMClient(ai_settings)
        self.jina_client = JinaAIClient(ai_settings)
        
        # Active workflow executions
        self.active_executions: Dict[str, WorkflowExecution] = {}
        
        # Initialize workflow
        self.workflow = PresalesPipelineWorkflow(
            self.llm_client,
            self.jina_client,
            verbose=True
        )
        
        self.logger.info("WorkflowManager initialized")

    async def start_workflow(self, customer_name: str, transcript: str,
                           workflow_id: Optional[str] = None) -> str:
        """Start a new workflow execution"""
        
        # Generate workflow ID if not provided
        if not workflow_id:
            workflow_id = f"workflow_{customer_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create workflow execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            customer_name=customer_name,
            status="pending",
            current_stage=WorkflowStage.TRANSCRIPT_ANALYSIS.value,
            progress_percent=0.0,
            started_at=datetime.now(),
            metadata={
                "transcript_length": len(transcript),
                "created_by": "workflow_manager"
            }
        )
        
        # Store execution
        self.active_executions[workflow_id] = execution
        
        self.logger.info(f"Started workflow {workflow_id} for customer {customer_name}")
        
        return workflow_id

    async def execute_workflow(self, workflow_id: str, customer_name: str, 
                             transcript: str) -> Dict[str, Any]:
        """Execute workflow synchronously"""
        
        if workflow_id not in self.active_executions:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        execution = self.active_executions[workflow_id]
        execution.status = "running"
        
        try:
            self.logger.info(f"Executing workflow {workflow_id}")
            
            # Run the pipeline
            result = await self.workflow.run_pipeline(customer_name, transcript, workflow_id)
            
            # Update execution record
            execution.status = "completed" if result["status"] == "success" else "failed"
            execution.completed_at = datetime.now()
            execution.result = result
            execution.progress_percent = 100.0
            execution.current_stage = "completed"
            
            if result["status"] == "error":
                execution.error = result.get("error", "Unknown error")
            
            self.logger.info(f"Workflow {workflow_id} completed with status: {execution.status}")
            
            return {
                "workflow_id": workflow_id,
                "status": execution.status,
                "result": execution.result,
                "execution_time": (execution.completed_at - execution.started_at).total_seconds()
            }
            
        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            
            # Update execution with error
            execution.status = "failed"
            execution.completed_at = datetime.now()
            execution.error = str(e)
            
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e)
            }

    async def stream_workflow(self, workflow_id: str, customer_name: str,
                            transcript: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute workflow with streaming updates"""
        
        if workflow_id not in self.active_executions:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        execution = self.active_executions[workflow_id]
        execution.status = "running"
        
        try:
            self.logger.info(f"Streaming workflow {workflow_id}")
            
            # Stream pipeline execution
            async for update in self.workflow.stream_pipeline(customer_name, transcript, workflow_id):
                
                # Update execution state
                execution.current_stage = update.get("stage", execution.current_stage)
                execution.progress_percent = update.get("progress", execution.progress_percent)
                
                if update.get("stage") == "completed":
                    execution.status = "completed"
                    execution.completed_at = datetime.now()
                    execution.result = update.get("result")
                elif update.get("stage") == "error":
                    execution.status = "failed"
                    execution.completed_at = datetime.now()
                    execution.error = update.get("error")
                
                # Yield update with execution info
                yield {
                    "workflow_id": workflow_id,
                    "customer_name": customer_name,
                    "execution_status": execution.status,
                    "current_stage": execution.current_stage,
                    "progress_percent": execution.progress_percent,
                    "stage_update": update,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Workflow streaming failed for {workflow_id}: {str(e)}")
            
            execution.status = "failed"
            execution.completed_at = datetime.now()
            execution.error = str(e)
            
            yield {
                "workflow_id": workflow_id,
                "execution_status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current workflow status"""
        
        if workflow_id not in self.active_executions:
            return None
        
        execution = self.active_executions[workflow_id]
        
        return {
            "workflow_id": execution.workflow_id,
            "customer_name": execution.customer_name,
            "status": execution.status,
            "current_stage": execution.current_stage,
            "progress_percent": execution.progress_percent,
            "started_at": execution.started_at.isoformat(),
            "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
            "error": execution.error,
            "metadata": execution.metadata
        }

    def get_workflow_result(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow execution result"""
        
        if workflow_id not in self.active_executions:
            return None
        
        execution = self.active_executions[workflow_id]
        
        if execution.status != "completed" or not execution.result:
            return None
        
        return execution.result

    def list_active_workflows(self) -> List[Dict[str, Any]]:
        """List all active workflow executions"""
        
        return [
            {
                "workflow_id": execution.workflow_id,
                "customer_name": execution.customer_name,
                "status": execution.status,
                "current_stage": execution.current_stage,
                "progress_percent": execution.progress_percent,
                "started_at": execution.started_at.isoformat()
            }
            for execution in self.active_executions.values()
        ]

    def cleanup_completed_workflows(self, max_age_hours: int = 24):
        """Clean up old completed workflow executions"""
        
        current_time = datetime.now()
        to_remove = []
        
        for workflow_id, execution in self.active_executions.items():
            if execution.completed_at:
                age_hours = (current_time - execution.completed_at).total_seconds() / 3600
                if age_hours > max_age_hours:
                    to_remove.append(workflow_id)
        
        for workflow_id in to_remove:
            del self.active_executions[workflow_id]
            
        if to_remove:
            self.logger.info(f"Cleaned up {len(to_remove)} completed workflows")

    async def validate_workflow_inputs(self, customer_name: str, transcript: str) -> Dict[str, Any]:
        """Validate workflow inputs before execution"""
        
        errors = []
        warnings = []
        
        # Validate customer name
        if not customer_name or len(customer_name.strip()) == 0:
            errors.append("Customer name is required")
        elif len(customer_name) > 100:
            errors.append("Customer name too long (max 100 characters)")
        
        # Validate transcript
        if not transcript or len(transcript.strip()) == 0:
            errors.append("Transcript content is required")
        elif len(transcript) < 100:
            warnings.append("Transcript seems very short (< 100 characters)")
        elif len(transcript) > 100000:
            warnings.append("Transcript is very long (> 100k characters) - processing may take extra time")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    async def estimate_processing_time(self, transcript_length: int) -> Dict[str, Any]:
        """Estimate workflow processing time based on input size"""
        
        # Base processing time per stage (in seconds)
        base_time_per_stage = 10
        
        # Additional time based on transcript length
        length_factor = min(transcript_length / 1000, 5)  # Max 5x multiplier
        
        estimated_time_per_stage = base_time_per_stage * (1 + length_factor * 0.2)
        total_estimated_time = estimated_time_per_stage * 10  # 10 stages
        
        return {
            "estimated_total_seconds": int(total_estimated_time),
            "estimated_total_minutes": int(total_estimated_time / 60),
            "estimated_time_per_stage": int(estimated_time_per_stage),
            "factors": {
                "transcript_length": transcript_length,
                "length_factor": length_factor,
                "base_time": base_time_per_stage
            }
        }

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get overall workflow statistics"""
        
        total_executions = len(self.active_executions)
        completed = len([e for e in self.active_executions.values() if e.status == "completed"])
        failed = len([e for e in self.active_executions.values() if e.status == "failed"])
        running = len([e for e in self.active_executions.values() if e.status == "running"])
        pending = len([e for e in self.active_executions.values() if e.status == "pending"])
        
        return {
            "total_executions": total_executions,
            "completed": completed,
            "failed": failed,
            "running": running,
            "pending": pending,
            "success_rate": (completed / total_executions * 100) if total_executions > 0 else 0,
            "active_count": running + pending
        }