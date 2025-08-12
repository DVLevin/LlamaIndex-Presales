Feature: Project Management and Data Persistence
  As a sales professional managing multiple opportunities
  I want to save, search, and manage my proposal projects
  So that I can reuse past work and maintain organized proposal history

  Background:
    Given the LlamaIndex Pre-sales Pipeline application is running
    And I can access the application at http://localhost:8501

  @project-storage @critical
  Scenario: Create and Save Complete Project with All Artifacts
    Given I have completed a full proposal workflow for "TechStart Solutions"
    And I have generated 5 documents (problem overview, solution architecture, investment proposal, sales deck, roadmap)
    And I have made manual edits to 2 of the documents
    
    When I navigate to the Projects page
    
    Then I should see my project listed with the following details:
      | Field | Expected Value |
      | Customer Name | TechStart Solutions |
      | Status | Completed |
      | Progress Step | Completed |
      | Artifact Count | 5 |
      | Created Date | Today's date |
      | Updated Date | Today's date |
    
    When I click "👁️ View" on the project
    
    Then I should see the detailed project view
    And I should see all 5 artifacts listed with their details
    And I should see the original input content preserved
    And I should see the AI processing history (which agents ran)
    And I should see version information for edited documents

    When I click "📦 Export Project" 
    
    Then I should be able to download a ZIP file
    And the ZIP should contain:
      | File | Present |
      | project_info.json | ✓ |
      | original_input.txt | ✓ |
      | artifacts/problem_overview.md | ✓ |
      | artifacts/solution_architecture.md | ✓ |
      | artifacts/investment_proposal.md | ✓ |
      | artifacts/sales_deck.md | ✓ |
      | artifacts/implementation_roadmap.md | ✓ |

  @search-functionality
  Scenario: Search Projects by Content and Customer
    Given I have created multiple projects:
      | Customer | Keywords | Status |
      | Acme Manufacturing | supply chain, integration | Completed |
      | TechStart Solutions | cloud platform, APIs | In Progress |
      | Global Retail Corp | e-commerce, analytics | Draft |
    
    When I navigate to the Projects page
    And I enter "manufacturing" in the search box
    
    Then I should see only the "Acme Manufacturing" project in results
    And I should see a message indicating "Found 1 projects matching 'manufacturing'"
    
    When I clear the search and enter "cloud"
    
    Then I should see only the "TechStart Solutions" project
    And the match should highlight that it was found in document content
    
    When I clear the search and select "In Progress" from the status filter
    
    Then I should see only projects with "In Progress" status
    And completed and draft projects should be hidden
    
    When I clear all filters
    
    Then I should see all projects listed again
    And they should be sorted by most recent first

  @project-resume
  Scenario: Resume Work on Existing Project
    Given I have a saved project "Enterprise Integration" that was stopped at the Analysis phase
    And the project contains original input content and analysis results
    
    When I navigate to the Projects page
    And I find the "Enterprise Integration" project
    And I click "✏️ Resume"
    
    Then I should be redirected to the Analysis page
    And I should see my original input content loaded in session
    And I should see my previous analysis results displayed
    And the progress tracking should show Input ✅ and Analysis ✅
    And I should be able to continue to the Processing page

    When I complete the remaining workflow steps
    
    Then the project should be updated with new artifacts
    And the status should change from "In Progress" to "Completed"
    And all new documents should be added to the existing project
    And the version history should track all changes

  @project-templates
  Scenario: Use Past Project as Template for New Opportunity
    Given I have a completed project "Manufacturing Integration - Alpha Corp"
    And it contains high-quality documents suitable for reuse
    
    When I navigate to the Projects page
    And I click "📋 Copy" on the Alpha Corp project
    
    Then I should see a success message about creating a copy
    And I should see a new project listed as "Manufacturing Integration - Alpha Corp (Copy)"
    And the new project should have status "Draft"
    
    When I click "✏️ Resume" on the copied project
    
    Then I should see all the original documents loaded for editing
    And I should be able to modify customer-specific information
    And I should be able to update the customer name to a new prospect
    And the original project should remain unchanged

  @version-history
  Scenario: Track Document Version History and Rollback Changes
    Given I have a project with a "Problem Overview" document
    And I make the following edits over time:
      | Version | Change | Editor |
      | 1 | Original AI-generated content | ProDy Agent |
      | 2 | Added customer-specific details | User Edit |
      | 3 | Updated budget information | User Edit |
      | 4 | Added risk assessment section | User Edit |
    
    When I navigate to the Review page for this document
    And I click on the History tab
    
    Then I should see all 4 versions listed with timestamps
    And I should see which changes were made by AI vs manual editing
    And I should see the creation and update timestamps for each version
    
    When I click "Restore Version 2" 
    
    Then I should see a confirmation that version 2 was restored
    And the document editor should show the content from version 2
    And I should be able to make new edits from that restored point
    And the version history should continue from version 2 (creating version 5)

  @project-statistics
  Scenario: View Project Library Statistics and Insights
    Given I have multiple projects in my library with various statuses and dates
    
    When I navigate to the Projects page
    
    Then I should see comprehensive statistics including:
      | Metric | Displayed |
      | Total Projects | ✓ |
      | Completed Projects | ✓ |
      | In Progress Projects | ✓ |
      | Total Documents Generated | ✓ |
      | Recent Activity (this week) | ✓ |
      | Completion Rate Percentage | ✓ |
    
    And I should see visual progress indicators for completion rates
    And I should see activity status (Active vs All current)

  @data-export
  Scenario: Export Project Data for External Use
    Given I have a completed project with all artifacts
    
    When I export the project as a ZIP package
    And I extract the ZIP file
    
    Then the project_info.json should contain:
      | Field | Present |
      | Project ID | ✓ |
      | Customer Name | ✓ |
      | Creation Date | ✓ |
      | Status | ✓ |
      | Agents Completed | ✓ |
    
    And each artifact file should be properly formatted markdown
    And each artifact should contain customer-specific information
    And the file names should be descriptive and organized
    And the content should be ready for external presentation

  @error-recovery
  Scenario: Handle Project Operations Gracefully
    Given I have projects in my library
    
    When I attempt to delete a project
    
    Then I should see a confirmation dialog
    And I should have to explicitly confirm the deletion
    And the deletion should not happen accidentally
    
    When I confirm the deletion
    
    Then the project should be permanently removed
    And I should see a success message
    And the project should no longer appear in the list
    
    When I try to access a project that has been deleted
    
    Then I should see an appropriate error message
    And I should not see technical stack traces
    And I should be redirected back to the project list

  @data-persistence
  Scenario: Verify Long-term Data Persistence
    Given I create a project and close the application completely
    And I wait some time and restart the application
    
    When I navigate to the Projects page
    
    Then my saved project should still be available
    And all project metadata should be intact
    And all artifacts should be preserved
    And I should be able to resume work exactly where I left off
    
    When I create multiple projects over time
    
    Then the SQLite database should grow appropriately
    And search performance should remain good
    And data integrity should be maintained
    And no data corruption should occur