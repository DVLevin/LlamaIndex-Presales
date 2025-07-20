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
├── fe/                    # ✅ React Admin Interface (COMPLETED)
├── DEVELOPMENT_PLAN_v2.md # 📋 Current implementation guide
├── PROJECT_VISION.md      # 🎯 Business requirements
├── CLAUDE.md             # 🤖 Project context for AI sessions
├── AGENT_SPECIFICATIONS.md # 🤖 Agent personalities and tools
├── guides/               # 📚 LlamaIndex implementation patterns
├── ai/                   # 📋 Agent implementations (TO BE BUILT)
├── be/                   # 📋 Backend orchestration (TO BE BUILT)
├── tools/                # 📋 Custom tool implementations (TO BE BUILT)
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
- **Visualization**: [EPIC_1_COMPLETION.md](./EPIC_1_COMPLETION.md)  
- **Components**: FastAPI server, WebSocket manager, database models, testing framework
- **Achievement**: Robust backend foundation with 14/14 tests passing
- **Integration**: OpenRouter + Jina AI configured, PostgreSQL schema implemented

### 🔄 Epic 2: LlamaIndex Agent Pipeline (NEXT)
- **Focus**: Multi-agent workflow with Conversa, Conny, ProDy, Marketing agents
- **Integration**: LlamaIndex AgentWorkflow + OpenRouter LLM + Jina AI embeddings
- **Goal**: 10-step transcript-to-proposal automation pipeline

## 📖 Key Documentation

**For Development**: 
- **DEVELOPMENT_PLAN_v2.md** - Current implementation strategy
- **PROJECT_VISION.md** - Business requirements and 10-step pipeline
- **AGENT_SPECIFICATIONS.md** - Agent personalities and tool requirements

**For Context**:
- **CLAUDE.md** - Complete project context for AI development sessions
- **guides/** - LlamaIndex patterns for multi-agent workflows, streaming, OpenRouter

## 🎯 Next Steps

1. **Follow DEVELOPMENT_PLAN_v2.md** - Authoritative implementation guide
2. **Build Streamlit Pipeline App** - Main user interface for transcript processing
3. **Implement 10-Step Agent Workflow** - Core business automation logic
4. **Add RAG Knowledge Base** - Company proposal and solution repository

## 💡 Key Insight

This project evolved from a generic multi-agent chat system to a **specialized transcript-to-proposal automation tool**. The React frontend serves as an admin interface, while the main business value comes from the **Streamlit-based pipeline application** that achieves the 30% cycle-time reduction goal.

**Business Impact**: Automated transformation of customer conversations into professional proposal packages.