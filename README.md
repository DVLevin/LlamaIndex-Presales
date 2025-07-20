# LlamaIndex Presales AI System

A comprehensive multi-agent AI platform that automates and enhances the presales process through intelligent agent orchestration, real-time streaming, and seamless CRM integrations.

## 🚀 Overview

This system leverages **LlamaIndex** to create specialized AI agents that work together to handle the entire presales workflow - from prospect research to proposal generation. The platform features real-time streaming of agent activities, persistent state management, and extensive integrations with popular CRM systems.

### Key Features

- **🤖 Multi-Agent Workflow**: Specialized agents for research, qualification, proposals, and follow-ups
- **⚡ Real-time Streaming**: Live updates of agent progress via WebSockets
- **🔗 CRM Integration**: Native support for Salesforce, HubSpot, and other major CRMs
- **📊 Advanced Analytics**: Comprehensive tracking of agent performance and business outcomes
- **🛠️ Custom Tools**: Extensible tool system for specialized presales functions
- **🔒 Enterprise Security**: SOC2-ready with comprehensive audit trails

## 🏗️ Architecture

```
Frontend (React/Vue) → Backend (FastAPI) → AI Agents (LlamaIndex) → Tools & Integrations
                              ↓
                        Database (PostgreSQL) + Cache (Redis)
```

### Agent Workflow

1. **Research Agent** - Conducts prospect and company intelligence gathering
2. **Qualification Agent** - Evaluates leads using BANT framework and custom scoring
3. **Proposal Agent** - Generates customized proposals and presentations
4. **Review Agent** - Ensures quality and compliance before delivery
5. **Follow-up Agent** - Manages nurture sequences and relationship building

## 📁 Project Structure

```
├── ai/              # AI agents and LlamaIndex workflows
├── be/              # Backend API and orchestration layer
├── fe/              # Frontend user interface
├── db/              # Database schemas and state management
├── tools/           # Custom tool implementations
├── docs/            # Architecture and API documentation
├── future_ideas/    # Expansion roadmap and concepts
└── guides/          # LlamaIndex implementation guides
```

## 🛠️ Technology Stack

### Core Technologies
- **AI Framework**: LlamaIndex 0.10+ with multi-agent workflows
- **Backend**: FastAPI with async support, WebSocket streaming
- **Frontend**: React 18+ or Vue 3 with real-time UI components
- **Database**: PostgreSQL 15+ with JSONB for flexible state storage
- **Cache**: Redis for session management and real-time data
- **Queue**: Celery for background task processing

### LlamaIndex Integration
- **Agent Patterns**: AgentWorkflow, Orchestrator, and Custom Planner support
- **Tool Ecosystem**: LlamaHub integrations + custom presales tools
- **Streaming**: Real-time agent output with progress indicators
- **State Management**: Persistent context across agent handoffs

### External Integrations
- **CRM Systems**: Salesforce, HubSpot, Microsoft Dynamics
- **Communication**: Email automation, calendar scheduling
- **Research**: Web search, company databases, social media APIs
- **Document Generation**: Proposal templates, contract automation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (recommended)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LlamaIndex-Presales
   ```

2. **Environment Setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your API keys and database credentials
   # Required: OpenAI API key, database URLs, etc.
   ```

3. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up -d
   ```

4. **Manual Setup**
   ```bash
   # Backend setup
   cd be/
   pip install -r requirements.txt
   uvicorn main:app --reload
   
   # Frontend setup (new terminal)
   cd fe/
   npm install
   npm run dev
   
   # Database setup (new terminal)
   cd db/
   # Run migration scripts
   ```

### Configuration

#### Environment Variables
```bash
# AI Configuration
OPENAI_API_KEY=your_openai_key
LLAMAINDEX_CACHE_DIR=./cache

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/presales
REDIS_URL=redis://localhost:6379

# CRM Integrations
SALESFORCE_CLIENT_ID=your_sf_client_id
SALESFORCE_CLIENT_SECRET=your_sf_secret
HUBSPOT_API_KEY=your_hubspot_key

# External APIs
TAVILY_API_KEY=your_tavily_key  # For web research
```

## 📖 Usage

### Starting a Presales Conversation

1. **Web Interface**: Navigate to the frontend application
2. **Enter Prospect Information**: Company name, contact details, initial context
3. **Agent Activation**: The system automatically starts with the Research Agent
4. **Real-time Monitoring**: Watch agents work through the qualification pipeline
5. **Review Outputs**: Generated proposals, qualification scores, and follow-up plans

### API Usage

```python
# Example: Trigger agent workflow via API
import requests

