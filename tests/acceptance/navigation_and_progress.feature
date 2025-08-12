Feature: Multi-Page Navigation and Progress Tracking
  As a user of the proposal generation system
  I want intuitive navigation with clear progress indication
  So that I always know where I am in the process and what to do next

  Background:
    Given the LlamaIndex Pre-sales Pipeline application is running
    And I can access the application at http://localhost:8501

  @navigation @ux
  Scenario: Multi-Page Navigation Flow with Progress Tracking
    Given I am on the application homepage
    
    Then I should see a sidebar with navigation options
    And I should see the following pages available:
      | Page | Icon | Status |
      | Smart Input | 💭 | Accessible |
      | Content Analysis | 🤖 | Locked |
      | AI Processing | ⚡ | Locked |
      | Document Review | 📋 | Locked |
      | Project Library | 📚 | Accessible |
    And I should see progress indicators showing 0/4 steps completed
    And I should see "Smart Input" highlighted as the current/next step

    When I click on the locked "Content Analysis" page
    
    Then I should remain on the current page (cannot navigate to locked page)
    And the "Content Analysis" page should still show as locked
    
    When I click on "Smart Input" in the sidebar
    
    Then I should navigate to the Input page
    And I should see the page title "💭 Smart Business Input"
    And I should see input options for text, file upload, and templates

    When I enter some business content in the text area
    And I set a customer name
    And I click "Save & Continue to Analysis"
    
    Then I should see the "Smart Input" page marked as completed (✅) in the sidebar
    And I should see the "Content Analysis" page become accessible (unlocked)
    And I should be automatically redirected to the Analysis page
    And the progress should show 1/4 steps completed

    When I complete the content analysis
    And I click "Start AI Processing"
    
    Then I should see the "Content Analysis" page marked as completed
    And I should see the "AI Processing" page become accessible
    And I should be redirected to the Processing page
    And the progress should show 2/4 steps completed

    When I complete the AI processing
    And I click "View Results"
    
    Then I should see the "AI Processing" page marked as completed
    And I should see the "Document Review" page become accessible
    And I should be redirected to the Review page
    And the progress should show 3/4 steps completed

    When I click "Mark Review Complete"
    
    Then I should see all 4 steps marked as completed
    And the progress should show 4/4 steps completed
    And I should see celebration indicators (balloons or similar)

  @quick-actions
  Scenario: Sidebar Quick Actions Work Correctly
    Given I am on any page of the application
    
    When I look at the sidebar
    
    Then I should see a "Quick Actions" section
    And I should see a "🆕 New Project" button
    
    When I click "🆕 New Project"
    
    Then I should see a confirmation message about starting a new project
    And all progress should be reset to 0/4 steps
    And I should be redirected to the Input page
    And any previous session data should be cleared

    When I have some progress made (input completed)
    
    Then I should see a "▶️ Continue Process" button in the sidebar
    
    When I click "▶️ Continue Process"
    
    Then I should be taken to the next incomplete step in the workflow
    And it should skip any already completed steps

  @demo-mode
  Scenario: Demo Mode Provides Complete Sample Workflow
    Given I am on the Input page with no content entered
    
    When I click "🎭 Demo Mode" in the sidebar
    
    Then I should see sample content automatically loaded
    And I should see a success message about demo data being loaded
    And I should see balloons or celebration animation
    And the input page should be marked as completed
    And I should be redirected to the Analysis page with sample analysis results

    When I continue through the demo workflow
    
    Then each page should have realistic sample data
    And I should be able to complete the entire flow with demo data
    And all generated documents should contain realistic sample content
    And the demo should demonstrate the full value proposition

  @breadcrumbs @context
  Scenario: User Always Knows Current Context and Next Steps
    Given I am on any page in the application
    
    Then I should see clear indication of:
      | Element | Visibility |
      | Current page title | Clearly displayed |
      | Step description | What this step accomplishes |
      | Progress indicator | How far through the process |
      | Next action | What to do next |
      | Current project info | If working on a saved project |
    
    When I am working on a saved project
    
    Then I should see the project name displayed in the sidebar
    And I should see "🎯 Current Project: [Project Name]" information
    
    When I have prerequisites missing for a page
    
    Then I should see clear guidance about what's needed
    And I should see helpful buttons to complete the prerequisites
    And I should not see confusing or technical error messages

  @responsive-design
  Scenario: Navigation Works on Different Screen Sizes
    Given I am using the application
    
    When I resize the browser window to tablet size
    
    Then the sidebar should remain functional
    And all navigation elements should be accessible
    And the page content should adapt appropriately
    
    When I use the application on a mobile-sized screen
    
    Then the navigation should still be usable
    And critical functionality should remain accessible
    And the user experience should remain intuitive

  @accessibility
  Scenario: Navigation is Accessible and User-Friendly
    Given I am a new user encountering the application for the first time
    
    Then the navigation should be self-explanatory
    And each page should have clear instructions
    And I should be guided toward the correct next action
    And error messages should be helpful, not technical
    
    When I make a mistake (like trying to skip steps)
    
    Then I should receive helpful guidance
    And I should be redirected to the correct workflow step
    And the application should help me get back on track

  @state-management
  Scenario: Session State is Properly Managed Across Pages
    Given I have entered content on the Input page
    And I have completed analysis on the Analysis page
    
    When I navigate back to the Input page
    
    Then my previously entered content should still be visible
    And I should be able to modify it if needed
    
    When I navigate forward again to Analysis
    
    Then my analysis results should still be available
    And I should not need to re-run the analysis
    
    When I complete the entire workflow and start a new project
    
    Then all previous session data should be properly cleared
    And I should start with a clean slate
    And the new project should not be contaminated with old data