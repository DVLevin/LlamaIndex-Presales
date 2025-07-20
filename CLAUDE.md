# CLAUDE.md - Project Context for Future Sessions

## Project Overview
**LlamaIndex Presales AI System** - A comprehensive multi-agent AI platform for automating presales workflows using LlamaIndex framework with real-time streaming and CRM integrations.

## What We've Built
This is a complete project skeleton with detailed task briefs for each component. The system uses LlamaIndex's multi-agent patterns to create specialized AI agents that collaborate on presales tasks.

## Project Structure & Status

### ✅ Completed Components
- **`ai/TASK_BRIEF.md`** - Multi-agent workflow design with Research, Qualification, Proposal, Review, and Follow-up agents
- **`be/TASK_BRIEF.md`** - FastAPI backend with WebSocket streaming and agent orchestration  
- **`fe/` (PRODUCTION READY)** - Complete React + TypeScript frontend with real-time capabilities
- **`db/TASK_BRIEF.md`** - PostgreSQL schema for conversation state and agent execution tracking
- **`tools/TASK_BRIEF.md`** - Custom tools for CRM integration, research, qualification, and document generation
- **`docs/ARCHITECTURE_OVERVIEW.md`** - Complete system architecture documentation
- **`future_ideas/EXPANSION_CONCEPTS.md`** - Roadmap for phases 2-4 with advanced features
- **`README.md`** - Comprehensive project documentation and setup instructions
- **`DEVELOPMENT_PLAN.md`** - Detailed development roadmap with LlamaIndex implementation strategy

### 📁 Key Directories
```
LlamaIndex-Presales/
├── ai/              # AI agents using LlamaIndex workflows
├── be/              # Backend API and orchestration
├── fe/              # Frontend user interface
├── db/              # Database schemas and state management  
├── tools/           # Custom tool implementations
├── docs/            # Architecture documentation
├── future_ideas/    # Expansion roadmap
├── guides/          # LlamaIndex implementation guides
└── project_idea/    # Original (empty) task brief
```

## Technical Architecture

### Core Technologies
- **AI Framework**: LlamaIndex 0.10+ with AgentWorkflow, Orchestrator, or Custom Planner patterns
- **Backend**: FastAPI with async/await, WebSocket streaming, Celery task queue
- **Frontend**: Modern React/Vue with real-time components, WebSocket client
- **Database**: PostgreSQL 15+ with JSONB for agent state, Redis for caching
- **Deployment**: Docker Compose for dev, Kubernetes for production

### Agent Workflow Design
```
Research Agent → Qualification Agent → Proposal Agent → Review Agent
      ↓                ↓                    ↓              ↓
   Research         Lead Score          Proposal       Quality
    Notes           & Status            Content        Assurance
      ↓                ↓                    ↓              ↓
                    Follow-up Agent (if needed)
                           ↓
                  Database State Persistence
```

### Integration Points
- **CRM Systems**: Salesforce, HubSpot, Microsoft Dynamics
- **Research APIs**: Web search (Tavily), company databases, social media
- **Communication**: Email automation, calendar scheduling
- **Document Generation**: Proposal templates, contract automation

## Development Commands

### Common Commands for Each Component
```bash
# Backend development
cd be/
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend development  
cd fe/
npm install
npm run dev

# Database setup
cd db/
# Run migration scripts (to be implemented)

# Full stack with Docker
docker-compose up -d
```

### Testing Commands
```bash
# Backend tests
cd be/ && pytest tests/

# Frontend tests
cd fe/ && npm run test

# Acceptance tests (manual verification)
cd fe/ && npm run test:acceptance
cd be/ && pytest tests/acceptance/
cd ai/ && python -m pytest tests/acceptance/

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Acceptance Testing Strategy (BDD/ATDD)

We follow **Behavior-Driven Development (BDD)** and **Acceptance Test-Driven Development (ATDD)** practices. Every component must have corresponding acceptance tests that can be manually verified.

### Acceptance Test Requirements
- **Location**: Each component folder must contain `tests/acceptance/` directory
- **Format**: Gherkin-style scenarios with Given/When/Then structure
- **Coverage**: All user-facing functionality must have acceptance criteria
- **Manual Verification**: Tests should be written so they can be manually executed and verified

### Acceptance Test Structure
```
component_folder/
├── src/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── acceptance/          # Acceptance tests here
│       ├── README.md        # How to run acceptance tests
│       ├── chat.feature     # Gherkin scenarios
│       ├── dashboard.feature
│       └── websocket.feature
```

### Writing Acceptance Tests
1. **Feature Files**: Use `.feature` extension with Gherkin syntax
2. **Scenarios**: Each feature should have multiple test scenarios
3. **Steps**: Clear Given/When/Then steps that can be manually verified
4. **Data**: Include test data and expected outcomes
5. **Prerequisites**: Document any setup required before testing

### Example Acceptance Test
```gherkin
Feature: Real-time Chat Interface
  As a sales representative
  I want to see AI agent responses in real-time
  So that I can monitor the presales process actively

  Scenario: Agent message streaming
    Given I am connected to the chat interface
    And the WebSocket connection is established
    When I send a message "Research Acme Corp"
    Then I should see "Research Agent is working..." immediately
    And I should see research results streaming in real-time
    And the final message should contain company information
    And the agent status should show "Research Complete"
