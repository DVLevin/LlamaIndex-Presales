"""
Mermaid Diagram Renderer for Streamlit
HTML-based rendering without dependency conflicts
"""
import streamlit as st
from typing import Optional
import base64


def render_mermaid_diagram(mermaid_code: str, height: int = 400, key: Optional[str] = None):
    """
    Render Mermaid diagram using HTML/JavaScript
    
    Args:
        mermaid_code: Mermaid diagram code
        height: Height of the diagram container in pixels
        key: Unique key for the component
    """
    
    # Create unique ID for the diagram
    import random, string
    diagram_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # HTML template for Mermaid rendering
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>
    </head>
    <body>
        <div id="mermaid-{diagram_id}" style="text-align: center; padding: 20px;">
            <pre class="mermaid">
{mermaid_code}
            </pre>
        </div>
        
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'neutral',
                themeVariables: {{
                    primaryColor: '#667eea',
                    primaryTextColor: '#333333',
                    primaryBorderColor: '#764ba2',
                    lineColor: '#333333',
                    sectionBkgColor: '#f8f9fa',
                    altSectionBkgColor: '#e9ecef',
                    gridColor: '#e1e5e9',
                    secondaryColor: '#f1f3f4',
                    tertiaryColor: '#ffffff'
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Render using HTML component
    st.components.v1.html(html_template, height=height, scrolling=False)


def render_mermaid_with_fallback(mermaid_code: str, title: str = "", height: int = 400, key: Optional[str] = None):
    """
    Render Mermaid diagram with code fallback
    
    Args:
        mermaid_code: Mermaid diagram code
        title: Optional title for the diagram
        height: Height of the diagram container
        key: Unique key for the component
    """
    
    if title:
        st.markdown(f"**{title}**")
    
    # Try to render diagram
    try:
        render_mermaid_diagram(mermaid_code, height=height, key=key)
    except Exception as e:
        # Fallback to code display
        st.warning("⚠️ Diagram rendering unavailable - showing code:")
        st.code(mermaid_code, language="mermaid")


def create_pipeline_flow_diagram() -> str:
    """Create the main pipeline flow diagram"""
    
    return """
graph TD
    A[📄 Customer Transcript] --> B[🎯 Conversa Agent]
    B -->|"Requirements<br/>Analysis"| C[🏗️ Conny Agent]
    C -->|"Business<br/>Consultation"| D[📋 ProDy Agent]
    D -->|"Document<br/>Generation"| E[🎨 Marketing Agent]
    E -->|"Sales Deck<br/>Creation"| F[📦 Proposal Package]
    
    G[📚 Company<br/>Knowledge] -.->|"Past Solutions"| C
    G -.->|"Templates"| D
    G -.->|"Best Practices"| E
    
    H[🤖 AI Models] -.->|"OpenRouter LLM"| B
    H -.->|"Jina AI Search"| C
    H -.->|"Document AI"| D
    
    classDef startEnd fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef agent fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef support fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class A,F startEnd
    class B,C,D,E agent
    class G,H support
    """


def create_system_architecture_diagram() -> str:
    """Create system architecture diagram"""
    
    return """
graph TB
    subgraph "User Interface"
        UI[Streamlit App]
        SIDEBAR[Navigation Sidebar]
    end
    
    subgraph "AI Processing Pipeline"
        CONV[Conversa Agent<br/>Transcript Analysis]
        CONN[Conny Agent<br/>Business Consulting]
        PROD[ProDy Agent<br/>Document Generation]
        MARK[Marketing Agent<br/>Sales Deck]
    end
    
    subgraph "Data Layer"
        TRANS[Transcript Storage]
        DOCS[Document Templates]
        KNOW[Knowledge Base]
        OUTPUT[Generated Documents]
    end
    
    subgraph "External Services"
        OR[OpenRouter API<br/>LLM Models]
        JINA[Jina AI<br/>Embeddings & Search]
    end
    
    UI --> CONV
    SIDEBAR --> UI
    
    CONV --> CONN
    CONN --> PROD
    PROD --> MARK
    
    CONV <--> TRANS
    PROD <--> DOCS
    CONN <--> KNOW
    MARK --> OUTPUT
    
    CONV -.-> OR
    CONN -.-> JINA
    PROD -.-> OR
    MARK -.-> OR
    
    classDef ui fill:#e3f2fd,stroke:#1565c0
    classDef agent fill:#e8f5e8,stroke:#2e7d32
    classDef data fill:#fce4ec,stroke:#c2185b
    classDef external fill:#fff3e0,stroke:#f57c00
    
    class UI,SIDEBAR ui
    class CONV,CONN,PROD,MARK agent
    class TRANS,DOCS,KNOW,OUTPUT data
    class OR,JINA external
    """


def create_user_flow_diagram() -> str:
    """Create user flow diagram"""
    
    return """
graph LR
    A[👤 User] --> B[📋 About Section]
    B --> C[📁 Upload Transcript]
    C --> D[🎯 Proposals Section]
    D --> E[🚀 Generate Package]
    E --> F[📊 Monitor Progress]
    F --> G[📄 Review Documents]
    G --> H[💾 Download Package]
    
    I[⚙️ Configurations] -.->|"Setup"| D
    J[🔧 Advanced Settings] -.->|"Customize"| E
    
    classDef user fill:#ffecb3,stroke:#ff8f00,stroke-width:2px
    classDef process fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef config fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    
    class A user
    class B,C,D,E,F,G,H process
    class I,J config
    """


def render_interactive_pipeline_diagram():
    """Render the main interactive pipeline diagram"""
    
    st.markdown("### 🔄 **AI Pipeline Architecture**")
    
    # Main pipeline flow
    render_mermaid_with_fallback(
        create_pipeline_flow_diagram(),
        title="10-Step Intelligent Processing Pipeline",
        height=500,
        key="main_pipeline"
    )
    
    # Benefits summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⏱️ Processing Time", "3-7 min", "vs 2-4 hours manual")
    
    with col2:
        st.metric("📄 Documents Generated", "6", "professional outputs")
    
    with col3:
        st.metric("🎯 Accuracy Rate", "95%+", "consistent quality")


def render_system_overview_diagrams():
    """Render system overview with multiple diagrams"""
    
    diagram_tab, flow_tab = st.tabs(["🏗️ System Architecture", "👤 User Flow"])
    
    with diagram_tab:
        st.markdown("### 🏗️ **System Architecture Overview**")
        render_mermaid_with_fallback(
            create_system_architecture_diagram(),
            height=600,
            key="system_arch"
        )
    
    with flow_tab:
        st.markdown("### 👤 **User Experience Flow**")
        render_mermaid_with_fallback(
            create_user_flow_diagram(),
            height=400,
            key="user_flow"
        )