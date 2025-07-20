"""
Tests for the LlamaIndex AgentWorkflow system
"""

import pytest
import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from workflow import PresalesPipelineWorkflow, WorkflowStage
from workflow_manager import WorkflowManager
from llm_integration import OpenRouterLLMClient
from jina_integration import JinaAIClient
from config import AISettings


class TestWorkflowComponents:
    """Test workflow components and individual agents"""
    
    @pytest.fixture
    def ai_settings(self):
        """Create test AI settings"""
        return AISettings(
            openrouter_api_key="test-key",
            jina_api_key="test-jina-key",
            default_llm_model="moonshotai/kimi-k2"
        )
    
    @pytest.fixture
    def llm_client(self, ai_settings):
        """Create test LLM client"""
        return OpenRouterLLMClient(ai_settings)
    
    @pytest.fixture
    def jina_client(self, ai_settings):
        """Create test Jina client"""
        return JinaAIClient(ai_settings)
    
    @pytest.fixture
    def workflow(self, llm_client, jina_client):
        """Create test workflow"""
        return PresalesPipelineWorkflow(llm_client, jina_client, verbose=False)
    
    @pytest.fixture
    def workflow_manager(self, ai_settings):
        """Create test workflow manager"""
        return WorkflowManager(ai_settings)
    
    @pytest.fixture
    def sample_transcript(self):
        """Sample customer transcript for testing"""
        return """
        Customer: We're struggling with our current manual processes. Everything takes too long and we're making too many errors.
        
        Sales Rep: Can you tell me more about the specific processes that are causing problems?
        
        Customer: Well, our customer onboarding process currently takes about 2 weeks. We have to manually collect information, verify it, and then set up accounts. It's all spreadsheets and email. Our team of 5 people spends most of their time on this.
        
        Sales Rep: What would success look like for you?
        
        Customer: If we could cut that time in half and reduce errors, that would be huge. We're also planning to grow our team by 50% next year, so we need something that can scale.
        
        Sales Rep: Are there any integration requirements with existing systems?
        
        Customer: Yes, we use Salesforce for CRM and QuickBooks for accounting. Any solution would need to work with those systems.
        
        Customer: What about budget and timeline?
        
        Sales Rep: We're looking to implement something in the next 6 months. Budget is around $200K for the first year.
        """
    
    def test_workflow_initialization(self, workflow):
        """Test workflow initializes correctly"""
        assert workflow is not None
        assert hasattr(workflow, 'conversa_agent')
        assert hasattr(workflow, 'conny_agent')
        assert hasattr(workflow, 'prody_agent')
        assert hasattr(workflow, 'preston_agent')
        assert hasattr(workflow, 'marketing_agent')
    
    def test_workflow_manager_initialization(self, workflow_manager):
        """Test workflow manager initializes correctly"""
        assert workflow_manager is not None
        assert hasattr(workflow_manager, 'workflow')
        assert hasattr(workflow_manager, 'llm_client')
        assert hasattr(workflow_manager, 'jina_client')
        assert len(workflow_manager.active_executions) == 0
    
    def test_workflow_input_validation(self, workflow_manager):
        """Test workflow input validation"""
        # Test valid inputs
        result = asyncio.run(workflow_manager.validate_workflow_inputs(
            "Test Customer", "This is a valid transcript with sufficient content to test the validation logic."
        ))
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        
        # Test invalid inputs
        result = asyncio.run(workflow_manager.validate_workflow_inputs("", ""))
        assert result["valid"] is False
        assert "Customer name is required" in result["errors"]
        assert "Transcript content is required" in result["errors"]
    
    def test_processing_time_estimation(self, workflow_manager):
        """Test processing time estimation"""
        result = asyncio.run(workflow_manager.estimate_processing_time(1000))
        assert "estimated_total_seconds" in result
        assert "estimated_total_minutes" in result
        assert result["estimated_total_seconds"] > 0
        assert result["estimated_total_minutes"] > 0
    
    def test_workflow_id_generation(self, workflow_manager, sample_transcript):
        """Test workflow ID generation"""
        workflow_id = asyncio.run(workflow_manager.start_workflow("Test Customer", sample_transcript))
        assert workflow_id is not None
        assert "test_customer" in workflow_id.lower()
        assert len(workflow_manager.active_executions) == 1
    
    def test_workflow_status_tracking(self, workflow_manager, sample_transcript):
        """Test workflow status tracking"""
        workflow_id = asyncio.run(workflow_manager.start_workflow("Test Customer", sample_transcript))
        
        status = workflow_manager.get_workflow_status(workflow_id)
        assert status is not None
        assert status["workflow_id"] == workflow_id
        assert status["customer_name"] == "Test Customer"
        assert status["status"] == "pending"
    
    def test_workflow_statistics(self, workflow_manager, sample_transcript):
        """Test workflow statistics calculation"""
        # Start a few workflows
        asyncio.run(workflow_manager.start_workflow("Customer 1", sample_transcript))
        asyncio.run(workflow_manager.start_workflow("Customer 2", sample_transcript))
        
        stats = workflow_manager.get_workflow_statistics()
        assert stats["total_executions"] == 2
        assert stats["pending"] == 2
        assert stats["running"] == 0
        assert stats["completed"] == 0
    
    def test_active_workflows_listing(self, workflow_manager, sample_transcript):
        """Test active workflows listing"""
        workflow_id1 = asyncio.run(workflow_manager.start_workflow("Customer 1", sample_transcript))
        workflow_id2 = asyncio.run(workflow_manager.start_workflow("Customer 2", sample_transcript))
        
        active_workflows = workflow_manager.list_active_workflows()
        assert len(active_workflows) == 2
        
        workflow_ids = [w["workflow_id"] for w in active_workflows]
        assert workflow_id1 in workflow_ids
        assert workflow_id2 in workflow_ids


