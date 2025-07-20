Feature: Chat Interface
  As a sales representative
  I want to interact with AI agents through a chat interface
  So that I can get help with presales activities in real-time

  Background:
    Given I am on the presales application at http://localhost:5173
    And the "Chat" tab is selected by default

  Scenario: Initial chat interface display
    Given I am on the chat interface
    Then I should see the header "Presales AI Assistant"
    And I should see a connection status indicator in the header
    And I should see an empty message area with text "Start a conversation"
    And I should see helper text "Send a message to begin working with the AI agents"
    And I should see a message input field at the bottom
    And I should see a send button with a paper airplane icon

  Scenario: Connection status indicator
    Given I am on the chat interface
    Then I should see a connection status indicator
    And the status should be one of: "Connecting...", "Connected", "Disconnected", or "Connection Error"
    And the status should have an appropriate colored background (yellow for connecting, green for connected, gray for disconnected, red for error)

  Scenario: Sending a message without backend
    Given I am on the chat interface
    And the backend is not running
    When I type "Hello, test message" in the message input
    And I click the send button
    Then I should see my message appear in the chat with "You" as the sender
    And I should see the current timestamp on my message
    And I should see a blue background for my message
    And the message input field should be cleared
    And the connection status should show "Disconnected" or "Connection Error"

  Scenario: Message input behavior
    Given I am on the chat interface
    When I click on the message input field
    Then the input field should be focused
    When I type a multi-line message with Shift+Enter
    Then the textarea should expand to show multiple lines
    When I press Enter without Shift
    Then the message should be sent (if connected) or queued
    And the textarea should return to single line height

  Scenario: Message input validation
    Given I am on the chat interface
    When the message input is empty
    Then the send button should be disabled
    When I type only spaces "   " in the message input
    Then the send button should still be disabled
    When I type a valid message "Test message"
    Then the send button should be enabled

  Scenario: Placeholder text based on connection status
    Given I am on the chat interface
    When the connection status is "Disconnected"
    Then the input placeholder should be "Connecting..."
    And the input field should be disabled
    When the connection status is "Connected"
    Then the input placeholder should be "Ask me about prospects, research, or proposals..."
    And the input field should be enabled

  Scenario: Message display formatting
    Given I have sent several messages
    Then each message should display:
      - An icon (User icon for my messages, Bot icon for agent messages)
      - A sender label ("You" for user, agent name for agents)
      - A timestamp in the format HH:MM:SS
      - The message content with proper text wrapping
      - Appropriate background colors (blue for user, gray for agents)

  Scenario: Chat scrolling behavior
    Given I have many messages in the chat
    When new messages are added
    Then the chat should automatically scroll to the bottom
    And I should always see the latest message
    When I manually scroll up to read older messages
    And a new message arrives
    Then the chat should scroll back to the bottom

  Scenario: Agent streaming indicator
    Given I am connected to the backend
    When an agent starts working on my request
    Then I should see a "Agent is working..." indicator
    And I should see three animated dots
    And the dots should pulse with a slight delay between them
    When the agent finishes working
    Then the streaming indicator should disappear

  Scenario: System messages
    Given I am using the chat interface
    When a system error occurs
    Then I should see a system message with a warning icon
    And the message should have a yellow background
    And the sender should be labeled "System"
    And the message content should describe the error

  Scenario: Message metadata display
    Given I receive a message with metadata
    When I look at the message
    Then I should see a "Metadata" collapsible section
    When I click on "Metadata"
    Then I should see the raw JSON metadata in a formatted code block
    And the metadata should be syntax highlighted

  Scenario: Responsive design - Mobile view
    Given I am on the chat interface
    When I resize my browser to mobile width (< 768px)
    Then the header should remain at the top
    And the message list should take up most of the screen
    And the input area should remain at the bottom
    And all elements should be touch-friendly
    And text should remain readable without horizontal scrolling

  Scenario: Accessibility - Keyboard navigation
    Given I am on the chat interface
    When I press Tab repeatedly
    Then I should be able to navigate to:
      - The message input field
      - The send button
      - Any clickable elements in the interface
    And each focused element should have a visible focus indicator
    When I press Enter on the send button
    Then it should send the message
    When I press Escape while focused on any element
    Then the element should lose focus

  Scenario: Error recovery after connection loss
    Given I am connected and chatting
    When the connection is lost
    Then the status should change to "Disconnected" 
    And the input field should be disabled
    And I should see appropriate visual feedback
    When I try to send a message while disconnected
    Then I should see a warning that the message cannot be sent
    When the connection is restored
    Then the status should change to "Connected"
    And the input field should be re-enabled
    And I should be able to send messages normally