# CLAUDE.md - Project Context for Future Sessions

## Project Overview
**LlamaIndex Presales AI System** - A comprehensive multi-agent AI platform for automating presales workflows using LlamaIndex framework with real-time streaming and CRM integrations.

## What We've Built
This is a complete project skeleton with detailed task briefs for each component. The system uses LlamaIndex's multi-agent patterns to create specialized AI agents that collaborate on presales tasks.

## Project Structure & Status

### ✅ Completed Components
- **`ai/TASK_BRIEF.md`** - Multi-agent workflow design with Research, Qualification, Proposal, Review, and Follow-up agents
- **`be/TASK_BRIEF.md`** - FastAPI backend with WebSocket streaming and agent orchestration
- **`fe/TASK_BRIEF.md`** - React/Vue frontend with real-time chat interface and dashboards
- **`db/TASK_BRIEF.md`** - PostgreSQL schema for conversation state and agent execution tracking
- **`tools/TASK_BRIEF.md`** - Custom tools for CRM integration, research, qualification, and document generation
- **`docs/ARCHITECTURE_OVERVIEW.md`** - Complete system architecture documentation
- **`future_ideas/EXPANSION_CONCEPTS.md`** - Roadmap for phases 2-4 with advanced features
- **`README.md`** - Comprehensive project documentation and setup instructions

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

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Next Steps for Implementation

### Phase 1: Core Implementation (Current Priority)
1. **AI Agents** (`ai/` folder):
   - Implement FunctionAgent classes for each specialist agent
   - Create AgentWorkflow or Orchestrator pattern setup  
   - Add streaming event handling for real-time updates
   - Integrate with custom tools from `tools/` folder

2. **Backend** (`be/` folder):
   - Set up FastAPI project with async endpoints
   - Implement WebSocket streaming for agent outputs
   - Create agent orchestration logic
   - Add database integration for state persistence

3. **Frontend** (`fe/` folder):
   - Build React/Vue chat interface
   - Implement WebSocket client for real-time streaming  
   - Create agent activity visualization components
   - Add dashboard for conversation management

4. **Database** (`db/` folder):
   - Design PostgreSQL schema for conversations, agent executions, tool calls
   - Implement state serialization/deserialization
   - Create migration system
   - Add performance indexes

5. **Tools** (`tools/` folder):
   - Implement CRM integration tools (Salesforce, HubSpot)
   - Build research and qualification tools
   - Create document generation utilities
   - Add compliance and validation tools

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

### Development Priorities
1. **AI agents** are the core value - start here
2. **Backend orchestration** enables agent coordination
3. **Frontend streaming** provides user experience
4. **Database persistence** ensures reliability
5. **Custom tools** provide competitive advantage

### Repository Status
- **Current**: Complete project skeleton with detailed task briefs
- **Next**: Begin implementation starting with AI agents
- **Git**: Ready to initialize repository and push to GitHub

This CLAUDE.md provides complete context for any future development sessions on this project.