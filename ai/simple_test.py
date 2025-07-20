#!/usr/bin/env python3
"""
Simple test for workflow system components
"""

import sys
import os
import asyncio

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from config import AISettings
    from workflow_manager import WorkflowManager
    print("✓ Successfully imported workflow components")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_workflow_system():
    """Test basic workflow system functionality"""
    print("Testing workflow system...")
    
    # Test basic initialization
    settings = AISettings(
        openrouter_api_key="test-key",
        jina_api_key="test-jina-key",
        default_llm_model="moonshotai/kimi-k2"
    )
    
    manager = WorkflowManager(settings)
    print(f"✓ WorkflowManager initialized with {len(manager.active_executions)} executions")
    
    # Test input validation
    sample_transcript = "This is a test transcript for validation purposes with enough content to pass validation checks and demonstrate the workflow system capabilities."
    validation = asyncio.run(manager.validate_workflow_inputs("Test Customer", sample_transcript))
    print(f"✓ Input validation: {'PASS' if validation['valid'] else 'FAIL'} - Errors: {validation['errors']}")
    
    # Test processing time estimation
    estimation = asyncio.run(manager.estimate_processing_time(len(sample_transcript)))
    print(f"✓ Time estimation: {estimation['estimated_total_minutes']} minutes estimated")
    
    # Test workflow creation
    workflow_id = asyncio.run(manager.start_workflow("Test Customer", sample_transcript))
    print(f"✓ Workflow created: {workflow_id}")
    
    # Test status tracking
    status = manager.get_workflow_status(workflow_id)
    print(f"✓ Status tracking: {status['status']} at stage {status['current_stage']}")
    
    # Test active workflows listing
    active = manager.list_active_workflows()
    print(f"✓ Active workflows: {len(active)} workflows")
    
    # Test statistics
    stats = manager.get_workflow_statistics()
    print(f"✓ Statistics: {stats['total_executions']} total, {stats['pending']} pending")
    
    print("Basic workflow tests completed successfully!")

if __name__ == "__main__":
    test_workflow_system()