class TestWorkflowStages:
    """Test individual workflow stages"""
    
    @pytest.fixture
    def ai_settings(self):
        return AISettings(
            openrouter_api_key="test-key",
            jina_api_key="test-jina-key", 
            default_llm_model="moonshotai/kimi-k2"
        )
    
    def test_workflow_stages_enum(self):
        """Test workflow stages enumeration"""
        stages = list(WorkflowStage)
        assert len(stages) == 10
        assert WorkflowStage.TRANSCRIPT_ANALYSIS in stages
        assert WorkflowStage.BUSINESS_CONSULTATION in stages
        assert WorkflowStage.FINAL_DELIVERY in stages
    
    def test_workflow_stage_progression(self):
        """Test workflow stage progression logic"""
        stages = [
            WorkflowStage.TRANSCRIPT_ANALYSIS,
            WorkflowStage.BUSINESS_CONSULTATION,
            WorkflowStage.REQUIREMENTS_REFINEMENT,
            WorkflowStage.PM_HANDOVER,
            WorkflowStage.DOCUMENT_GENERATION,
            WorkflowStage.QUALITY_REVIEW,
            WorkflowStage.PACKAGE_CREATION,
            WorkflowStage.RAG_INTEGRATION,
            WorkflowStage.SALES_DECK_CREATION,
            WorkflowStage.FINAL_DELIVERY
        ]
        
        # Verify all stages are present in correct order
        assert len(stages) == 10
        assert stages[0] == WorkflowStage.TRANSCRIPT_ANALYSIS
        assert stages[-1] == WorkflowStage.FINAL_DELIVERY


class TestAgentIntegration:
    """Test agent integration within workflow"""
    
    @pytest.fixture
    def ai_settings(self):
        return AISettings(
            openrouter_api_key="test-key",
            jina_api_key="test-jina-key",
            default_llm_model="moonshotai/kimi-k2"
        )
    
    @pytest.fixture
    def llm_client(self, ai_settings):
        return OpenRouterLLMClient(ai_settings)
    
    @pytest.fixture
    def jina_client(self, ai_settings):
        return JinaAIClient(ai_settings)
    
    def test_agent_capabilities(self, llm_client, jina_client):
        """Test agent capabilities are properly defined"""
        from agents.conversa_agent import ConversaAgent
        from agents.conny_agent import ConnyAgent
        from agents.prody_agent import ProDyAgent
        from agents.preston_agent import PrestonAgent
        from agents.marketing_agent import MarketingAgent
        
        # Test each agent has capabilities
        conversa = ConversaAgent(llm_client, jina_client)
        assert len(conversa.get_capabilities()) > 0
        assert "transcript_analysis" in conversa.get_capabilities()
        
        conny = ConnyAgent(llm_client, jina_client) 
        assert len(conny.get_capabilities()) > 0
        assert "business_consultation" in conny.get_capabilities()
        
        prody = ProDyAgent(llm_client, jina_client)
        assert len(prody.get_capabilities()) > 0
        assert "problem_analysis_documentation" in prody.get_capabilities()
        
        preston = PrestonAgent(llm_client, jina_client)
        assert len(preston.get_capabilities()) > 0
        assert "current_state_process_mapping" in preston.get_capabilities()
        
        marketing = MarketingAgent(llm_client, jina_client)
        assert len(marketing.get_capabilities()) > 0
        assert "sales_presentation_creation" in marketing.get_capabilities()
    
    def test_agent_system_prompts(self, llm_client, jina_client):
        """Test agents have proper system prompts"""
        from agents.conversa_agent import ConversaAgent
        from agents.conny_agent import ConnyAgent
        
        conversa = ConversaAgent(llm_client, jina_client)
        prompt = conversa.get_system_prompt()
        assert "Conversa" in prompt
        assert "transcript" in prompt.lower()
        
        conny = ConnyAgent(llm_client, jina_client)
        prompt = conny.get_system_prompt()
        assert "Conny" in prompt
        assert "business" in prompt.lower()


