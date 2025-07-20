# LlamaIndex Pre-sales Pipeline - Development Plan v2.0
## Aligned with True Business Vision

> **Business Goal**: 30% reduction in proposal cycle-time through intelligent transcript processing

---

## 🎯 Architecture Overview

### Core Technology Stack:
- **Frontend**: Streamlit (fast ML/AI app development)
- **Backend**: LlamaIndex AgentWorkflow (10-step pipeline)
- **RAG System**: Vector embeddings + Jina reranker
- **LLM Provider**: OpenRouter (flexible model selection)
- **Document Storage**: File system + vector database
- **Output Format**: Markdown files + Mermaid diagrams

---

## 🚀 Phase 1: Streamlit Foundation & Core Pipeline (2-3 weeks)

### Epic 1: Streamlit Application Setup
**Goal**: Create the main user interface with model configuration

#### Features:
```python
# Main Streamlit structure
import streamlit as st
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.openrouter import OpenRouter

# Sidebar: Configuration
st.sidebar.title("Pipeline Configuration")
selected_model = st.sidebar.selectbox("Select LLM Model", ["gpt-4o", "claude-3.5-sonnet", "llama-3.1-405b"])
api_key = st.sidebar.text_input("OpenRouter API Key", type="password")

# Main area: Workflow steps
st.title("Pre-sales Proposal Pipeline")
uploaded_transcript = st.file_uploader("Upload Customer Transcript", type=['txt', 'docx', 'pdf'])
```

#### Core Components:
- **Model Selection UI**: OpenRouter integration with dropdown
- **API Key Management**: Secure credential handling
- **File Upload**: Transcript processing (txt, docx, pdf)
- **Progress Tracking**: Real-time pipeline status
- **Configuration Panels**: Agent-specific settings

#### Success Criteria:
- Streamlit app runs locally
- OpenRouter integration working
- File upload processing transcripts
- Basic UI for all 10 pipeline steps

### Epic 2: LlamaIndex Agent Pipeline Implementation
**Goal**: Build the core 10-step workflow with named agents

#### Agent Implementation Strategy:
```python
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent

# Step 1: Conversa (Transcript Processor)
conversa_agent = FunctionAgent(
    name="Conversa", 
    description="Transcript processing and analysis specialist",
    system_prompt="""You are Conversa, a transcript analysis expert. 
    Extract key requirements, pain points, stakeholders, and business context 
    from customer conversations. Focus on what the customer REALLY needs.""",
    tools=[transcript_parser_tool, requirement_extractor_tool],
    can_handoff_to=["Conny"]
)

# Step 2: Conny (Consultant)  
conny_agent = FunctionAgent(
    name="Conny",
    description="Business consultant and solution architect", 
    system_prompt="""You are Conny, a senior business consultant. 
    Based on transcript analysis, identify the optimal project approach 
    and solution architecture. Create clear project descriptions.""",
    tools=[rag_search_tool, solution_matcher_tool, competitive_analysis_tool],
    can_handoff_to=["Conversa", "ProDy"]
)

# Step 3: ProDy (Product Manager)
prody_agent = FunctionAgent(
    name="ProDy", 
    description="Product manager and documentation specialist",
    system_prompt="""You are ProDy, an expert product manager. 
    Create comprehensive project documentation including problem analysis, 
    process design, visualizations, and investment proposals.""",
    tools=[document_generator_tool, mermaid_diagram_tool, roadmap_planner_tool],
    can_handoff_to=["Conny"]
)

# Marketing Agent (Final step)
marketing_agent = FunctionAgent(
    name="MarketingAgent",
    description="Sales deck creation specialist",
    system_prompt="""You are the Marketing Agent. Create compelling, 
    customer-facing sales presentations using approved project documents. 
    Focus on value proposition and business benefits.""",
    tools=[sales_deck_template_tool, presentation_builder_tool]
)

# Pipeline orchestration
pipeline_workflow = AgentWorkflow(
    agents=[conversa_agent, conny_agent, prody_agent, marketing_agent],
    initial_agent="Conversa",
    verbose=True
)
```

#### Pipeline Flow:
1. **Conversa**: Transcript → Structured Analysis
2. **Conny**: Analysis → Project Description  
3. **Conversa**: Transcript + Description → Enhanced Summary
4. **Conny**: Summary v2 → Zero-Knowledge Brief
5. **ProDy**: Brief → 5 Document Artifacts
6. **Conny**: Review Documents → Approval/Feedback
7. **System**: Package & Store Approved Documents
8. **Marketing**: Documents → Customer Sales Deck

---

## 🤖 Phase 2: Specialized Tools Development (2-3 weeks)

### Epic 3: Agent-Specific Tools

