Feature: Application Navigation
  As a sales representative
  I want to easily navigate between different parts of the application
  So that I can efficiently access chat and agent monitoring features

  Background:
    Given I am on the presales application at http://localhost:5173

  Scenario: Initial application load
    Given I load the application for the first time
    Then I should see the main navigation bar at the top
    And I should see two navigation tabs: "Chat" and "Agents"
    And the "Chat" tab should be selected by default
    And the "Chat" tab should have a blue background and blue text
    And the "Agents" tab should have gray text on white background
    And I should see the chat interface below the navigation

  Scenario: Navigation tab visual design
    Given I am viewing the navigation bar
    Then the navigation bar should have:
      - White background
      - Bottom border (gray)
      - Proper padding around tabs
    And each tab should display:
      - An icon (MessageSquare for Chat, Users for Agents)
      - Text label next to the icon
      - Rounded corners when selected
      - Hover effect when not selected

  Scenario: Switching to Agents tab
    Given I am on the Chat tab
    When I click the "Agents" tab
    Then the "Agents" tab should become selected with blue background
    And the "Chat" tab should become unselected with gray text
    And I should see the agents dashboard content
    And the URL should remain the same (single page application)

  Scenario: Switching back to Chat tab
    Given I am on the Agents tab
    When I click the "Chat" tab  
    Then the "Chat" tab should become selected with blue background
    And the "Agents" tab should become unselected with gray text
    And I should see the chat interface content
    And any previous chat messages should still be visible

  Scenario: Tab state persistence during session
    Given I am on the Chat tab and have sent some messages
    When I switch to the Agents tab
    And then switch back to the Chat tab
    Then my previous chat messages should still be displayed
    And my chat history should be preserved
    And the WebSocket connection should remain active

  Scenario: Keyboard navigation support
    Given I am using keyboard navigation
    When I press Tab to navigate through the interface
    Then I should be able to focus on the "Chat" tab
    And I should be able to focus on the "Agents" tab
    And each focused tab should have a visible focus indicator
    When I press Enter on a focused tab
    Then that tab should become active

  Scenario: Tab hover effects
    Given I am using a mouse
    When I hover over the inactive "Agents" tab
    Then the text color should change to a darker gray
    And there should be a smooth color transition
    When I hover over the inactive "Chat" tab
    Then the text color should change to a darker gray
    And there should be a smooth color transition
    When I hover over the active tab
    Then it should maintain its active blue styling

  Scenario: Mobile responsive navigation
    Given I am viewing on mobile device (< 768px width)
    When I look at the navigation bar
    Then both tabs should remain visible
    And the icons and text should be appropriately sized for touch
    And there should be adequate spacing between tabs
    And tapping on tabs should work reliably

  Scenario: Visual feedback for active tab
    Given I am viewing the navigation
    When the "Chat" tab is active
    Then it should have:
      - Blue background (bg-blue-100)
      - Blue text color (text-blue-700)
      - MessageSquare icon in blue
      - Rounded corners
    When the "Agents" tab is active
    Then it should have:
      - Blue background (bg-blue-100)
      - Blue text color (text-blue-700)
      - Users icon in blue
      - Rounded corners

  Scenario: Navigation during different connection states
    Given I am on the Chat tab with a disconnected WebSocket
    When I switch to the Agents tab
    Then the tab switch should work normally
    And I should see the agents dashboard
    When I switch back to the Chat tab
    Then I should see the connection status as disconnected
    And the interface should still be functional

  Scenario: Page refresh behavior
    Given I am on the Agents tab
    When I refresh the page
    Then the application should load with the Chat tab selected (default)
    And I should see the chat interface
    And the WebSocket should attempt to connect

  Scenario: Browser back/forward button behavior
    Given I am navigating between tabs
    When I use browser back/forward buttons
    Then the navigation should not be affected (single page app)
    And I should remain on the same tab I was on
    And the application state should be preserved

  Scenario: Tab accessibility
    Given I am using assistive technology
    When I navigate to the tabs
    Then each tab should have proper ARIA labels
    And the selected tab should be marked with aria-selected="true"
    And the unselected tab should be marked with aria-selected="false"
    And screen readers should announce tab changes

  Scenario: Content area updates
    Given I am switching between tabs
    When I click the "Chat" tab
    Then the content area below should show:
      - Chat interface with header "Presales AI Assistant"
      - Connection status indicator
      - Message list area
      - Message input field at bottom
    When I click the "Agents" tab
    Then the content area below should show:
      - Agents dashboard with agent cards
      - Section headers for "Active Agents" and "Available Agents"
      - Grid layout of agent status cards

  Scenario: Smooth transitions
    Given I am switching between tabs
    When I click from one tab to another
    Then the content should change immediately
    And there should be no loading delay
    And there should be no visual glitches or flickering
    And the transition should feel smooth and responsive