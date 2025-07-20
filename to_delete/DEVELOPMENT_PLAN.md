# LlamaIndex Presales AI System - Development Plan

## Project Status Overview

### ✅ Phase 1: Frontend Foundation (COMPLETED)
**Status**: Production-ready frontend with real-time capabilities
- React + TypeScript + Vite setup
- WebSocket client with auto-reconnection
- Chat interface with agent communication
- Agent status dashboard
- Comprehensive BDD/ATDD acceptance tests
- Responsive design and accessibility

## Development Roadmap

---

## 🚀 Phase 2: Backend Foundation (NEXT PRIORITY - 2-3 weeks)

### Epic 1: FastAPI + WebSocket Infrastructure
**Goal**: Create the backend server that connects to the existing frontend

#### Features:
- **FastAPI Application Setup**
  - Async FastAPI server on port 8000
  - CORS configuration for frontend connection
  - Health check endpoints (`/health`, `/api/status`)
  - Environment configuration management

- **WebSocket Real-time Communication**
  - WebSocket endpoint at `/ws/{conversation_id}`
  - Connection management and client tracking
  - Message broadcasting to connected clients
  - Heartbeat/ping-pong for connection health

- **Basic Conversation Management**
  - In-memory conversation storage (Phase 2)
  - Conversation lifecycle management
  - Message history tracking
  - Session state persistence

#### Implementation Strategy:
```python
# Core FastAPI structure
app = FastAPI()
websocket_manager = WebSocketManager()

@app.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    # Connect to frontend WebSocket client
    pass

@app.post("/api/conversations/{conversation_id}/messages")
async def send_message(conversation_id: str, message: MessageRequest):
    # Trigger agent processing
    pass
```

#### Success Criteria:
- Frontend connects successfully to `ws://localhost:8000`
- Messages sent from frontend appear in backend logs
- Basic echo/response functionality working
- WebSocket connection status shows "Connected"

---

## 🤖 Phase 3: LlamaIndex Agent Integration (3-4 weeks)

### Epic 2: Multi-Agent Workflow Implementation
**Goal**: Implement the core AI agents using LlamaIndex patterns

#### Based on LlamaIndex Guides Analysis:

**Pattern Choice**: **AgentWorkflow** (Linear Swarm Pattern)
- Convenience and built-in handoff management
- Perfect for presales workflow sequence
- Streaming event support included

#### Agent Architecture:
```python
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent

# Research Agent - First in chain
research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Conducts prospect research and market intelligence",
    system_prompt="You are a sales research specialist. Gather company information, market data, and competitive intelligence. Hand off to QualificationAgent when research is complete.",
    llm=llm,
    tools=[web_search_tool, crm_lookup_tool, company_data_tool],
    can_handoff_to=["QualificationAgent"]
)

# Qualification Agent - Scores and evaluates
qualification_agent = FunctionAgent(
    name="QualificationAgent",
    description="Evaluates lead quality and assigns qualification scores",
    system_prompt="You are a sales qualification expert. Analyze research data to score lead quality, identify decision makers, and assess purchase intent. Hand off to ProposalAgent for qualified leads.",
    llm=llm,
    tools=[scoring_tool, decision_maker_tool, budget_analysis_tool],
    can_handoff_to=["ProposalAgent", "FollowUpAgent"]
)

# Proposal Agent - Generates customized proposals
proposal_agent = FunctionAgent(
    name="ProposalAgent", 
    description="Generates customized proposals and presentations",
    system_prompt="You are a proposal generation specialist. Create tailored proposals, pricing models, and presentation materials based on research and qualification data. Hand off to ReviewAgent for quality assurance.",
    llm=llm,
    tools=[proposal_template_tool, pricing_tool, document_generation_tool],
    can_handoff_to=["ReviewAgent"]
)

# Review Agent - Quality assurance
review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Quality assurance and compliance checking", 
    system_prompt="You are a quality assurance specialist. Review all generated content for accuracy, compliance, and alignment with company standards. Provide final approval or request revisions.",
    llm=llm,
    tools=[compliance_checker_tool, content_review_tool, approval_tool],
    can_handoff_to=["FollowUpAgent"]
)

# Workflow orchestration
workflow = AgentWorkflow(
    agents=[research_agent, qualification_agent, proposal_agent, review_agent],
    initial_agent="ResearchAgent",
    verbose=True
)
```

#### Streaming Implementation:
```python
async def process_user_message(conversation_id: str, message: str):
    # Stream events to frontend via WebSocket
    async for event in workflow.stream_events(message):
        await websocket_manager.send_event(conversation_id, {
            "type": event.type,
            "data": event.data,
            "agent": event.agent_name,
            "timestamp": datetime.utcnow()
        })
```

### Epic 3: Custom Tools Development
**Goal**: Build specialized tools for each agent

#### Research Agent Tools:
- **Web Search Tool** (Tavily integration)
- **CRM Lookup Tool** (Salesforce/HubSpot API)
- **Company Data Tool** (Company information APIs)
- **Market Intelligence Tool** (Industry data sources)

#### Qualification Agent Tools:
- **Lead Scoring Tool** (Proprietary scoring algorithm)
- **Decision Maker Identification** (LinkedIn/company database)
- **Budget Analysis Tool** (Financial data analysis)
- **Competition Analysis Tool** (Competitive intelligence)