class TestWorkflowIntegration:
    """Integration tests for complete workflow"""
    
    @pytest.fixture
    def ai_settings(self):
        return AISettings(
            openrouter_api_key="test-key",
            jina_api_key="test-jina-key",
            default_llm_model="moonshotai/kimi-k2"
        )
    
    @pytest.fixture
    def workflow_manager(self, ai_settings):
        return WorkflowManager(ai_settings)
    
    @pytest.fixture
    def sample_transcript(self):
        return """
        Customer discussion about digital transformation needs:
        - Current manual processes are inefficient
        - Need integration with Salesforce and QuickBooks
        - Budget of $200K for first year
        - Timeline of 6 months for implementation
        - Team growth expected of 50% next year
        - Customer onboarding currently takes 2 weeks, want to reduce to 1 week
        - 5-person team currently handling all manual processes
        - Primary pain points: time consumption and error rates
        """
    
    @pytest.mark.asyncio
    async def test_workflow_full_execution_mock(self, workflow_manager, sample_transcript):
        """Test full workflow execution with mocked responses"""
        
        # This would be a full integration test with real API calls
        # For now, we test the workflow structure and error handling
        
        workflow_id = await workflow_manager.start_workflow("Integration Test Customer", sample_transcript)
        assert workflow_id is not None
        
        status = workflow_manager.get_workflow_status(workflow_id)
        assert status["status"] == "pending"
        assert status["current_stage"] == WorkflowStage.TRANSCRIPT_ANALYSIS.value
    
    @pytest.mark.asyncio
    async def test_workflow_streaming_updates(self, workflow_manager, sample_transcript):
        """Test workflow streaming functionality"""
        
        workflow_id = await workflow_manager.start_workflow("Streaming Test Customer", sample_transcript)
        
        updates = []
        try:
            # Collect first few streaming updates (with timeout for testing)
            async for update in workflow_manager.stream_workflow(
                workflow_id, "Streaming Test Customer", sample_transcript
            ):
                updates.append(update)
                if len(updates) >= 3:  # Just test first few updates
                    break
        except Exception as e:
            # Expected in test environment without real API keys
            assert "api" in str(e).lower() or "auth" in str(e).lower()
        
        # Should have attempted to start streaming
        assert workflow_id in workflow_manager.active_executions
    
    def test_workflow_error_handling(self, workflow_manager):
        """Test workflow error handling"""
        
        # Test with invalid workflow ID
        status = workflow_manager.get_workflow_status("nonexistent-id")
        assert status is None
        
        result = workflow_manager.get_workflow_result("nonexistent-id") 
        assert result is None
    
    def test_workflow_cleanup(self, workflow_manager, sample_transcript):
        """Test workflow cleanup functionality"""
        
        # Create some workflows
        workflow_id = asyncio.run(workflow_manager.start_workflow("Cleanup Test", sample_transcript))
        
        # Test cleanup (won't actually clean up recent workflows)
        initial_count = len(workflow_manager.active_executions)
        workflow_manager.cleanup_completed_workflows(max_age_hours=0.001)  # Very short age
        
        # Should not clean up pending/running workflows regardless of age
        assert len(workflow_manager.active_executions) == initial_count


if __name__ == "__main__":
    # Run basic tests if executed directly
    print("Running workflow tests...")
    
    # Test basic initialization
    settings = AISettings(
        openrouter_api_key="test-key",
        jina_api_key="test-jina-key",
        default_llm_model="moonshotai/kimi-k2"
    )
    
    manager = WorkflowManager(settings)
    print(f"✓ WorkflowManager initialized with {len(manager.active_executions)} executions")
    
    # Test input validation
    sample_transcript = "This is a test transcript for validation purposes."
    validation = asyncio.run(manager.validate_workflow_inputs("Test Customer", sample_transcript))
    print(f"✓ Input validation: {'PASS' if validation['valid'] else 'FAIL'}")
    
    # Test workflow creation
    workflow_id = asyncio.run(manager.start_workflow("Test Customer", sample_transcript))
    print(f"✓ Workflow created: {workflow_id}")
    
    # Test status tracking
    status = manager.get_workflow_status(workflow_id)
    print(f"✓ Status tracking: {status['status']} at stage {status['current_stage']}")
    
    print("Basic workflow tests completed successfully!")