response = requests.post("/api/v1/conversations", json={
    "prospect_name": "John Smith",
    "company_name": "Acme Corp",
    "initial_context": "Interested in our enterprise solution"
})

conversation_id = response.json()["id"]

# Stream real-time updates
import websocket
ws = websocket.create_connection(f"ws://localhost:8000/ws/stream/{conversation_id}")
```

### Agent Customization

```python
# Example: Custom agent configuration
from llama_index.core.agent.workflow import FunctionAgent

custom_research_agent = FunctionAgent(
    name="CustomResearchAgent",
    description="Industry-specific research specialist",
    system_prompt="You are an expert in [INDUSTRY] research...",
    tools=[industry_database_tool, competitive_analysis_tool],
    can_handoff_to=["QualificationAgent"]
)
```

## 🔧 Development

### Component Development

Each component has its own task brief and development guidelines:

- **[Backend Development](be/TASK_BRIEF.md)**: API endpoints, agent orchestration, streaming
- **[Frontend Development](fe/TASK_BRIEF.md)**: UI components, real-time updates, dashboards
- **[AI Agent Development](ai/TASK_BRIEF.md)**: LlamaIndex workflows, agent logic, tool integration
- **[Database Design](db/TASK_BRIEF.md)**: Schema design, state management, analytics
- **[Tool Development](tools/TASK_BRIEF.md)**: Custom integrations, CRM connectors, research APIs

### Testing

```bash
# Backend tests
cd be/
pytest tests/

# Frontend tests
cd fe/
npm run test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Code Quality

```bash
# Python code formatting
black . && isort . && flake8

# TypeScript/JavaScript formatting
npm run lint && npm run format
```

## 📊 Monitoring & Analytics

### Agent Performance Metrics
- Success rates per agent type
- Average execution times
- Tool usage statistics
- Conversion rates from qualification to proposal

### Business Metrics
- Lead qualification accuracy
- Proposal acceptance rates
- Time-to-proposal generation
- Revenue impact tracking

### System Health
- API response times
- WebSocket connection stability
- Database performance
- Resource utilization

## 🔒 Security & Compliance

### Data Protection
- End-to-end encryption for sensitive data
- PII anonymization and pseudonymization
- Secure API key management with vault storage
- Audit trails for all agent actions

### Compliance Features
- GDPR compliance with data deletion rights
- SOC 2 Type II controls
- Role-based access control (RBAC)
- Activity logging and monitoring

## 🚀 Deployment

### Production Deployment

1. **Container Registry**: Push Docker images to your registry
2. **Kubernetes**: Apply manifests from `k8s/` directory
3. **Database Migrations**: Run production migrations
4. **Environment Configuration**: Set production environment variables
5. **Monitoring Setup**: Deploy observability stack

```bash
# Example Kubernetes deployment
kubectl apply -f k8s/
kubectl get pods -n presales-system
```

### Scaling Considerations

- **Horizontal Scaling**: Stateless backend services with load balancing
- **Database Scaling**: Read replicas and connection pooling
- **Agent Execution**: Distributed task processing with Celery
- **Caching**: Redis cluster for high availability

## 📚 Documentation

- **[Architecture Overview](docs/ARCHITECTURE_OVERVIEW.md)**: System design and component interactions
- **[API Documentation](docs/api/)**: Comprehensive API reference
- **[Agent Development Guide](docs/agents/)**: Creating and customizing agents
- **[Tool Development Guide](docs/tools/)**: Building custom tools and integrations
- **[Deployment Guide](docs/deployment/)**: Production deployment instructions

## 🗺️ Roadmap

### Phase 1 (Current): Core Platform
- Multi-agent workflow implementation
- Real-time streaming interface
- Basic CRM integrations
- PostgreSQL state management

### Phase 2 (3-6 months): [Advanced Features](future_ideas/EXPANSION_CONCEPTS.md)
- Voice interaction capabilities
- Advanced analytics and ML insights
- Multi-modal document analysis
- Enhanced personalization

### Phase 3 (6-12 months): Enterprise Features
- Multi-tenant architecture
- Advanced security and compliance
- API ecosystem for third-party developers
- Global expansion with localization

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow the existing code style and conventions
- Add comprehensive tests for new features
- Update documentation for any API changes
- Ensure all CI/CD checks pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

- **Documentation**: Check the `docs/` directory for detailed guides
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas
- **Email**: Contact the development team at [your-email]

## 🙏 Acknowledgments

- **LlamaIndex Team**: For the excellent multi-agent framework
- **OpenAI**: For GPT models powering the AI agents
- **Community Contributors**: For tools, integrations, and feedback

---

**Built with ❤️ using LlamaIndex and modern web technologies**