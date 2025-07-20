Feature: Agent Status Dashboard
  As a sales representative
  I want to monitor AI agent activities and statuses
  So that I can understand what agents are working on and their current state

  Background:
    Given I am on the presales application at http://localhost:5173
    And I click on the "Agents" tab

  Scenario: Initial dashboard display
    Given I am on the agents dashboard
    Then I should see the heading "Available Agents"
    And I should see 4 agent cards displayed in a grid
    And each agent card should show:
      - Agent name (Research Agent, Qualification Agent, Proposal Agent, Review Agent)
      - Agent description
      - Current status badge
    And all agents should initially show "Idle" status with gray background

  Scenario: Agent card information display
    Given I am viewing the agent dashboard
    Then the "Research Agent" card should display:
      - Name: "Research Agent"
      - Description: "Conducts prospect research and market intelligence"
      - Status: "Idle" with Bot icon and gray background
    And the "Qualification Agent" card should display:
      - Name: "Qualification Agent"
      - Description: "Evaluates lead quality and scoring"
      - Status: "Idle" with Bot icon and gray background
    And the "Proposal Agent" card should display:
      - Name: "Proposal Agent"
      - Description: "Generates customized proposals and presentations"
      - Status: "Idle" with Bot icon and gray background
    And the "Review Agent" card should display:
      - Name: "Review Agent"
      - Description: "Quality assurance and compliance checking"
      - Status: "Idle" with Bot icon and gray background

  Scenario: Agent status visual indicators
    Given I am viewing agent status badges
    When an agent status is "Idle"
    Then I should see a Bot icon and gray background
    When an agent status is "Thinking"
    Then I should see a Clock icon and blue background
    When an agent status is "Working"
    Then I should see a spinning Loader icon and yellow background
    When an agent status is "Waiting"
    Then I should see a Pause icon and purple background
    When an agent status is "Completed"
    Then I should see a CheckCircle icon and green background
    When an agent status is "Error"
    Then I should see an AlertCircle icon and red background

  Scenario: Active vs Available agents organization
    Given some agents are working and others are idle
    When I view the dashboard
    Then I should see an "Active Agents" section at the top
    And active agents should include those with status: thinking, working, waiting, completed, error
    And I should see an "Available Agents" section below
    And available agents should be those with "idle" status
    And available agents should be displayed in a 2-column grid

  Scenario: Current task display
    Given an agent has a current task assigned
    When I view that agent's card
    Then I should see a "Current Task:" label
    And below it, I should see the task description
    And the task text should be clearly visible and readable
    When an agent has no current task
    Then the "Current Task" section should not be displayed

  Scenario: Empty state when no agents are available
    Given there are no agents configured in the system
    When I view the agents dashboard  
    Then I should see a centered message box
    And it should display "No agents active"
    And below it should say "Start a conversation to see agent activity"
    And the message should have a gray background and border

  Scenario: Responsive design - Desktop view
    Given I am viewing the dashboard on desktop (> 1024px width)
    When I look at the available agents section
    Then idle agents should be displayed in a 2-column grid
    And each agent card should have adequate spacing
    And text should be clearly readable

  Scenario: Responsive design - Mobile view
    Given I am viewing the dashboard on mobile (< 768px width)
    When I look at the available agents section
    Then idle agents should be displayed in a single column
    And each agent card should span the full width
    And all text should remain readable without horizontal scrolling
    And status badges should remain appropriately sized

  Scenario: Agent status updates in real-time
    Given I have the agents dashboard open
    And I have WebSocket connection to the backend
    When an agent status changes from "idle" to "working"
    Then the agent card should move from "Available Agents" to "Active Agents" section
    And the status badge should update to show spinning loader and yellow background
    When the agent status changes from "working" to "completed"
    Then the status badge should update to show checkmark and green background
    And the agent should remain in the "Active Agents" section
    When the agent status returns to "idle"
    Then the agent card should move back to "Available Agents" section

  Scenario: Agent card visual hierarchy
    Given I am viewing agent cards
    Then each card should have:
      - White background with subtle border
      - Rounded corners
      - Appropriate padding for readability
      - Agent name as the most prominent text (medium font weight)
      - Description in smaller, lighter text
      - Status badge prominently positioned in top-right corner
      - Current task (if present) clearly separated from description

  Scenario: Navigation between tabs
    Given I am on the agents dashboard
    When I click the "Chat" tab
    Then I should see the chat interface
    And the "Chat" tab should be highlighted with blue background
    When I click the "Agents" tab again
    Then I should return to the agents dashboard
    And the "Agents" tab should be highlighted with blue background
    And my previous view state should be preserved

  Scenario: Agent task information updates
    Given an agent is showing a current task
    When the agent completes the task and starts a new one
    Then the "Current Task" text should update to show the new task
    And the update should happen smoothly without page refresh
    When an agent finishes all tasks
    Then the "Current Task" section should disappear
    And only the agent name, description, and status should remain

  Scenario: Dashboard performance
    Given I am viewing the agents dashboard
    When agent statuses update frequently
    Then the dashboard should update smoothly without flickering
    And there should be no noticeable delay in status changes
    And the interface should remain responsive during updates

  Scenario: Accessibility - Screen reader support
    Given I am using a screen reader
    When I navigate to the agents dashboard
    Then each agent card should have appropriate ARIA labels
    And agent status changes should be announced
    And the current task information should be readable
    And navigation between sections should be clear

  Scenario: Accessibility - Keyboard navigation
    Given I am using keyboard navigation
    When I press Tab repeatedly on the agents dashboard
    Then I should be able to navigate to clickable elements
    And each focused element should have a visible focus indicator
    And the tab order should be logical (top to bottom, left to right)