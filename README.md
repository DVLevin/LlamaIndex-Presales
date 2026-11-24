# LlamaIndex Pre-sales AI Pipeline

A local reference implementation by Dima Levin at Cone Red. Give it a sales conversation transcript and it produces a draft proposal package. A salesperson can compare the draft with the transcript, correct the scope and figures, and export the reviewed version. [Dima Levin](https://dimalevin.com) · [Cone Red](https://cone.red)

## What you can try

1. Open the sample project in Streamlit or supply your own transcript.
2. Inspect the proposed requirements and the draft documents.
3. Edit the proposal and export the package. Project state is stored in SQLite.

The published examples come from internal demo runs. For provider-backed processing, configure your own API keys using `.env.example`.

## 🎉 **Current System Capabilities**

### **✅ Complete Multi-Page Workflow**
- **💭 Input Page**: Smart content collection with transcript analysis
- **🤖 Analysis Page**: AI-powered business intelligence extraction  
- **⚡ Processing Page**: Real-time multi-agent pipeline with progress visualization
- **📋 Review Page**: Document editing interface with version control
- **📚 Projects Page**: Complete project library with search and export

### **✅ Professional Document Generation**  
- **Problem Overview** with customer-specific analysis
- **Solution Approach** tailored to customer requirements
- **Process Visualization** with Mermaid diagrams
- **Investment Proposal** with ROI calculations
- **Sales deck draft** for the salesperson to review

### **✅ Project Management System**
- **Automatic Saving**: All work persisted in SQLite database
- **Search & Filter**: Full-text search across projects and content
- **Export System**: Complete ZIP packages with all documents
- **Version Control**: Track changes and document evolution
- **Resume Capability**: Continue work from any workflow stage

### What a reviewer should check

Compare the draft with the transcript. Check names, requirements, scope, budget assumptions and any customer-facing commitments. The salesperson decides what can be shared.

---

## Quick start

### **1. Installation & Setup**
```bash
# Clone and setup
git clone https://github.com/DVLevin/LlamaIndex-Presales.git
cd LlamaIndex-Presales/
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies  
pip install -r streamlit_app/requirements.txt

# Launch application
streamlit run streamlit_app/main.py
```

### **2. Access Application**
**🌐 Open**: http://localhost:8501

### **3. Quick Demo Test**
1. **Click "🎭 Demo Mode"** in the sidebar
2. **Watch the workflow**: Complete sample data loads
3. **Generate Proposal**: Click "🚀 Generate Proposal Package" 
4. **Review results**: Open the draft documents and compare them with the sample input
5. **Check Projects**: See saved project in Projects page

The sample run produces a draft proposal package you can inspect in the review page.

---

## 📊 **System Architecture**

### **🎯 Multi-Page Streamlit Application** (`streamlit_app/`)
```
streamlit_app/
├── main.py                     # Primary application entry point
├── config.py                   # Configuration and API key management
├── components/                 # UI components and business logic
│   ├── smart_input.py         # Content collection and analysis
│   ├── pipeline_progress.py   # Real-time processing visualization
│   ├── document_preview.py    # Generated document management
│   └── dynamic_pipeline.py    # AI agent orchestration
├── pages/                      # Multi-page workflow implementation
│   ├── input_page.py          # Content input and templates
│   ├── analysis_page.py       # Business intelligence extraction
│   ├── processing_page.py     # Multi-agent pipeline execution
│   ├── review_page.py         # Document editing and finalization
│   └── projects_page.py       # Project library and management
└── storage/                    # Data persistence layer
    └── project_manager.py     # SQLite database operations
```

### **🤖 AI Agent Pipeline** (`ai/src/`)
```
ai/src/
├── agents/                     # Specialized AI agents
│   ├── conversa_agent.py     # Transcript analysis and requirements
│   ├── conny_agent.py        # Business consulting and strategy  
│   ├── prody_agent.py        # Document generation and templates
│   └── marketing_agent.py    # Sales deck and presentation creation
├── workflow.py                # LlamaIndex agent orchestration
├── rag_system.py             # Knowledge base and document retrieval
├── llm_integration.py        # OpenRouter API integration
└── jina_integration.py       # Embeddings and document search
```

### **🧪 Comprehensive Testing Suite** (`tests/`)
```
tests/
├── acceptance/                 # Business acceptance tests (BDD)
│   ├── core_workflow.feature # End-to-end business process
│   ├── navigation_and_progress.feature # Multi-page flow
│   ├── project_management.feature # Data persistence
│   └── business_value.feature # illustrative business scenarios
└── validation/                # System validation tests
    ├── core_validation.py    # Programmatic system tests
    └── quick_system_test.py   # Rapid functionality verification
```

---

## How the workflow handles an illustrative transcript

### **Step 1: Input Collection** 💭
```
Customer Discovery Call Transcript:
Customer: "Our inventory system is causing delays..."
Sales Rep: "What specific challenges are you facing?"
Customer: "Manual processes and lack of real-time visibility..."
```

### **Step 2: AI Analysis** 🤖
```json
{
  "customer": "Acme Manufacturing Corp",
  "industry": "manufacturing",
  "pain_points": ["manual processes", "inventory delays", "visibility"],
  "stakeholders": ["CTO", "VP Operations"],
  "budget_indicators": ["$500K approved"],
  "timeline": ["Q2 2025 launch deadline"]
}
```

### **Step 3: Agent Processing** ⚡
- **Conversa**: Extract detailed requirements and pain points
- **Conny**: Develop business strategy and solution approach
- **ProDy**: Generate professional documents with customer details
- **Marketing**: Create customer-facing sales presentation

### **Step 4: Professional Output** 📋
- **Problem Overview**: Customer-specific analysis and requirements
- **Solution Approach**: Tailored recommendations with implementation roadmap  
- **Investment Proposal**: ROI calculations and budget recommendations
- **Sales Deck**: Draft presentation for the salesperson to check

---

## 📱 **User Interface Highlights**

### **LazyFlow Design Philosophy**
- **Single-tap generation**: All processing with one button click
- **Smart defaults**: System configured for immediate use
- **Clear progress tracking**: Always know where you are in the process
- **Professional output**: Editable drafts for review

### **Key Features**
- **🎭 Demo Mode**: Instant demonstration with realistic sample data
- **📊 Progress Tracking**: Visual indication of workflow completion
- **💾 Auto-Save**: All work automatically persisted in database
- **📦 Export System**: Complete ZIP packages for easy sharing
- **🔍 Project Search**: Find and reuse past proposals and templates

---

## 🧪 **Validation & Testing**

### Functional checks

The validation scripts cover project storage and retrieval, input detection, document generation, and workflow state.

### **Business Acceptance Tests (Gherkin BDD)**
- **`core_workflow.feature`**: End-to-end customer transcript to proposal
- **`navigation_and_progress.feature`**: Multi-page flow with progress tracking
- **`project_management.feature`**: Data persistence and project operations
- **`document_editing.feature`**: Content management with version control
- **`business_value.feature`**: Illustrative business-value expectations for discussion

See the [acceptance test guide](tests/acceptance/README.md) for the manual workflow checks.

### Measuring a real engagement

To estimate time saved, use the same transcripts, scope and quality criteria for both the manual and assisted workflow. Measure each proposal through final review, including corrections and rework. Any savings estimate would also need observed usage and operating costs. The demo has no published client benchmark.

---

## ⚙️ **Configuration & API Keys**

### **Required API Keys**
- **OpenRouter**: `sk-or-v1-...` for LLM processing
- **Jina AI**: `jina_...` for embeddings and document search

### **Configuration Options**
- **Model Selection**: Choose LLM models per use case
- **Prompt Management**: Customize agent behavior and templates  
- **Storage Settings**: Configure project retention and export formats

**Setup**: Navigate to Configurations → API Keys in the application

---

## 📚 **Documentation & Support**

### **Current Documentation** ✅
- **`PLATFORM_VALIDATION_COMPLETE.md`**: Complete system validation and capabilities
- **`SIMPLE_TEST_GUIDE.md`**: Quick 5-minute system validation
- **`CLAUDE.md`**: Complete project context for AI development sessions
- **`tests/acceptance/README.md`**: Comprehensive testing guide

### **Architecture Documentation**
- **`docs/epic_completions/`**: Visual development milestone documentation
- **`docs/architecture/`**: System design and technical specifications  

### **Historical Context** 📁
- **`docs_archive/`**: Previous development phases and design evolution
- **`docs_archive/README.md`**: **Agentic Navigation Guide** for Claude agents
- **Important**: Use archive navigation guide to understand what docs are outdated vs current

**⚠️ For Future Claude Sessions**: The `docs_archive/README.md` contains a comprehensive decision tree and status guide for all historical documentation. This prevents future agents from using outdated information and provides clear guidance on what references to trust for current system implementation.

---

## 🎯 **Next Steps & Roadmap**

### **Phase 1: Local demonstration**
- Multi-page Streamlit application with professional UI
- Complete project management with SQLite persistence
- Workflow validation scripts and acceptance scenarios
- Demo mode for immediate system demonstration

### **Phase 2: AI Integration** 🔄 NEXT PRIORITY  
- Expand integration of provider-backed agents in the demo workflow
- Integrate OpenRouter API for live LLM processing
- Implement RAG knowledge base for organizational learning
- Real-time streaming updates during agent execution

### **Phase 3: Enterprise Features** 📋 FUTURE
- CRM integration (Salesforce, HubSpot)
- Multi-tenant support with company branding
- Advanced analytics and success metrics
- API access for external integrations

---

## Try the workflow

Run the application locally, open the sample project, and review the draft against the transcript. Try changing a requirement in the input and see which parts of the proposal need to be checked again.

**Application URL**: http://localhost:8501 (after running `streamlit run streamlit_app/main.py`)