```

### Acceptance Testing Workflow
1. **Before Implementation**: Write acceptance criteria first
2. **During Development**: Reference acceptance tests to guide implementation
3. **After Implementation**: Manually verify all acceptance scenarios
4. **Documentation**: Update acceptance tests when requirements change
5. **Handoff**: Use acceptance tests to demonstrate completed features

## Next Steps for Implementation

## Current Implementation Status

### ✅ Phase 1: Frontend (COMPLETED)
**Frontend** (`fe/` folder): **🎉 PRODUCTION READY**
- ✅ Complete React + TypeScript + Vite setup with Tailwind CSS
- ✅ WebSocket client with auto-reconnection and connection management  
- ✅ Real-time chat interface with message rendering
- ✅ Agent status dashboard with visual indicators
- ✅ Navigation system between Chat and Agents tabs
- ✅ Comprehensive BDD/ATDD acceptance tests
- ✅ Responsive design and accessibility features
- ✅ TypeScript type system for all components
- ✅ Development server running on http://localhost:5173

### 🔄 Phase 2: Backend Implementation (NEXT PRIORITY)
**Backend** (`be/` folder): Ready for development
- 📋 FastAPI + WebSocket infrastructure (see DEVELOPMENT_PLAN.md)
- 📋 LlamaIndex AgentWorkflow integration
- 📋 Multi-agent orchestration with streaming events
- 📋 Database state persistence

### 📋 Phase 3: AI Agents Development 
**AI Agents** (`ai/` folder): Specification complete
- 📋 Implement FunctionAgent classes using LlamaIndex patterns
- 📋 Create AgentWorkflow with Research → Qualification → Proposal → Review flow
- 📋 Add streaming event handling for real-time frontend updates  
- 📋 Integrate with custom tools from `tools/` folder

### 📋 Phase 4: Database & Tools
**Database** (`db/` folder): Schema designed
- 📋 PostgreSQL implementation with conversation persistence
- 📋 Agent execution tracking and audit trails
- 📋 State serialization/deserialization for workflow continuity

**Tools** (`tools/` folder): Specifications complete
- 📋 CRM integration tools (Salesforce, HubSpot)
- 📋 Research tools with Tavily web search integration
- 📋 Document generation and proposal tools
- 📋 Compliance and validation utilities

### Key Implementation Patterns from Guides

#### Agent Creation (from guides/Multi-agent workflows - LlamaIndex.md)
```python
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow

research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Conducts prospect research and market intelligence",
    system_prompt="You are a sales research specialist...",
    tools=[web_search_tool, crm_lookup_tool],
    can_handoff_to=["QualificationAgent"]
)
```

#### Streaming Implementation (from guides/Streaming output and events - LlamaIndex.md)
```python
from llama_index.core.agent.workflow import AgentStream

async for event in agent_workflow.stream_events():
    if isinstance(event, AgentStream):
        # Stream to frontend via WebSocket
        await websocket.send_text(event.delta)
```

### Environment Variables Needed
```bash
# AI Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_key (optional)

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/presales
REDIS_URL=redis://localhost:6379/0

# CRM Integration
SALESFORCE_CLIENT_ID=your_salesforce_client_id
SALESFORCE_CLIENT_SECRET=your_salesforce_secret
HUBSPOT_API_KEY=your_hubspot_api_key

# Research APIs
TAVILY_API_KEY=your_tavily_api_key
```

## Common Development Patterns

### Adding New Agents
1. Create agent class in `ai/agents/`
2. Define tools in `tools/`
3. Add to workflow orchestration
4. Update database schema if needed
5. Add frontend visualization

### Adding New Tools
1. Inherit from `BaseToolSpec` in `tools/`
2. Implement required methods with type hints
3. Add to agent configuration
4. Test integration
5. Document usage

### Frontend Component Development  
1. Create WebSocket connection management
2. Implement real-time message rendering
3. Add agent status indicators
4. Create conversation history display
5. Build responsive design

## Important Notes for Future Sessions

### Project Philosophy
- **Agent-centric design**: Everything revolves around intelligent agents collaborating
- **Real-time first**: Users should see agent progress as it happens
- **State persistence**: Conversations can be resumed after interruptions
- **Tool extensibility**: Easy to add new integrations and capabilities
- **Security by design**: Enterprise-ready with comprehensive audit trails

### Key Decisions Made
- **LlamaIndex**: Chosen for mature multi-agent framework
- **PostgreSQL**: Selected for JSONB support and strong consistency
- **FastAPI**: Picked for async support and automatic OpenAPI docs
- **WebSocket streaming**: Real-time updates are core requirement
- **Modular architecture**: Each component can be developed independently

### Development Priorities (Updated)
1. ✅ **Frontend streaming** provides user experience - **COMPLETED**
2. 🔄 **Backend orchestration** enables agent coordination - **NEXT**
3. 📋 **AI agents** are the core value - Phase 3
4. 📋 **Database persistence** ensures reliability - Phase 4
5. 📋 **Custom tools** provide competitive advantage - Phase 4

### LlamaIndex Integration Strategy
Based on analysis of guides in `guides/` folder:
- **AgentWorkflow Pattern**: Use linear swarm pattern for presales workflow
- **FunctionAgent Implementation**: Specialized agents with specific tools and handoff capabilities  
- **Streaming Events**: Real-time progress updates to frontend via WebSocket
- **Tavily Integration**: Web research capabilities for ResearchAgent
- **Tool Modularity**: Reusable tools across different agents
- **State Persistence**: Conversation and workflow state management

### Repository Status
- **Current**: ✅ Frontend production-ready, detailed development plan created
- **Next**: 🔄 Backend FastAPI + WebSocket implementation (see DEVELOPMENT_PLAN.md)
- **Git**: All changes committed with clean history

### Quick Start Commands
```bash
# Frontend development (WORKING NOW)
cd fe/
npm install
npm run dev  # http://localhost:5173

# Acceptance testing
cd fe/tests/acceptance/
# Follow README.md for manual testing procedures

# Next: Backend development
cd be/
# See DEVELOPMENT_PLAN.md Phase 2 for implementation steps
```

This CLAUDE.md provides complete context for any future development sessions on this project.