Feature: Complete Proposal Generation Workflow
  As a sales representative
  I want to transform customer transcripts into complete proposal packages
  So that I can reduce proposal cycle-time by 30% and deliver professional materials

  Background:
    Given the LlamaIndex Pre-sales Pipeline application is running
    And I can access the application at http://localhost:8501
    And I have valid API keys configured in the system

  @critical @smoke-test
  Scenario: End-to-End Customer Transcript to Proposal Package
    Given I am a sales rep with a customer discovery call transcript
    And I need to create a complete proposal package for "Acme Manufacturing Corp"
    
    When I navigate to the Input page
    And I enter the following customer transcript:
      """
      Customer Discovery Call - Acme Manufacturing Corp
      
      Participants: 
      - Sarah Johnson (CTO, Acme Manufacturing)
      - Mike Davis (VP Operations, Acme Manufacturing)  
      - John Smith (Sales Rep, Our Company)

      Sarah: "Our biggest pain point is managing our supply chain data. We have systems that don't talk to each other - our inventory management, production planning, and supplier portals are all separate. This creates a lot of manual work and delays."

      Mike: "The lack of real-time visibility is killing us. When we have a production issue, it takes hours to figure out the ripple effect on our delivery commitments. We need something that gives us a unified view."

      Sarah: "We want real-time dashboards that show our entire supply chain status. Production capacity, inventory levels, supplier delivery status, all in one place."

      Mike: "The goal is to reduce our production planning cycle from 24 hours to 2 hours, and eliminate the manual reporting completely."

      Sarah: "We have budget approved for up to $500K for this project. We need to have something operational by Q2 2025 because that's when our new product line launches."
      """
    And I set the customer name to "Acme Manufacturing Corp"
    And I set the content type hint to "Customer Transcript"
    And I click "Save & Continue to Analysis"

    Then I should be redirected to the Analysis page
    And I should see a success message confirming the input was saved
    And I should see the input summary showing "Acme Manufacturing Corp" as the customer
    And I should see that transcript detection shows "Yes"

    When I click "Analyze Content with AI"
    And I wait for the analysis to complete

    Then I should see the content analysis results
    And I should see "manufacturing" detected as an industry
    And I should see "integration" and "analytics" as solution indicators
    And I should see budget indicators showing "$500K"
    And I should see timeline mentions including "Q2 2025"
    And I should see that Conversa agent is recommended (due to transcript)
    And I should see that Conny, ProDy, and Marketing agents are recommended

    When I click "Start AI Processing"

    Then I should be redirected to the Processing page
    And I should see the agent sequence visualization
    And I should see processing controls available

    When I click "Demo Mode (Fast)" to simulate AI processing

    Then I should see real-time progress updates
    And I should see each agent processing in sequence (Conversa → Conny → ProDy → Marketing)
    And I should see the processing progress reach 100%
    And I should see a success message that pipeline execution completed

    When I click "View Results"

    Then I should be redirected to the Review page
    And I should see generated documents available for review
    And I should see documents including:
      | Document Type | Expected |
      | Problem Overview | ✓ |
      | Solution Architecture | ✓ |
      | Investment Proposal | ✓ |
      | Sales Deck | ✓ |

    When I select the "Problem Overview" document
    And I click on it to edit

    Then I should see the document content in the editor
    And I should see markdown formatting
    And I should be able to make edits to the content

    When I modify the document title to "Acme Manufacturing - Problem Analysis"
    And I add a new section "## Risk Assessment" to the document
    And I click "Save Changes"

    Then I should see a success message that changes were saved
    And I should see the updated title reflected

    When I click "Mark Review Complete"

    Then I should see a completion success message
    And I should see balloons animation celebrating completion

    When I click "Export Final Package"

    Then I should see a download button for the complete proposal package
    And the filename should include "Acme_Manufacturing_Corp" and today's date
    And I should be able to download a ZIP file containing all documents

    When I navigate to the Projects page

    Then I should see my completed project listed
    And I should see "Acme Manufacturing Corp" as the customer name
    And I should see the status as "Completed"
    And I should see the artifact count showing multiple documents
    And I should see today's date as the creation date

  @business-value
  Scenario: Demonstrate 30% Cycle-Time Reduction
    Given I have timed the traditional manual proposal process at 8 hours
    And I am using the AI-powered pipeline for the first time
    
    When I complete the entire workflow from transcript input to final package
    
    Then the total time should be under 15 minutes (including manual review)
    And I should achieve more than 30% time reduction compared to manual process
    And the quality of generated documents should be professional and comprehensive

  @customer-ready
  Scenario: Generated Proposal Package is Customer-Ready
    Given I have completed the proposal generation workflow
    And I have downloaded the final package
    
    When I extract and review the ZIP package contents
    
    Then I should find the following customer-ready documents:
      | Document | Customer-Ready | Professional Quality |
      | Problem Overview | ✓ | ✓ |
      | Solution Architecture | ✓ | ✓ |
      | Investment Proposal | ✓ | ✓ |
      | Executive Sales Deck | ✓ | ✓ |
      | Implementation Roadmap | ✓ | ✓ |
    And each document should be formatted in markdown
    And each document should contain specific customer information (Acme Manufacturing Corp)
    And each document should reference the customer's specific challenges and requirements
    And the investment proposal should include the customer's budget range ($500K)

  @error-handling
  Scenario: Handle Missing Prerequisites Gracefully
    Given I navigate directly to the Processing page without completing prerequisites
    
    Then I should see an error message about missing prerequisites
    And I should see helpful buttons to navigate back to Input or Analysis pages
    And the application should not crash or show technical errors
    And I should be guided back to the correct workflow sequence

  @data-persistence 
  Scenario: Project Data is Properly Persisted
    Given I have created a complete proposal project
    And I close the browser completely
    
    When I reopen the application
    And I navigate to the Projects page
    
    Then I should still see my saved project
    And I should be able to click "Resume" to continue working on it
    And all my document edits should be preserved
    And the project status should be accurately reflected