#### Conversa Tools:
```python
# Transcript processing tools
class TranscriptParserTool(BaseToolSpec):
    """Extract structured data from conversation transcripts"""
    
    def parse_transcript(self, transcript_text: str) -> Dict:
        # Extract speakers, topics, requirements, pain points
        return {
            "stakeholders": [...],
            "requirements": [...], 
            "pain_points": [...],
            "business_context": "...",
            "decision_criteria": [...]
        }

class RequirementExtractorTool(BaseToolSpec):
    """Identify functional and non-functional requirements"""
    
    def extract_requirements(self, analysis: Dict) -> List[str]:
        # Process analysis into clear requirements
        pass
```

#### Conny Tools:
```python
# Consultant analysis tools
class SolutionMatcherTool(BaseToolSpec):
    """Match requirements to company solutions via RAG"""
    
    def find_similar_projects(self, requirements: List[str]) -> List[Dict]:
        # RAG search through company knowledge base
        pass

class CompetitiveAnalysisTool(BaseToolSpec):
    """Analyze competitive landscape and positioning"""
    
    def analyze_competition(self, project_description: str) -> Dict:
        # Market analysis and differentiation
        pass
```

#### ProDy Tools:
```python
# Documentation generation tools
class DocumentGeneratorTool(BaseToolSpec):
    """Generate structured markdown documents"""
    
    def generate_problem_overview(self, brief: Dict) -> str:
        # Create problem overview markdown
        pass
    
    def generate_process_overview(self, brief: Dict) -> str:
        # Create solution process markdown
        pass

class MermaidDiagramTool(BaseToolSpec):
    """Generate process visualization diagrams"""
    
    def create_process_diagram(self, old_process: str, new_process: str) -> str:
        # Generate mermaid diagram code
        return """
        graph TD
        A[Current Process] --> B[Pain Point 1]
        C[New Process] --> D[Solution]
        """
```

### Epic 4: RAG Knowledge Base System
**Goal**: Company knowledge base with intelligent retrieval

#### Components:
```python
# RAG system setup
from llama_index.core import VectorStoreIndex, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.rerank.jina import JinaRerank

# Knowledge base ingestion
class CompanyKnowledgeBase:
    def __init__(self):
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
        self.reranker = JinaRerank(model="jina-reranker-v1-base-en")
        self.index = None
    
    def ingest_documents(self, document_folder: str):
        """Process MD, PDF, PPT files into vector store"""
        documents = []
        # Load and process files
        self.index = VectorStoreIndex.from_documents(
            documents,
            embed_model=self.embed_model
        )
    
    def search_similar_solutions(self, query: str, top_k: int = 5) -> List[Dict]:
        """Find relevant past projects and solutions"""
        results = self.index.as_retriever(similarity_top_k=10).retrieve(query)
        # Rerank with Jina
        reranked = self.reranker.postprocess_nodes(results, query_str=query)
        return reranked[:top_k]
```

---

## 🗄️ Phase 3: Document Generation & Management (2 weeks)

### Epic 5: Template System & Document Output

#### Document Templates:
```markdown
# Document Templates Structure

## 1. Problem Overview Template
- Executive Summary
- Current State Analysis  
- Pain Points & Challenges
- Business Impact Assessment

## 2. Process Overview Template
- Solution Approach
- Implementation Strategy
- Technology Stack
- Success Criteria

## 3. Process Visualization Template
- Current Process Flow (Mermaid)
- Proposed Process Flow (Mermaid)  
- Comparison Analysis
- Efficiency Gains

## 4. Investment Proposal Template
- Product Roadmap
- Resource Requirements
- Timeline & Milestones
- Budget Estimation
- ROI Analysis

## 5. Next Steps Template
- Immediate Actions
- Decision Points
- Stakeholder Involvement
- Risk Mitigation
```

#### File Management System:
```python
class ProposalManager:
    def __init__(self, base_path: str = "./proposals"):
        self.base_path = base_path
    
    def create_project_folder(self, project_name: str) -> str:
        """Create timestamped project folder"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{project_name}_{timestamp}"
        folder_path = os.path.join(self.base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def save_document(self, folder_path: str, doc_type: str, content: str):
        """Save generated markdown document"""
        filename = f"{doc_type.lower().replace(' ', '_')}.md"
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'w') as f:
            f.write(content)
    
    def create_download_package(self, folder_path: str) -> str:
        """Create zip package for download"""
        # Implementation for zip creation
        pass
```

---

## 📊 Phase 4: Advanced Features & UI Enhancement (2 weeks)

### Epic 6: Streamlit UI Polish
**Goal**: Professional interface with all required features

#### Enhanced UI Components:
```python
# Advanced Streamlit interface
def render_agent_configuration():
    """Agent-specific prompt and tool configuration"""
    st.subheader("Agent Configuration")
    
    # Tabbed interface for each agent
    conversa_tab, conny_tab, prody_tab, marketing_tab = st.tabs([
        "Conversa", "Conny", "ProDy", "Marketing"
    ])
    
    with conversa_tab:
        st.text_area("Conversa System Prompt", height=200)
        st.multiselect("Conversa Tools", ["Transcript Parser", "Requirement Extractor"])
    
    # Similar for other agents...

def render_pipeline_progress():
    """Real-time pipeline execution progress"""
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    
    # Update progress as pipeline executes
    for step, status in pipeline_execution:
        progress_bar.progress(step / 10)
        status_placeholder.text(f"Step {step}: {status}")

def render_document_preview():
    """Preview and download generated documents"""
    st.subheader("Generated Documents")
    
    doc_tabs = st.tabs(["Problem Overview", "Process Overview", "Visualization", "Investment", "Next Steps"])
    
    for tab, doc in zip(doc_tabs, generated_docs):
        with tab:
            st.markdown(doc.content)
            st.download_button(
                label=f"Download {doc.title}",
                data=doc.content,
                file_name=f"{doc.title}.md"
            )
```

