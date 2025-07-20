# CLAUDE.md - Project Context for Future Sessions

## Project Overview  
**LlamaIndex Pre-sales Multi-Agent Pipeline** - An intelligent transcript processing system that transforms customer conversations into comprehensive proposal packages, reducing proposal cycle-time by 30%.

### 🎯 **Business Vision**
Transform raw customer transcripts through a specialized 10-step agent pipeline to generate:
- Structured problem analysis
- Solution process documentation  
- Visual process diagrams (Mermaid)
- Investment proposals with roadmaps
- Customer-facing sales decks

**Primary Goal**: **30% reduction in proposal cycle-time**

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
- **AI Framework**: LlamaIndex 0.10+ with AgentWorkflow for linear pipeline orchestration
- **Frontend**: Streamlit for rapid ML/AI application development
- **LLM Provider**: OpenRouter for flexible model selection without cost escalation
- **RAG System**: Vector embeddings + Jina reranker for company knowledge base
- **Document Output**: Markdown files + Mermaid diagram generation
- **Deployment**: Local development → Cloud deployment for production

### Agent Pipeline Design (10-Step Workflow)
```
Customer Transcript
         ↓
1. Conversa (Transcript Analysis) → Structured Requirements
         ↓
2. Conny (Consultant) → Project Description  
         ↓
3. Conversa (Refinement) → Enhanced Summary v2
         ↓  
4. Conny (Zero-Knowledge Brief) → PM Handover Document
         ↓
5. ProDy (Product Manager) → 5 Document Artifacts:
   • Problem Overview (.md)
   • Process Overview (.md) 
   • Process Visualization (.md + Mermaid)
   • Investment Proposal (.md)
   • Next Steps (.md)
         ↓
6. Conny (Quality Review) → Approval/Feedback Loop
         ↓
7. System Package → Project Folder Creation
         ↓
8. RAG Knowledge Base (Always Available) → Past Solutions Integration
         ↓
9. Marketing Agent → Customer Sales Deck (.md)
         ↓
10. Streamlit UI → Document Download & Review
```

### Integration Points  
- **OpenRouter**: Multi-LLM access (GPT-4o, Claude-3.5-Sonnet, Llama-3.1-405B)
- **Knowledge Base**: Company proposals, projects, solutions (MD/PDF/PPT ingestion)
- **Document Processing**: Transcript parsing (TXT, DOCX, PDF input)
- **Output Generation**: Markdown documents, Mermaid diagrams, ZIP packages
- **Optional**: CRM integration for customer data, external hybrid databases

## Development Commands

### Common Commands for Development
```bash
# Main Streamlit Application
pip install streamlit llama-index llama-index-llms-openrouter
streamlit run streamlit_app/main.py

# Knowledge Base Setup  
python scripts/ingest_knowledge_base.py --folder ./knowledge_base

# Pipeline Testing
python scripts/test_pipeline.py --transcript sample_transcript.txt

# Document Generation
python scripts/generate_proposal.py --project "Acme Corp Digital Transform"
```

### Testing Commands
```bash
# Pipeline Integration Tests
pytest tests/test_pipeline.py

# Agent Unit Tests  
pytest tests/test_agents.py

# RAG System Tests
pytest tests/test_rag_system.py

# Document Generation Tests
pytest tests/test_document_generation.py

# Acceptance Tests (BDD/ATDD)
pytest tests/acceptance/ --verbose

# Streamlit App Tests
pytest tests/test_streamlit_app.py
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
Feature: Transcript to Proposal Pipeline
  As a sales representative
  I want to transform customer transcripts into complete proposals
  So that I can reduce proposal cycle-time by 30%

  Scenario: Complete pipeline execution
    Given I have uploaded a customer discovery call transcript
    And I have selected "gpt-4o" as the LLM model
    When I execute the pipeline
    Then Conversa should analyze the transcript and extract requirements
    And Conny should create a project description based on requirements
    And ProDy should generate 5 document artifacts
    And the Marketing Agent should create a customer sales deck
    And I should be able to download all documents as a ZIP package
    And the total processing time should be less than 5 minutes
```

### Acceptance Testing Workflow
1. **Before Implementation**: Write acceptance criteria first
2. **During Development**: Reference acceptance tests to guide implementation
3. **After Implementation**: Manually verify all acceptance scenarios
4. **Documentation**: Update acceptance tests when requirements change
5. **Handoff**: Use acceptance tests to demonstrate completed features

## Next Steps for Implementation

## Current Implementation Status

### ✅ Phase 1: React Admin Interface (COMPLETED - BONUS)
**Admin Interface** (`fe/` folder): **🎉 PRODUCTION READY**
- ✅ React + TypeScript interface for monitoring pipeline execution
- ✅ Real-time WebSocket dashboard for agent status tracking
- ✅ Document preview and management interface  
- ✅ Could serve as admin panel for reviewing generated proposals
- ✅ Comprehensive BDD/ATDD acceptance tests
- ✅ Development server running on http://localhost:5173

> **Note**: This React interface was built before understanding the true vision. It can serve as a valuable admin/monitoring dashboard, but the **main application should be Streamlit-based**.

