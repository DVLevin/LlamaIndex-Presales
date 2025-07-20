# Project Architecture Overview

## System Overview
The LlamaIndex Presales System is a comprehensive multi-agent AI platform designed to automate and enhance the presales process through intelligent agent orchestration, real-time streaming, and seamless integrations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (FE)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Chat UI   │  │ Dashboard   │  │  Analytics  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────┬───────────────────────────────────────────┘
                      │ WebSocket + REST API
┌─────────────────────┴───────────────────────────────────────────┐
│                        Backend (BE)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ API Gateway │  │   Streaming │  │ Agent Mgmt  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Agent Orchestration
┌─────────────────────┴───────────────────────────────────────────┐
│                         AI Agents                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Research   │  │Qualification│  │  Proposal   │              │
│  │   Agent     │  │   Agent     │  │   Agent     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐  ┌─────────────┐                               │
│  │  Follow-up  │  │   Review    │                               │
│  │   Agent     │  │   Agent     │                               │
│  └─────────────┘  └─────────────┘                               │
└─────────┬───────────────────────────────────────┬───────────────┘
          │                                       │
┌─────────┴───────────┐                 ┌─────────┴───────────────┐
│       Tools         │                 │      Database           │
│  ┌─────────────┐    │                 │  ┌─────────────┐        │
│  │ CRM Tools   │    │                 │  │Conversation │        │
│  └─────────────┘    │                 │  │    State    │        │
│  ┌─────────────┐    │                 │  └─────────────┘        │
│  │Research Tools│    │                 │  ┌─────────────┐        │
│  └─────────────┘    │                 │  │   Agent     │        │
│  ┌─────────────┐    │                 │  │  Execution  │        │
│  │Custom Tools │    │                 │  └─────────────┘        │
│  └─────────────┘    │                 └─────────────────────────┘
└─────────────────────┘
```

## Component Interaction Flow

### 1. User Interaction Flow
```
User Input → Frontend → Backend API → Agent Orchestrator → AI Agents
     ↑                                                         ↓
Frontend ← WebSocket Stream ← Backend Streaming ← Agent Events
```

### 2. Agent Workflow
```
Research Agent → Qualification Agent → Proposal Agent → Review Agent
      ↓                ↓                    ↓              ↓
   Research         Lead Score          Proposal       Quality
    Notes           & Status            Content        Assurance
      ↓                ↓                    ↓              ↓
                  Database State Management
```

## Technology Stack

### Frontend Stack
- **Framework**: React 18+ with Next.js or Vue 3 with Nuxt.js
- **State Management**: Redux Toolkit or Pinia
- **UI Components**: Tailwind CSS + Headless UI
- **Real-time**: WebSocket client with auto-reconnection
- **Build Tools**: Vite or Webpack 5

### Backend Stack
- **Framework**: FastAPI (Python) with async support
- **WebSocket**: FastAPI WebSocket or Socket.IO
- **Task Queue**: Celery with Redis broker
- **API Documentation**: OpenAPI/Swagger auto-generation
- **Monitoring**: Prometheus + Grafana

### AI/ML Stack
- **Core Framework**: LlamaIndex 0.10+
- **LLM Integration**: OpenAI GPT-4, Anthropic Claude, or OpenRouter
- **Agent Patterns**: AgentWorkflow, Orchestrator, or Custom Planner
- **Tool Integration**: LlamaHub tools + Custom tools
- **Vector Storage**: Pinecone, Weaviate, or Qdrant (if needed)

### Database Stack
- **Primary Database**: PostgreSQL 15+ with JSONB support
- **Caching Layer**: Redis for session and real-time data
- **Migration Management**: Alembic (SQLAlchemy)
- **Connection Pooling**: pgbouncer for connection management

### Infrastructure Stack
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production) or Docker Swarm (dev)
- **Reverse Proxy**: Nginx or Traefik
- **Monitoring**: Prometheus, Grafana, ELK stack
- **CI/CD**: GitHub Actions, GitLab CI, or Jenkins

## Data Flow Architecture

### 1. Conversation Lifecycle
```sql
-- Conversation initialization
conversations → messages → agent_executions → tool_calls → outcomes
```

### 2. Agent State Management
```python
# State flow example
ConversationState {
    prospect_info: {...},
    research_notes: [...],
    qualification_score: 85,
    proposal_content: "...",
    current_agent: "ProposalAgent",
    workflow_status: "in_progress"
}
```

### 3. Real-time Event Stream
```javascript
// WebSocket event types
{
    type: "agent_start",
    agent: "ResearchAgent",
    timestamp: "2025-01-20T10:00:00Z"
}