### Epic 7: Proposal Review Mode
**Goal**: Analyze existing proposals for improvement

#### Review Pipeline:
```python
def proposal_review_mode():
    """Review existing proposals using pipeline logic"""
    st.subheader("Proposal Review Mode")
    
    uploaded_proposal = st.file_uploader("Upload Existing Proposal", type=['md', 'pdf', 'docx'])
    
    if uploaded_proposal:
        # Use Conny + ProDy agents to analyze
        analysis = review_proposal_pipeline.run(uploaded_proposal)
        
        st.subheader("Improvement Recommendations")
        st.markdown(analysis.recommendations)
        
        st.subheader("Missing Elements")
        st.markdown(analysis.missing_elements)
        
        st.subheader("Suggested Enhancements")
        st.markdown(analysis.enhancements)
```

---

## 🔧 Phase 5: Production Features (1-2 weeks)

### Epic 8: Performance & Reliability
- **Caching**: Streamlit session state for pipeline results
- **Error Handling**: Graceful failure recovery
- **Logging**: Comprehensive audit trail
- **Performance**: Optimize RAG queries and LLM calls

### Epic 9: Advanced RAG Features
- **Tagging System**: Categorize knowledge base content
- **Graph RAG**: Optional hybrid database integration
- **Memory Chains**: Learn from successful patterns
- **Analytics**: Track proposal success rates

---

## 📈 Success Metrics & Validation

### Primary KPI: **30% Proposal Cycle-Time Reduction**
- **Before**: Manual proposal creation time
- **After**: Automated pipeline + review time
- **Target**: Measurable 30% improvement

### Quality Metrics:
- **Proposal Acceptance Rate**: Track win/loss ratio
- **Client Satisfaction**: Feedback on proposal quality
- **Internal Efficiency**: Reduce manual review cycles
- **Knowledge Reuse**: Percentage of content from RAG system

### Technical Metrics:
- **Pipeline Success Rate**: >95% completion without errors
- **Response Time**: <5 minutes for full proposal generation
- **RAG Relevance**: >80% relevant knowledge base matches
- **User Adoption**: Track active usage and session length

---

## 🛠️ Development Environment Setup

### Required Dependencies:
```bash
# Core requirements
pip install streamlit
pip install llama-index
pip install llama-index-llms-openrouter
pip install llama-index-embeddings-huggingface
pip install llama-index-rerank-jina

# Document processing
pip install python-docx PyPDF2 python-pptx
pip install markdown

# Additional utilities
pip install python-dotenv
pip install pandas plotly  # For analytics
```

### Project Structure:
```
pre-sales-pipeline/
├── streamlit_app/
│   ├── main.py                 # Main Streamlit application
│   ├── config.py              # Configuration management
│   └── components/            # UI components
├── agents/
│   ├── conversa.py            # Transcript Processor Agent
│   ├── conny.py               # Consultant Agent  
│   ├── prody.py               # Product Manager Agent
│   └── marketing.py           # Marketing Deck Agent
├── tools/
│   ├── transcript_tools.py    # Conversa tools
│   ├── consulting_tools.py    # Conny tools
│   ├── documentation_tools.py # ProDy tools
│   └── rag_tools.py           # RAG system tools
├── templates/
│   ├── problem_overview.md    # Document templates
│   ├── process_overview.md
│   ├── investment_proposal.md
│   └── sales_deck.md
├── knowledge_base/            # Company documents
├── proposals/                 # Generated proposals
└── tests/
    └── acceptance/            # BDD tests for pipeline
```

---

## 🚀 Getting Started for Engineer

### Step 1: Environment Setup (30 minutes)
```bash
git clone <repository>
cd pre-sales-pipeline
pip install -r requirements.txt
streamlit run streamlit_app/main.py
```

### Step 2: Basic Pipeline (Day 1-2)
- Streamlit app with file upload
- Basic AgentWorkflow with 4 agents
- Simple document generation

### Step 3: RAG Integration (Day 3-5)
- Knowledge base setup
- Vector embedding pipeline
- RAG search integration

### Step 4: Document Templates (Day 6-7)
- Markdown template system
- Mermaid diagram generation
- File download functionality

### Step 5: Polish & Test (Day 8-10)
- UI refinements
- Error handling
- Acceptance testing

This plan transforms your brilliant business vision into a concrete development roadmap that will deliver measurable ROI through proposal automation!