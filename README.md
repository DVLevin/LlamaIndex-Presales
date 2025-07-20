# LlamaIndex Presales AI System

**Transform customer conversations into comprehensive proposal packages, reducing proposal cycle-time by 30%.**

## 🎯 Business Vision

An intelligent **10-step agent pipeline** that processes customer discovery call transcripts and generates:
- Structured problem analysis
- Solution process documentation  
- Visual process diagrams (Mermaid)
- Investment proposals with roadmaps
- Customer-facing sales decks

## 🚀 Current Status

### ✅ **Phase 1: React Admin Interface (COMPLETED)**
- **Production-ready** React + TypeScript dashboard (`fe/` folder)
- Real-time WebSocket monitoring and agent status tracking
- Can serve as admin panel for reviewing generated proposals
- Run: `cd fe/ && npm install && npm run dev`

### 🔄 **Phase 2: Streamlit Pipeline Application (NEXT PRIORITY)**
**Main Application**: Transcript-to-proposal automation
- Streamlit UI with OpenRouter model selection
- File upload for customer transcripts (TXT, DOCX, PDF)
- Real-time pipeline progress tracking  
- Document preview and download functionality

### 📋 **Phase 3: 10-Step Agent Workflow**
**Core Business Logic** using LlamaIndex AgentWorkflow:
1. **Conversa**: Transcript analysis → Structured requirements
2. **Conny**: Business consulting → Project description
3. **ProDy**: Document generation → 5 artifacts
4. **Marketing Agent**: Customer sales deck creation

## 📁 Project Structure

```
LlamaIndex-Presales/
├── ai/                    # 🔄 AI Agents & LLM Integration (IN PROGRESS)
│   ├── src/agents/        # Agent implementations (Conversa, Conny, ProDy, etc.)
│   └── src/               # LLM and Jina AI integration services
├── be/                    # ✅ Backend API & WebSocket Server (COMPLETED)
│   ├── src/               # FastAPI application and database models
│   └── tests/             # Backend unit tests
├── fe/                    # ✅ React Admin Interface (COMPLETED)
│   ├── src/components/    # React components and dashboard
│   └── tests/acceptance/  # BDD acceptance tests
├── docs/                  # 📚 Project Documentation
│   ├── architecture/      # Technical architecture and system design
│   ├── epic_completions/  # Epic completion visualizations
│   └── plans/             # Development plans and roadmaps
├── prompts/               # 🎯 Customizable Agent Prompts
│   ├── agents/            # Individual agent behavior definitions
│   ├── templates/         # Document templates (task briefs, visions)
│   └── tools/             # Analysis tools (requirements, stakeholders)
├── tests/integration/     # 🧪 Integration Tests
├── guides/                # 📚 LlamaIndex implementation patterns
├── tools/                 # 📋 Custom tool implementations (TO BE BUILT)
└── to_delete/            # 🗑️ Outdated documentation
```

## 🛠️ Quick Start

### Admin Interface (Monitoring Dashboard)
```bash
cd fe/
npm install
npm run dev  # http://localhost:5173
```

### Main Pipeline Application (Next to Build)
```bash
# Install dependencies
pip install streamlit llama-index llama-index-llms-openrouter

# Run main application (when implemented)
streamlit run streamlit_app/main.py
```

## 📊 Epic Completion Status

### ✅ Epic 1: Backend Foundation (COMPLETED)
- **Visualization**: [EPIC_1_COMPLETION.md](./docs/epic_completions/EPIC_1_COMPLETION.md)  
- **Components**: FastAPI server, WebSocket manager, database models, testing framework
- **Achievement**: Robust backend foundation with 14/14 tests passing
- **Integration**: OpenRouter + Jina AI configured, PostgreSQL schema implemented

### 🔄 Epic 2: LlamaIndex Agent Pipeline (IN PROGRESS)
- **Plan**: [EPIC_2_PLAN.md](./docs/plans/EPIC_2_PLAN.md)
- **Progress**: OpenRouter LLM + Jina AI integration ✅, Agent framework ✅, Prompts system ✅
- **Focus**: Multi-agent workflow with Conversa, Conny, ProDy, Preston, Marketing agents
- **Next**: Complete workflow orchestration and backend integration

## 📖 Key Documentation

**For Development**: 
- **[DEVELOPMENT_PLAN_v2.md](./docs/plans/DEVELOPMENT_PLAN_v2.md)** - Current implementation strategy
- **[PROJECT_VISION.md](./PROJECT_VISION.md)** - Business requirements and 10-step pipeline
- **[AGENT_SPECIFICATIONS.md](./AGENT_SPECIFICATIONS.md)** - Agent personalities and tool requirements

**For Architecture**:
- **[TECHNICAL_ARCHITECTURE.md](./docs/architecture/TECHNICAL_ARCHITECTURE.md)** - Complete system design with diagrams
- **[RAG_ARCHITECTURE.md](./docs/architecture/RAG_ARCHITECTURE.md)** - Knowledge base and vector system design

**For Customization**:
- **[prompts/README.md](./prompts/README.md)** - Guide to customizing agent behavior for your company
- **[prompts/agents/](./prompts/agents/)** - Individual agent prompts (Conversa, Conny, ProDy, etc.)

**For Context**:
- **[CLAUDE.md](./CLAUDE.md)** - Complete project context for AI development sessions
- **[guides/](./guides/)** - LlamaIndex patterns for multi-agent workflows, streaming, OpenRouter

## 🎯 Next Steps

1. **Customize Agent Prompts** - Add your company-specific prompts in [prompts/agents/](./prompts/agents/)
2. **Complete Agent Workflow** - Finish ProDy, Preston, Marketing agents and workflow orchestration  
3. **Build Streamlit Pipeline App** - Main user interface for transcript processing
4. **Add RAG Knowledge Base** - Company proposal and solution repository

## 💡 Key Insight

This project evolved from a generic multi-agent chat system to a **specialized transcript-to-proposal automation tool**. The React frontend serves as an admin interface, while the main business value comes from the **Streamlit-based pipeline application** that achieves the 30% cycle-time reduction goal.

**Business Impact**: Automated transformation of customer conversations into professional proposal packages.