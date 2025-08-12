Feature: AI Agent Processing and Intelligence
  As a sales professional using AI-powered proposal generation
  I want intelligent content analysis and multi-agent processing
  So that I get high-quality, contextually relevant business proposals

  Background:
    Given the LlamaIndex Pre-sales Pipeline application is running
    And I have valid API keys configured
    And I have entered business content in the input phase

  @content-analysis @intelligence
  Scenario: Intelligent Content Analysis and Business Intelligence Extraction
    Given I have entered a customer transcript containing:
      """
      Customer Discovery Call - Global Retail Solutions

      Participants:
      - Jennifer Chen (Chief Digital Officer, Global Retail)
      - Marcus Thompson (VP of Operations, Global Retail)
      - Sarah Wilson (Sales Rep, Our Company)

      Jennifer: "We're struggling with our e-commerce platform integration. Our inventory system, customer database, and payment processing are all separate silos. This creates a nightmare for our customer service team."

      Marcus: "The impact is significant. We're losing approximately $50K per month in failed transactions and customer churn due to poor user experience. Our order fulfillment time has increased by 40% over the past year."

      Jennifer: "We've allocated $750K for a comprehensive digital transformation initiative. The board wants to see results by Q3 2025, which coincides with our peak holiday season preparation."

      Marcus: "We need real-time analytics, automated inventory management, and a unified customer view. Our technical team has experience with cloud platforms and APIs."
      """
    
    When I navigate to the Analysis page
    And I click "🚀 Analyze Content with AI"
    
    Then I should see intelligent analysis results including:
      | Analysis Category | Detected |
      | Transcript Recognition | Yes (conversation format detected) |
      | Industry Classification | Retail/E-commerce |
      | Content Type | Customer Transcript |
      | Urgency Level | High (deadline mentioned) |
    
    And I should see Business Intelligence extraction:
      | Intelligence Type | Extracted Value |
      | Stakeholders | Jennifer Chen (CDO), Marcus Thompson (VP Ops) |
      | Budget Indicators | $750K, $50K monthly loss |
      | Timeline Mentions | Q3 2025, holiday season |
      | Technical Context | Cloud platforms, APIs, inventory systems |
    
    And I should see Solution Mapping:
      | Solution Category | Identified |
      | Integration | ✓ (separate silos mentioned) |
      | Analytics | ✓ (real-time analytics needed) |
      | Automation | ✓ (automated inventory management) |
      | Transformation | ✓ (digital transformation initiative) |

  @agent-routing
  Scenario: Smart AI Agent Routing Based on Content Analysis
    Given I have completed content analysis
    And the system has detected this is a customer transcript about retail integration
    
    When I review the AI Agent Routing Strategy
    
    Then I should see recommended agent sequence:
      | Agent | Recommended | Reason |
      | Conversa | ✅ | Transcript detected - needs conversation analysis |
      | Conny | ✅ | Business consulting needed for solution architecture |
      | ProDy | ✅ | Document generation required |
      | Marketing | ✅ | Customer-facing materials needed |
    
    And I should see estimated processing time: "8 minutes"
    And I should see expected document count: "5+ artifacts"
    
    When I customize the routing to skip Conversa (override)
    And I save the custom routing
    
    Then I should see updated processing plan
    And I should see reduced estimated time: "6 minutes"
    And the system should respect my override while warning about potential impacts

  @ai-pipeline-execution
  Scenario: Multi-Agent Pipeline Processing with Real-Time Monitoring
    Given I have configured the AI agent routing
    And I am on the Processing page
    
    When I click "🚀 Start AI Pipeline"
    
    Then I should see the pipeline state change to "Processing"
    And I should see the overall progress bar at 0%
    And I should see "Current Activity: Initializing pipeline..."
    
    # Note: This tests the demo mode since we don't have actual AI integration yet
    When I click "🎭 Demo Mode (Fast)" instead
    
    Then I should see each agent process in sequence:
      | Agent | Expected Behavior |
      | Conversa | Shows "Conversa processing..." for ~1 second |
      | Conny | Shows "Conny processing..." for ~1 second |
      | ProDy | Shows "ProDy processing..." for ~1 second |
      | Marketing | Shows "Marketing processing..." for ~1 second |
    
    And I should see the progress bar incrementally increase: 25% → 50% → 75% → 100%
    And I should see real-time status updates in the progress log
    And I should see completion celebration (balloons) when finished

  @agent-workflow-visualization
  Scenario: Clear Agent Workflow Visualization and Progress Tracking
    Given I am on the Processing page
    And the AI pipeline is configured to run
    
    When I view the agent workflow visualization
    
    Then I should see a clear flow diagram showing:
      | Agent | Icon | Description | Status |
      | Conversa | 🎧 | Transcript Analysis & Requirements | Waiting |
      | Conny | 💼 | Business Consulting & Architecture | Waiting |
      | ProDy | 📋 | Document Generation & PM | Waiting |
      | Marketing | 🎨 | Customer-Facing Materials | Waiting |
    
    When processing begins
    
    Then I should see status indicators update dynamically:
      | Status | Visual Indicator |
      | Waiting | ⚪ Waiting |
      | Queued | ⏳ Queued |
      | Processing | ⚡ Processing... |
      | Completed | ✅ Completed |
    
    And each agent should show its expected outputs:
      | Agent | Expected Outputs |
      | Conversa | Structured requirements, Stakeholder mapping |
      | Conny | Solution architecture, Implementation strategy |
      | ProDy | Problem overview, Process docs, Investment proposal, Roadmap |
      | Marketing | Sales deck, Executive summary, Value proposition |

  @processing-controls
  Scenario: Processing Controls and Error Handling
    Given I am running the AI pipeline
    And processing is in progress
    
    When I look at the processing controls
    
    Then I should see options to:
      | Control | Available |
      | ⏸️ Pause | ✓ |
      | ⏹️ Stop | ✓ |
      | 🔄 Refresh Status | ✓ |
    
    When I click "⏸️ Pause"
    
    Then the pipeline should pause gracefully
    And I should see "Pipeline paused" message
    And I should see option to resume
    
    When I click "⏹️ Stop"
    
    Then the pipeline should stop completely
    And I should see "Pipeline stopped" message
    And I should have option to restart from beginning

  @output-quality
  Scenario: Validate Quality of AI-Generated Content
    Given I have completed the AI processing pipeline with demo mode
    
    When I review the generated documents
    
    Then each document should demonstrate AI-quality content:
      | Document | Quality Indicators |
      | Problem Overview | Customer-specific pain points, business impact quantification |
      | Solution Architecture | Technical approach, integration patterns, technology stack |
      | Investment Proposal | ROI calculations, budget breakdown, financial justification |
      | Sales Deck | Executive summary, value proposition, competitive advantages |
      | Implementation Roadmap | Project phases, milestones, resource allocation |
    
    And all documents should:
      | Quality Check | Met |
      | Reference correct customer name | ✓ |
      | Include specific details from input | ✓ |
      | Use professional business language | ✓ |
      | Have appropriate length and depth | ✓ |
      | Be ready for customer presentation | ✓ |

  @performance-metrics
  Scenario: Processing Performance and Time Validation
    Given I start the AI processing pipeline
    
    When I monitor the processing time
    
    Then the demo mode should complete in under 10 seconds
    And each agent should process in approximately 1-2 seconds
    And the total workflow should demonstrate the 30% time reduction value proposition
    
    # When real AI integration is implemented:
    # And the full AI pipeline should complete in under 15 minutes
    # And it should be significantly faster than manual proposal creation (8+ hours)

  @error-scenarios
  Scenario: Handle Processing Errors and Edge Cases
    Given I attempt to start processing without proper prerequisites
    
    When I click "🚀 Start AI Pipeline" without input content
    
    Then I should see a clear error message about missing prerequisites
    And I should see helpful buttons to navigate back to required steps
    And the application should not crash or show technical errors
    
    When I have API configuration issues (simulated)
    
    Then I should see user-friendly error messages about connectivity
    And I should see guidance about checking API keys
    And I should be able to retry after fixing the configuration

  @integration-readiness
  Scenario: Verify System is Ready for Real AI Integration
    Given the processing pipeline architecture is in place
    
    When I examine the integration points
    
    Then I should see clear separation between:
      | Component | Purpose |
      | UI Layer | User interaction and progress display |
      | Processing Logic | Agent orchestration and workflow |
      | Mock Implementation | Simulation for demo purposes |
      | Integration Points | Where real AI agents will connect |
    
    And the mock implementation should demonstrate:
      | Capability | Demonstrated |
      | Agent sequencing | ✓ |
      | Progress tracking | ✓ |
      | Result handling | ✓ |
      | Error management | ✓ |
      | State management | ✓ |
    
    And switching to real AI agents should require minimal UI changes