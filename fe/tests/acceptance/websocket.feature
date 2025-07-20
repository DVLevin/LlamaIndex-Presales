Feature: WebSocket Real-time Communication
  As a sales representative
  I want real-time communication with AI agents
  So that I can see their work progress and results immediately

  Background:
    Given I am on the presales application at http://localhost:5173
    And I am on the "Chat" tab

  Scenario: WebSocket connection establishment
    Given the backend WebSocket server is running on ws://localhost:8000
    When I load the chat interface
    Then the connection status should change from "Connecting..." to "Connected" within 5 seconds
    And the connection indicator should be green
    And the message input should be enabled
    And the placeholder should change to "Ask me about prospects, research, or proposals..."

  Scenario: WebSocket connection failure
    Given the backend WebSocket server is NOT running
    When I load the chat interface
    Then the connection status should show "Connecting..." initially
    And after 5-10 seconds it should change to "Connection Error" or "Disconnected"
    And the connection indicator should be red or gray
    And the message input should remain disabled
    And the placeholder should remain "Connecting..."

  Scenario: Automatic reconnection attempts
    Given I have a connected WebSocket
    When the backend server goes down
    Then the connection status should change to "Disconnected"
    And the system should automatically attempt to reconnect
    And I should see the status change back to "Connecting..." periodically
    When the backend server comes back online
    Then the connection should be re-established automatically
    And the status should change to "Connected"

  Scenario: Sending messages via WebSocket
    Given I have a connected WebSocket
    When I type "Research Acme Corporation" and send
    Then my message should appear in the chat immediately
    And the WebSocket should send a message to the backend
    And the message should include:
      - type: "user_message"
      - content: "Research Acme Corporation" 
      - conversationId: the current conversation ID
      - timestamp: current time

  Scenario: Receiving agent messages
    Given I have a connected WebSocket
    And I have sent a message that triggers agent work
    When the backend sends an agent response
    Then I should see a new message appear in the chat
    And the message should show:
      - Agent icon (Bot icon)
      - Agent name as sender
      - Message content from the agent
      - Timestamp of when received
      - Gray background color

  Scenario: Receiving agent status updates
    Given I have a connected WebSocket
    When the backend sends agent status updates
    Then the streaming indicator should appear when status is "working" or "thinking"
    And the streaming indicator should show animated dots
    And the streaming indicator should disappear when status is "completed" or "idle"

  Scenario: Receiving tool call notifications
    Given I have a connected WebSocket
    When an agent makes a tool call
    Then I should receive a WebSocket event with type "tool_call"
    And the event should include:
      - Tool name
      - Tool parameters
      - Tool status (pending/running/completed/error)
      - Agent ID making the call

  Scenario: Receiving agent handoff notifications
    Given I have a connected WebSocket
    When one agent hands off to another
    Then I should receive a WebSocket event with type "handoff"
    And the event should include:
      - fromAgent: source agent name
      - toAgent: target agent name
      - reason: handoff reason
      - context: handoff context data

  Scenario: Error message handling
    Given I have a connected WebSocket
    When the backend sends an error event
    Then I should see a system message in the chat
    And the message should have:
      - System icon (AlertCircle)
      - "System" as sender
      - Yellow background
      - Error description in the content
      - Current timestamp

  Scenario: WebSocket message parsing errors
    Given I have a connected WebSocket
    When the backend sends malformed JSON
    Then the application should not crash
    And I should see a console error message
    And the chat should continue working normally
    And no message should be added to the chat

  Scenario: Connection status visual feedback
    Given I am watching the connection status indicator
    When the status is "Connecting..."
    Then I should see a spinning loader icon
    And yellow/amber background color
    When the status is "Connected"
    Then I should see a WiFi icon
    And green background color
    When the status is "Disconnected"
    Then I should see a WiFi-off icon
    And gray background color
    When the status is "Connection Error"
    Then I should see an alert/error icon
    And red background color

  Scenario: Message queuing during disconnection
    Given I have a disconnected WebSocket
    When I try to send a message
    Then the message should appear in my chat as sent
    And I should see a warning that delivery failed
    And the message should be marked as undelivered (if implemented)
    When the connection is re-established
    Then previously failed messages should be automatically resent (if implemented)

  Scenario: WebSocket URL formation
    Given I am connecting to WebSocket
    Then the WebSocket URL should be: ws://localhost:8000/ws/demo-conversation
    And it should include the conversation ID in the path
    And it should use the correct protocol (ws:// for development)

  Scenario: Connection timeout handling
    Given I am attempting to connect to WebSocket
    When the connection takes longer than expected
    Then the system should not wait indefinitely
    And after a reasonable timeout period (10-30 seconds)
    The status should change to "Connection Error"
    And I should be able to manually retry the connection

  Scenario: Clean connection shutdown
    Given I have a connected WebSocket
    When I navigate away from the page
    Then the WebSocket connection should be cleanly closed
    And the connection should send a close frame with code 1000
    When I return to the page
    Then a new connection should be established automatically

  Scenario: Multiple conversation support
    Given I have multiple browser tabs open with different conversations
    When each tab connects to WebSocket
    Then each should have a unique connection with different conversation IDs
    And messages should only appear in the correct conversation tab
    And agent status updates should be conversation-specific