{
    type: "tool_call",
    tool: "company_research",
    parameters: {...},
    status: "executing"
}

{
    type: "agent_stream",
    delta: "Based on my research...",
    agent: "ResearchAgent"
}
```

## Security Architecture

### Authentication & Authorization
- **User Authentication**: JWT tokens with refresh mechanism
- **API Security**: OAuth 2.0 with scopes
- **Role-Based Access**: Admin, Manager, Sales Rep permissions
- **Rate Limiting**: Per-user and per-endpoint limits

### Data Protection
- **Encryption**: TLS 1.3 for data in transit
- **Database**: Encryption at rest for sensitive fields
- **API Keys**: Secure vault storage (HashiCorp Vault)
- **PII Protection**: Anonymization and pseudonymization

### Compliance
- **GDPR**: Data processing consent and deletion rights
- **SOC 2**: Security controls and audit trails
- **Data Residency**: Geographic data storage options
- **Audit Logging**: Complete action audit trails

## Scalability Considerations

### Horizontal Scaling
- **Backend**: Stateless API servers behind load balancer
- **Database**: Read replicas and connection pooling
- **Agent Execution**: Distributed task processing
- **Caching**: Redis cluster for session data

### Performance Optimization
- **API Response Time**: Target <200ms for most endpoints
- **Agent Execution**: Parallel tool execution where possible
- **Database Queries**: Optimized indexes and query patterns
- **Frontend**: Code splitting and lazy loading

### Monitoring & Observability
- **Application Metrics**: Response times, error rates, throughput
- **Agent Performance**: Success rates, execution times
- **Infrastructure**: CPU, memory, disk, network utilization
- **Business Metrics**: Conversion rates, user engagement

## Deployment Architecture

### Development Environment
```yaml
# docker-compose.yml structure
services:
  frontend:
    build: ./fe
    ports: ["3000:3000"]
  
  backend:
    build: ./be
    ports: ["8000:8000"]
    depends_on: [db, redis]
  
  db:
    image: postgres:15
    volumes: ["postgres_data:/var/lib/postgresql/data"]
  
  redis:
    image: redis:7-alpine
```

### Production Environment
- **Container Orchestration**: Kubernetes with ingress controllers
- **Database**: Managed PostgreSQL with automatic backups
- **Caching**: Redis cluster with persistence
- **Load Balancing**: Application load balancer with health checks
- **Monitoring**: Comprehensive observability stack

## Integration Points

### External Systems
- **CRM Systems**: Salesforce, HubSpot, Microsoft Dynamics
- **Email Services**: SendGrid, AWS SES, Mailgun
- **Calendar Systems**: Google Calendar, Outlook, Calendly
- **Communication**: Slack, Microsoft Teams integration

### API Design Principles
- **RESTful Design**: Standard HTTP methods and status codes
- **API Versioning**: URL path versioning (/api/v1/)
- **Error Handling**: Consistent error response format
- **Documentation**: OpenAPI specifications with examples

## Development Workflow

### Code Organization
```
project/
├── be/          # Backend application
├── fe/          # Frontend application  
├── ai/          # AI agents and workflows
├── db/          # Database schemas and migrations
├── tools/       # Custom tool implementations
├── docs/        # Documentation
└── future_ideas/# Expansion concepts
```

### Quality Assurance
- **Testing**: Unit, integration, and E2E test suites
- **Code Quality**: Linting, formatting, type checking
- **Security**: SAST, DAST, dependency scanning
- **Performance**: Load testing and profiling

This architecture provides a solid foundation for building a scalable, maintainable, and secure multi-agent presales system while allowing for future expansion and enhancement.