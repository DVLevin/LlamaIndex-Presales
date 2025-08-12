#!/usr/bin/env python3
"""
Quick System Validation Test
Programmatically tests core functionality without browser automation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import our system components
from streamlit_app.storage.project_manager import ProjectManager
from streamlit_app.pages.page_navigation import PageNavigator
from streamlit_app.config import AppConfig, validate_api_keys


class TestSystemCore(unittest.TestCase):
    """Test core system functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_db_path = "/tmp/test_projects.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        self.project_manager = ProjectManager(self.test_db_path)
        self.navigator = PageNavigator()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_project_manager_creation_and_storage(self):
        """Test project creation, storage, and retrieval"""
        print("\n🧪 Testing Project Manager Core Functionality...")
        
        # Create a test project
        project_id = self.project_manager.create_project(
            name="Test Manufacturing Project",
            customer_name="Acme Corp",
            input_content="Test customer transcript about manufacturing challenges...",
            input_metadata={"content_type": "transcript", "urgency": "high"}
        )
        
        self.assertIsNotNone(project_id)
        self.assertTrue(project_id.startswith("proj_"))
        print(f"✅ Project created with ID: {project_id}")
        
        # Save some artifacts
        artifact_id = self.project_manager.save_artifact(
            project_id=project_id,
            artifact_type="problem_overview",
            title="Problem Analysis",
            content="# Problem Overview\n\nAcme Corp faces integration challenges...",
            format="markdown",
            agent_generated="prody"
        )
        
        self.assertIsNotNone(artifact_id)
        print(f"✅ Artifact saved with ID: {artifact_id}")
        
        # Retrieve the project
        project = self.project_manager.get_project(project_id)
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "Test Manufacturing Project")
        self.assertEqual(project.customer_name, "Acme Corp")
        self.assertEqual(len(project.artifacts), 1)
        
        artifact = project.artifacts[0]
        self.assertEqual(artifact.artifact_type, "problem_overview")
        self.assertEqual(artifact.title, "Problem Analysis")
        self.assertTrue(artifact.content.startswith("# Problem Overview"))
        
        print("✅ Project retrieval and artifact validation successful")
        
        # Test project listing
        projects = self.project_manager.list_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["name"], "Test Manufacturing Project")
        
        print("✅ Project listing functionality working")
        
        # Test search functionality
        search_results = self.project_manager.search_projects("manufacturing")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]["name"], "Test Manufacturing Project")
        
        print("✅ Search functionality working")
        
        # Test export functionality
        zip_data = self.project_manager.export_project_to_zip(project_id)
        self.assertIsNotNone(zip_data)
        self.assertGreater(len(zip_data), 0)
        
        print("✅ Export functionality working")
    
    def test_page_navigation_system(self):
        """Test page navigation and progress tracking"""
        print("\n🧪 Testing Page Navigation System...")
        
        # Test page configurations
        self.assertEqual(len(self.navigator.pages), 5)
        
        required_pages = ["input", "analysis", "processing", "review", "projects"]
        for page in required_pages:
            self.assertIn(page, self.navigator.pages)
        
        print("✅ All required pages configured")
        
        # Test accessibility logic
        input_config = self.navigator.pages["input"]
        analysis_config = self.navigator.pages["analysis"]
        processing_config = self.navigator.pages["processing"]
        
        # Input should always be accessible
        self.assertTrue(self.navigator._is_page_accessible(input_config))
        
        # Analysis should require input (we'll mock session state)
        with patch('streamlit.session_state', {"smart_input": None}):
            self.assertFalse(self.navigator._is_page_accessible(analysis_config))
        
        with patch('streamlit.session_state', {"smart_input": {"content": "test"}}):
            self.assertTrue(self.navigator._is_page_accessible(analysis_config))
        
        print("✅ Page accessibility logic working")
    
    def test_config_validation(self):
        """Test configuration and API key validation"""
        print("\n🧪 Testing Configuration System...")
        
        # Test config creation
        config = AppConfig()
        self.assertIsInstance(config.available_models, dict)
        self.assertIsInstance(config.agent_models, dict)
        
        print("✅ Configuration object creation successful")
        
        # Test API key validation
        test_config = AppConfig(
            openrouter_api_key="sk-or-v1-test123",
            jina_api_key="jina_test123456789012345"
        )
        
        validation_result = validate_api_keys(test_config)
        self.assertIsInstance(validation_result, dict)
        self.assertIn("openrouter", validation_result)
        self.assertIn("jina", validation_result)
        
        print("✅ API key validation working")
    
    def test_mock_ai_processing(self):
        """Test mock AI processing pipeline simulation"""
        print("\n🧪 Testing Mock AI Processing...")
        
        # Simulate the smart input processing
        smart_input = {
            "content": """Customer Discovery Call - Acme Manufacturing Corp
            
            Sarah: "Our biggest pain point is managing our supply chain data..."
            Mike: "We need real-time dashboards for our supply chain status..."
            Sarah: "We have budget approved for up to $500K for this project..."
            """,
            "customer_name": "Acme Manufacturing Corp",
            "content_type_hint": "Customer Transcript"
        }
        
        # Import analysis function
        from streamlit_app.components.smart_input import generate_preview_analysis
        
        analysis_results = generate_preview_analysis(smart_input["content"])
        
        # Validate analysis results
        self.assertIsInstance(analysis_results, dict)
        self.assertIn("is_transcript", analysis_results)
        self.assertIn("industry_hints", analysis_results)
        self.assertIn("solution_indicators", analysis_results)
        self.assertIn("budget_indicators", analysis_results)
        
        # Check specific detections
        self.assertTrue(analysis_results["is_transcript"])  # Should detect conversation format
        self.assertIn("manufacturing", analysis_results["industry_hints"])
        self.assertTrue(len(analysis_results["budget_indicators"]) > 0)  # Should find $500K
        
        print("✅ Content analysis working correctly")
        print(f"   - Transcript detected: {analysis_results['is_transcript']}")
        print(f"   - Industries found: {analysis_results['industry_hints']}")
        print(f"   - Budget indicators: {analysis_results['budget_indicators']}")
        print(f"   - Solution types: {analysis_results['solution_indicators']}")
    
    def test_end_to_end_simulation(self):
        """Test complete end-to-end workflow simulation"""
        print("\n🧪 Testing End-to-End Workflow Simulation...")
        
        # Step 1: Input processing
        smart_input = {
            "content": "Customer transcript about retail integration challenges...",
            "customer_name": "Global Retail Solutions",
            "content_type_hint": "Customer Transcript",
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 2: Project creation
        project_id = self.project_manager.create_project(
            name=f"{smart_input['customer_name']} - AI Proposal",
            customer_name=smart_input["customer_name"],
            input_content=smart_input["content"],
            input_metadata=smart_input
        )
        
        # Step 3: Mock document generation (what AI agents would produce)
        mock_documents = {
            "problem_overview": "# Problem Overview\n\nGlobal Retail Solutions faces integration challenges...",
            "solution_architecture": "# Solution Architecture\n\nRecommended cloud-based integration platform...",
            "investment_proposal": "# Investment Proposal\n\n$750K investment for comprehensive digital transformation...",
            "sales_deck": "# Executive Summary\n\nTransform retail operations with AI-powered integration..."
        }
        
        # Step 4: Save all artifacts
        artifact_ids = []
        for doc_type, content in mock_documents.items():
            artifact_id = self.project_manager.save_artifact(
                project_id=project_id,
                artifact_type=doc_type,
                title=doc_type.replace("_", " ").title(),
                content=content,
                format="markdown",
                agent_generated="ai_pipeline"
            )
            artifact_ids.append(artifact_id)
        
        # Step 5: Update project completion
        self.project_manager.update_project_progress(
            project_id=project_id,
            progress_step="completed",
            status="completed",
            agents_completed=["conversa", "conny", "prody", "marketing"]
        )
        
        # Step 6: Validate complete project
        final_project = self.project_manager.get_project(project_id)
        
        self.assertEqual(final_project.status, "completed")
        self.assertEqual(final_project.progress_step, "completed")
        self.assertEqual(len(final_project.artifacts), 4)
        self.assertEqual(final_project.agents_completed, ["conversa", "conny", "prody", "marketing"])
        
        # Step 7: Test export
        zip_data = self.project_manager.export_project_to_zip(project_id)
        self.assertIsNotNone(zip_data)
        self.assertGreater(len(zip_data), 1000)  # Should be substantial ZIP file
        
        print("✅ Complete end-to-end workflow simulation successful")
        print(f"   - Project ID: {project_id}")
        print(f"   - Artifacts generated: {len(final_project.artifacts)}")
        print(f"   - Agents completed: {len(final_project.agents_completed)}")
        print(f"   - Export size: {len(zip_data):,} bytes")
    
    def run_all_tests(self):
        """Run all tests and return summary"""
        print("=" * 80)
        print("🚀 SYSTEM VALIDATION TEST SUITE")
        print("=" * 80)
        
        test_methods = [
            self.test_project_manager_creation_and_storage,
            self.test_page_navigation_system,
            self.test_config_validation,
            self.test_mock_ai_processing,
            self.test_end_to_end_simulation
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
            except Exception as e:
                print(f"❌ {test_method.__name__} FAILED: {str(e)}")
                failed += 1
        
        print("\n" + "=" * 80)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 80)
        print(f"✅ PASSED: {passed}/{len(test_methods)} tests")
        print(f"❌ FAILED: {failed}/{len(test_methods)} tests")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! System is ready for user acceptance testing.")
            print("\n🔗 Manual Testing Instructions:")
            print("1. Open browser to: http://localhost:8501")
            print("2. Click '🎭 Demo Mode' to load sample data")
            print("3. Follow complete workflow through all 5 pages")
            print("4. Verify professional documents are generated")
            print("5. Confirm project persistence and export functionality")
        else:
            print(f"\n⚠️  {failed} tests failed. Review errors above before manual testing.")
        
        return failed == 0


if __name__ == "__main__":
    tester = TestSystemCore()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)