#### Proposal Agent Tools:
- **Template Engine** (Document generation)
- **Pricing Calculator** (Dynamic pricing models)
- **ROI Calculator** (Value proposition tools)
- **Presentation Builder** (Slide generation)

#### Review Agent Tools:
- **Compliance Checker** (Legal/regulatory validation)
- **Content Quality Analyzer** (Grammar, consistency)
- **Brand Alignment Tool** (Style guide enforcement)
- **Approval Workflow** (Internal review process)

---

## 🗄️ Phase 4: Database & State Management (2-3 weeks)

### Epic 4: PostgreSQL Integration
**Goal**: Persistent storage for conversations and agent executions

#### Database Schema:
```sql
-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    status conversation_status,
    user_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB
);

-- Messages table  
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    content TEXT,
    type message_type,
    agent_name VARCHAR(100),
    timestamp TIMESTAMP,
    metadata JSONB
);

-- Agent executions table
CREATE TABLE agent_executions (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    agent_name VARCHAR(100),
    status execution_status,
    input_data JSONB,
    output_data JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- Tool calls table
CREATE TABLE tool_calls (
    id UUID PRIMARY KEY,
    agent_execution_id UUID REFERENCES agent_executions(id),
    tool_name VARCHAR(100),
    parameters JSONB,
    result JSONB,
    status tool_status,
    executed_at TIMESTAMP
);
```

#### State Management:
- **Conversation State Serialization**: Save/restore agent workflow state
- **Message Persistence**: All conversation history stored
- **Agent Execution Tracking**: Audit trail of all agent activities
- **Performance Metrics**: Response times, success rates, error rates

---

## 🔧 Phase 5: Production Features (3-4 weeks)

### Epic 5: Authentication & Multi-tenancy
- **JWT Authentication**: Secure user sessions
- **Role-based Access Control**: Admin, sales rep, manager roles
- **Multi-tenant Architecture**: Organization isolation
- **User Management**: Registration, profiles, preferences

### Epic 6: Advanced Features
- **Conversation Export**: PDF, Word document generation
- **Email Integration**: Automated follow-up emails
- **Calendar Integration**: Meeting scheduling
- **Notification System**: Real-time alerts and updates

### Epic 7: Monitoring & Analytics
- **Application Monitoring**: Health checks, performance metrics
- **Agent Performance Analytics**: Success rates, response times
- **Business Intelligence**: Sales pipeline insights
- **Error Tracking**: Logging and alerting

---

## 🚀 Phase 6: Deployment & Scaling (2-3 weeks)

### Epic 8: Production Deployment
- **Docker Containerization**: All services containerized
- **Kubernetes Deployment**: Production orchestration
- **CI/CD Pipelines**: Automated testing and deployment
- **Environment Management**: Dev, staging, production

### Epic 9: Performance Optimization
- **Database Optimization**: Indexing, query performance
- **Caching Layer**: Redis for session and response caching
- **Load Balancing**: Multiple backend instances
- **CDN Integration**: Static asset delivery

---

## Development Methodology

### BDD/ATDD Approach (Continued)
- **Acceptance Tests First**: Write tests before implementation
- **Feature Files**: Gherkin scenarios for all new features
- **Manual Verification**: Regular testing against acceptance criteria
- **Documentation**: Keep tests as living documentation

### LlamaIndex Best Practices
- **Follow Guide Patterns**: Use recommended AgentWorkflow approach
- **Streaming First**: Implement real-time updates throughout
- **Tool Modularity**: Build reusable, composable tools
- **State Management**: Proper conversation state handling
- **Error Recovery**: Graceful handling of agent failures

### Quality Assurance
- **Code Reviews**: All changes reviewed
- **Automated Testing**: Unit, integration, E2E tests
- **Performance Testing**: Load testing for agent workflows
- **Security Testing**: Penetration testing and vulnerability scans

---

## Success Metrics

### Technical Metrics
- **Response Time**: < 500ms for API calls, < 2s for agent responses
- **Availability**: 99.9% uptime for production system
- **Agent Success Rate**: > 95% successful completions
- **WebSocket Reliability**: < 0.1% connection failures

### Business Metrics
- **User Adoption**: Track active users and session length
- **Proposal Quality**: Measure acceptance rates
- **Sales Efficiency**: Time savings in presales process
- **Customer Satisfaction**: Feedback scores and NPS

### Development Velocity
- **Feature Delivery**: Consistent sprint velocity
- **Bug Resolution**: < 24h critical, < 72h high priority
- **Test Coverage**: > 80% code coverage
- **Documentation**: All features documented with acceptance tests

---

## Resource Requirements

### Development Team
- **Backend Developer**: FastAPI + LlamaIndex specialist
- **Frontend Developer**: React + TypeScript expert
- **DevOps Engineer**: Kubernetes + monitoring
- **QA Engineer**: Test automation + manual testing

### Infrastructure
- **Development**: Cloud VM for development/testing
- **Staging**: Kubernetes cluster for staging environment
- **Production**: Production-grade Kubernetes with monitoring
- **Database**: Managed PostgreSQL + Redis cluster

### External Services
- **LLM Provider**: OpenAI API or equivalent
- **Search API**: Tavily for web research
- **CRM Integration**: Salesforce/HubSpot API access
- **Monitoring**: Application monitoring service

This development plan provides a clear roadmap from the current completed frontend to a full production system, with specific focus on LlamaIndex implementation patterns and maintaining the BDD/ATDD approach throughout.