### 🔄 Phase 2: Streamlit Pipeline Application (NEXT PRIORITY)
**Main Application**: Streamlit-based transcript processing pipeline
- 📋 Streamlit UI with model selection and configuration (see DEVELOPMENT_PLAN_v2.md)
- 📋 File upload for customer transcripts (TXT, DOCX, PDF)
- 📋 Real-time pipeline progress tracking
- 📋 Agent-specific prompt and tool configuration
- 📋 Document preview and download functionality

### 📋 Phase 3: LlamaIndex Agent Pipeline 
**10-Step Agent Workflow**: Core business logic
- 📋 **Conversa Agent**: Transcript analysis and requirement extraction
- 📋 **Conny Agent**: Business consulting and solution architecture  
- 📋 **ProDy Agent**: Product management and documentation generation
- 📋 **Marketing Agent**: Customer-facing sales deck creation
- 📋 AgentWorkflow orchestration with handoffs and state management

### 📋 Phase 4: RAG Knowledge Base & Tools
**Company Knowledge System**: 
- 📋 Vector database with company proposals, projects, solutions
- 📋 Document ingestion pipeline (MD, PDF, PPT processing)
- 📋 Jina reranker for enhanced retrieval quality
- 📋 Tagging and categorization system

**Specialized Tools**:
- 📋 Transcript processing and parsing tools
- 📋 Document generation with Markdown templates
- 📋 Mermaid diagram generation for process visualization
- 📋 RAG search and solution matching tools

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

## Epic Completion Requirements

### Mandatory Epic Visualization
**After completing each Epic**, you MUST create a comprehensive visualization document following this pattern:

1. **File Naming**: `EPIC_X_COMPLETION.md` (where X is the epic number)
2. **Content Requirements**:
   - Epic objectives and achievements summary
   - System architecture diagrams using Mermaid
   - Implementation details with component status
   - Test coverage and results
   - Technical stack and dependencies
   - File structure created
   - Integration points established
   - Success metrics and next steps

3. **Mermaid Diagram Types to Include**:
   - **Component Architecture**: Show all implemented components and their relationships
   - **Database Schema**: ER diagrams with implementation status
   - **Sequence Diagrams**: API flows and communication patterns  
   - **Pie Charts**: Test coverage, completion metrics
   - **Dependency Graphs**: Technical stack and integrations

4. **Status Indicators**: Use ✅ for completed, 🔄 for in-progress, 📋 for planned
5. **Traceability**: Link back to original requirements and forward to next epic
6. **Documentation**: Store in project root and reference in README.md

**Example Epic completion visualization**: See `EPIC_1_COMPLETION.md` for the complete template.

This ensures:
- Complete traceability of development progress
- Visual documentation for stakeholders
- Knowledge transfer for future sessions
- Architecture decision recording
- Success metric tracking

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

### Development Priorities (Vision-Aligned)
1. ✅ **Admin Interface** - **COMPLETED** (bonus React dashboard)
2. 🔄 **Streamlit Pipeline App** - **NEXT** (main user interface)
3. 📋 **10-Step Agent Workflow** - Core business logic with Conversa, Conny, ProDy
4. 📋 **RAG Knowledge Base** - Company proposal and solution repository
5. 📋 **Document Generation** - Markdown templates and Mermaid diagrams

### LlamaIndex Integration Strategy (Vision-Specific)
Based on analysis of guides in `guides/` folder + business requirements:
- **AgentWorkflow Pattern**: Linear pipeline perfect for 10-step transcript processing
- **Specialized Agents**: 
  - **Conversa**: Transcript analysis with NLP tools
  - **Conny**: Business consulting with RAG access to company knowledge
  - **ProDy**: Document generation with template engines and diagram tools
  - **Marketing Agent**: Sales deck creation with customer-facing templates
- **Streaming Events**: Real-time progress updates to Streamlit interface
- **RAG Integration**: Always-available company knowledge base for all agents
- **State Persistence**: Workflow continuity and document version management
- **OpenRouter Integration**: Flexible LLM selection per agent for optimal cost/performance

### Repository Status
- **Current**: ✅ React admin interface ready, complete vision alignment completed
- **Next**: 🔄 Streamlit pipeline application development (see DEVELOPMENT_PLAN_v2.md)
- **Vision**: ✅ True business requirements captured with 30% cycle-time reduction goal
- **Git**: All changes committed with clean history

### Quick Start Commands
```bash
# React Admin Interface (BONUS - monitoring dashboard)
cd fe/
npm install
npm run dev  # http://localhost:5173

# Main Streamlit Application (TO BE DEVELOPED)
pip install streamlit llama-index llama-index-llms-openrouter
streamlit run streamlit_app/main.py

# Development Plan
# See DEVELOPMENT_PLAN_v2.md for complete implementation strategy
# See PROJECT_VISION.md for detailed business requirements

# Knowledge Base Setup (when ready)
python scripts/ingest_knowledge_base.py --folder ./company_knowledge
```

### For the Engineer
**Priority 1**: Follow `DEVELOPMENT_PLAN_v2.md` to build the Streamlit pipeline application
**Priority 2**: Implement the 10-step agent workflow with Conversa, Conny, ProDy, Marketing agents
**Priority 3**: Integrate RAG system for company knowledge base
**Priority 4**: Use React interface as admin panel for proposal management

The React frontend we built can serve as a valuable **admin interface** for reviewing generated proposals and monitoring pipeline performance!

This CLAUDE.md provides complete context for any future development sessions on this project.