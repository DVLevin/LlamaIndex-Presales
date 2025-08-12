Feature: Document Editing and Review Interface
  As a sales professional reviewing AI-generated proposals
  I want to edit, customize, and finalize documents with professional quality
  So that I can deliver personalized, high-quality proposals to customers

  Background:
    Given the LlamaIndex Pre-sales Pipeline application is running
    And I have completed the AI processing phase
    And I have generated documents available for review

  @document-editing @critical
  Scenario: Edit Individual Documents with Markdown Support
    Given I am on the Review page
    And I can see multiple generated documents available
    
    When I click on the "Problem Overview" document card
    
    Then I should see the document selected with a highlight or indicator
    And I should see the document title and word count displayed
    
    When I view the document editor
    
    Then I should see tabs for "✏️ Edit", "👁️ Preview", and "🕐 History"
    And I should see the Edit tab is active by default
    And I should see the document content loaded in a text editor
    And I should see the document title in an editable field

    When I modify the document title to "Acme Corp - Comprehensive Problem Analysis"
    And I add the following content to the document:
      """
      ## Executive Summary
      This analysis identifies critical operational inefficiencies at Acme Manufacturing that are costing approximately $2M annually in lost productivity.

      ## Risk Assessment
      Without addressing these integration challenges, Acme faces:
      - 15% annual growth in manual processing overhead
      - Increased competitive disadvantage in time-to-market
      - Potential supply chain disruptions during peak seasons
      """
    And I click "💾 Save Changes"
    
    Then I should see a success message "✅ Saved changes to 'Acme Corp - Comprehensive Problem Analysis'!"
    And the document should show as saved with the new title
    And I should see an info message that changes are saved

  @markdown-preview
  Scenario: Preview Markdown Formatting in Real-Time
    Given I am editing a document with markdown content
    And I have added formatted content including headers, lists, and bold text
    
    When I click on the "👁️ Preview" tab
    
    Then I should see the markdown rendered with proper formatting:
      | Element | Rendered Correctly |
      | Headers (# ## ###) | ✓ |
      | Bold text (**text**) | ✓ |
      | Lists (- item) | ✓ |
      | Line breaks | ✓ |
    
    And the preview should look professional and well-formatted
    And I should see export options at the bottom of the preview

    When I click "📄 Download Markdown"
    
    Then I should be able to download the document as a .md file
    And the downloaded file should contain my edited content
    And the file name should match the document title

  @version-tracking
  Scenario: Track Document Edit History and Versions
    Given I am editing a "Investment Proposal" document
    And I make multiple changes over time:
      | Edit | Description |
      | 1 | Update budget from $300K to $500K |
      | 2 | Add ROI calculation section |
      | 3 | Include implementation timeline |
      | 4 | Add risk mitigation strategies |
    
    When I click on the "🕐 History" tab after each edit
    
    Then I should see version history growing with each save
    And I should see timestamps for each version
    And I should see which changes were made by "user_edited" vs AI agents
    
    When I select version 2 from the history
    
    Then I should see a preview of the document at that point in time
    And I should see a "Restore Version 2" button
    
    When I click "Restore Version 2"
    
    Then I should see a success message about restoration
    And the editor should load the content from version 2
    And I should be able to continue editing from that point
    And the version number should increment appropriately

  @document-types
  Scenario: Edit Different Types of Generated Documents
    Given I have the following documents generated:
      | Document Type | Expected Content |
      | Problem Overview | Business challenges and pain points |
      | Solution Architecture | Technical approach and systems |
      | Investment Proposal | Budget, ROI, and financial justification |
      | Sales Deck | Executive summary and value proposition |
      | Implementation Roadmap | Project phases and timelines |
    
    When I edit each document type
    
    Then each should have appropriate content structure for its purpose
    And the Problem Overview should focus on customer challenges
    And the Solution Architecture should include technical details
    And the Investment Proposal should have financial information
    And the Sales Deck should be customer-facing and persuasive
    And the Implementation Roadmap should have clear phases and dates

    When I customize each document for "Global Manufacturing Corp"
    
    Then I should be able to:
      | Action | Possible |
      | Change customer name throughout | ✓ |
      | Update specific pain points | ✓ |
      | Modify budget figures | ✓ |
      | Adjust timelines | ✓ |
      | Add company-specific details | ✓ |
    And all changes should be saved independently for each document

  @ai-enhancement
  Scenario: AI Document Enhancement Feature (Placeholder)
    Given I am editing a document that could be improved
    
    When I click "🤖 AI Enhance"
    
    Then I should see an explanation of what AI enhancement would do
    And I should see suggested improvements specific to the document type
    And I should see a placeholder for future AI enhancement integration
    
    When I click "🚀 Apply AI Enhancement"
    
    Then I should see a simulated enhancement being applied
    And the enhanced content should appear in the editor
    And I should be able to review and further edit the enhanced content
    And the enhancement should be tracked as a version change

  @document-export
  Scenario: Export Individual Documents in Various Formats
    Given I have completed editing a document
    And I am in the Preview tab
    
    When I look at the export options
    
    Then I should see multiple export formats available:
      | Format | Available |
      | Download Markdown | ✓ |
      | Export to PDF | Planned |
      | Copy to Clipboard | Planned |
    
    When I click "📄 Download Markdown"
    
    Then I should receive a properly formatted .md file
    And the filename should include the document type and title
    And the content should be exactly as shown in the preview

  @document-validation
  Scenario: Validate Document Quality and Completeness
    Given I have edited multiple documents
    
    When I review each document
    
    Then each document should:
      | Quality Check | Met |
      | Contains customer-specific information | ✓ |
      | Has professional formatting | ✓ |
      | Is free of placeholder text | ✓ |
      | Includes relevant business details | ✓ |
      | Has appropriate length for its purpose | ✓ |
    
    And the Problem Overview should be 800-1200 words
    And the Investment Proposal should include specific budget figures
    And the Sales Deck should be concise and persuasive
    And all documents should reference the same customer and opportunity

  @concurrent-editing
  Scenario: Handle Multiple Document Editing Sessions
    Given I am editing the "Problem Overview" document
    And I make changes but don't save them immediately
    
    When I switch to editing the "Solution Architecture" document
    
    Then I should see a warning about unsaved changes
    Or the system should auto-save my changes appropriately
    And I should not lose any of my work
    
    When I return to the "Problem Overview" document
    
    Then my previous unsaved changes should still be available
    And I should be able to continue editing where I left off
    And the editing experience should be seamless across documents

  @error-handling
  Scenario: Handle Document Editing Errors Gracefully
    Given I am editing a document
    
    When I encounter an error (like temporary network issues)
    
    Then I should see a user-friendly error message
    And I should not lose my unsaved changes
    And I should be able to retry the save operation
    And the application should not crash or become unusable
    
    When I accidentally close the browser tab while editing
    And I reopen the application
    
    Then I should be able to resume editing
    And my recent changes should be preserved (if auto-saved)
    Or I should be warned about potential data loss