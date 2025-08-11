"""
Smart Business Input Component
Handles any business input (transcripts, thoughts, ideas) with markdown support
"""
import streamlit as st
import re
from typing import Dict, Any, Optional
from datetime import datetime


def render_smart_input_section():
    """Render the smart business input interface"""
    
    st.subheader("💭 Smart Business Input")
    st.markdown("**Enter any business content**: transcripts, ideas, customer feedback, or strategic thoughts")
    
    # Input tabs for different input methods
    text_tab, file_tab, template_tab = st.tabs(["✍️ Text Input", "📁 File Upload", "📋 Templates"])
    
    with text_tab:
        render_text_input_interface()
    
    with file_tab:
        render_file_input_interface()
    
    with template_tab:
        render_template_interface()


def render_text_input_interface():
    """Render smart text input with markdown support"""
    
    st.markdown("### ✍️ Direct Text Input")
    st.markdown("*Supports markdown formatting*")
    
    # Input format selection
    input_format = st.selectbox(
        "Input Format",
        ["Plain Text", "Markdown", "Customer Transcript", "Strategic Notes"],
        help="Select the type of content you're entering"
    )
    
    # Large text area for input
    user_input = st.text_area(
        "Business Content",
        height=300,
        placeholder=get_input_placeholder(input_format),
        help="Paste any business content here. The system will intelligently analyze and route it."
    )
    
    # Markdown preview if markdown selected
    if input_format == "Markdown" and user_input:
        with st.expander("🔍 Markdown Preview", expanded=False):
            st.markdown(user_input)
    
    # Metadata hints
    col1, col2 = st.columns(2)
    
    with col1:
        customer_name = st.text_input(
            "Customer/Project Name (Optional)",
            placeholder="Acme Corp, Internal Strategy, etc."
        )
        
    with col2:
        content_type_hint = st.selectbox(
            "Content Type Hint (Optional)",
            ["Auto-detect", "Customer Transcript", "Strategic Planning", 
             "Competitive Analysis", "Solution Requirements", "Feedback/Ideas"],
            help="Help the router understand your content"
        )
    
    # Save to session state
    if user_input:
        st.session_state["smart_input"] = {
            "content": user_input,
            "format": input_format,
            "customer_name": customer_name or "Business Input",
            "content_type_hint": content_type_hint,
            "input_method": "text",
            "timestamp": datetime.now().isoformat()
        }
        
        # Show input analysis preview
        render_input_analysis_preview(user_input)


def render_file_input_interface():
    """Render enhanced file upload interface"""
    
    st.markdown("### 📁 File Upload")
    
    uploaded_file = st.file_uploader(
        "Upload Business Document",
        type=["txt", "md", "docx", "pdf"],
        help="Upload transcripts, documents, or notes in various formats"
    )
    
    if uploaded_file:
        # Process uploaded file
        try:
            if uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                content = uploaded_file.read().decode('utf-8')
            elif uploaded_file.name.endswith('.md'):
                content = uploaded_file.read().decode('utf-8')
                st.markdown("**Markdown Preview:**")
                with st.expander("🔍 Preview", expanded=True):
                    st.markdown(content)
            else:
                st.warning("Advanced file processing (DOCX, PDF) coming soon!")
                return
                
            # Save to session state
            st.session_state["smart_input"] = {
                "content": content,
                "format": "file_upload",
                "customer_name": uploaded_file.name.split('.')[0],
                "content_type_hint": "Auto-detect",
                "input_method": "file",
                "filename": uploaded_file.name,
                "timestamp": datetime.now().isoformat()
            }
            
            st.success(f"✅ Loaded {len(content):,} characters from {uploaded_file.name}")
            render_input_analysis_preview(content)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")


def render_template_interface():
    """Render business input templates for common scenarios"""
    
    st.markdown("### 📋 Business Input Templates")
    st.markdown("*Quick-start templates for common business scenarios*")
    
    templates = {
        "Customer Discovery Call": {
            "content": """# Customer Discovery Call - [Customer Name]
**Date**: {date}
**Participants**: [Names and roles]

## Current Challenges
- [Key pain point 1]
- [Key pain point 2]
- [Key pain point 3]

## Current Process/System
[Describe current state]

## Desired Outcomes
- [Goal 1]
- [Goal 2]
- [Goal 3]

## Budget & Timeline
- **Budget Range**: [Amount or constraints]
- **Timeline**: [When they need solution]
- **Decision Process**: [Who decides, approval process]

## Technical Requirements
- [Requirement 1]
- [Requirement 2]

## Competitive Landscape
[Alternatives they're considering]

## Next Steps
[Agreed follow-up actions]
""",
            "icon": "🎧"
        },
        
        "Strategic Initiative": {
            "content": """# Strategic Initiative - [Initiative Name]
**Date**: {date}
**Stakeholders**: [Key people involved]

## Business Context
[Why this initiative matters now]

## Problem Statement
[Clear definition of what we're solving]

## Proposed Solution Approach
[High-level solution concept]

## Success Metrics
- [Metric 1]
- [Metric 2]
- [Metric 3]

## Resource Requirements
- **Team Size**: [Number of people]
- **Timeline**: [Duration]
- **Budget**: [Investment required]

## Risks & Mitigation
- **Risk 1**: [Description] → [Mitigation]
- **Risk 2**: [Description] → [Mitigation]

## Implementation Phases
1. **Phase 1**: [Description]
2. **Phase 2**: [Description]
3. **Phase 3**: [Description]
""",
            "icon": "📈"
        },
        
        "Competitive Analysis": {
            "content": """# Competitive Analysis - [Opportunity Name]
**Date**: {date}
**Analyst**: [Your name]

## Opportunity Overview
[Brief description of the deal/opportunity]

## Competitors Identified
### [Competitor 1 Name]
- **Strengths**: [What they do well]
- **Weaknesses**: [Where they fall short]
- **Pricing**: [Their pricing model]

### [Competitor 2 Name]
- **Strengths**: [What they do well]
- **Weaknesses**: [Where they fall short]
- **Pricing**: [Their pricing model]

## Our Differentiation
- [Key differentiator 1]
- [Key differentiator 2]
- [Key differentiator 3]

## Recommended Positioning
[How we should position against competition]

## Win Strategy
[Specific tactics to win this deal]
""",
            "icon": "⚔️"
        }
    }
    
    selected_template = st.selectbox(
        "Choose Template",
        list(templates.keys()),
        format_func=lambda x: f"{templates[x]['icon']} {x}"
    )
    
    if st.button("🚀 Load Template", use_container_width=True):
        template_content = templates[selected_template]["content"].format(
            date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Use a unique key to force re-render
        st.session_state["template_content"] = template_content
        st.rerun()
    
    # Show loaded template content
    if "template_content" in st.session_state:
        st.markdown("**Template Loaded - Edit as needed:**")
        edited_content = st.text_area(
            "Edit Template",
            value=st.session_state["template_content"],
            height=300,
            key="template_editor"
        )
        
        if edited_content != st.session_state.get("template_content", ""):
            st.session_state["smart_input"] = {
                "content": edited_content,
                "format": "Template",
                "customer_name": f"Template: {selected_template}",
                "content_type_hint": selected_template,
                "input_method": "template",
                "timestamp": datetime.now().isoformat()
            }


def render_input_analysis_preview(content: str):
    """Show preview of how the input will be analyzed"""
    
    if not content or len(content.strip()) < 10:
        return
    
    st.markdown("---")
    st.markdown("### 🤖 Input Analysis Preview")
    
    # Basic content analysis
    word_count = len(content.split())
    char_count = len(content)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Word Count", f"{word_count:,}")
    with col2:
        st.metric("Characters", f"{char_count:,}")
    with col3:
        is_transcript = detect_transcript_patterns(content)
        st.metric("Transcript Detected", "Yes" if is_transcript else "No")
    
    # Show what the router will analyze
    with st.expander("🔍 Router Analysis Preview", expanded=False):
        analysis = generate_preview_analysis(content)
        st.json(analysis)
        
    # Show potential past proposal matches
    with st.expander("📚 Similar Past Proposals (Mock)", expanded=False):
        st.markdown("*RAG system will find similar past work:*")
        mock_matches = [
            "📄 Acme Corp Digital Transformation (85% match)",
            "📄 TechStart AI Implementation (72% match)", 
            "📄 Manufacturing Process Optimization (68% match)"
        ]
        for match in mock_matches:
            st.markdown(f"- {match}")


def get_input_placeholder(input_format: str) -> str:
    """Get appropriate placeholder text for different input formats"""
    
    placeholders = {
        "Plain Text": """Paste any business content here...

Examples:
- Customer discovery call notes
- Strategic thoughts and ideas
- Competitive intelligence
- Solution requirements
- Meeting notes""",
        
        "Markdown": """# Your Business Content

Enter markdown-formatted content here...

## Example sections:
- **Customer**: Name and context
- **Challenge**: What they need to solve
- **Solution**: Your proposed approach""",
        
        "Customer Transcript": """Customer: We're struggling with our current system...
Sales Rep: Tell me more about the challenges you're facing.
Customer: Our biggest issue is...""",
        
        "Strategic Notes": """Strategic thoughts and planning notes...

Key considerations:
- Market opportunity
- Resource requirements
- Timeline constraints
- Success metrics"""
    }
    
    return placeholders.get(input_format, placeholders["Plain Text"])


def detect_transcript_patterns(content: str) -> bool:
    """Detect if content looks like a transcript"""
    
    transcript_patterns = [
        r'\b(Customer|Client|Prospect):\s',
        r'\b(Sales|Rep|Account Manager):\s',
        r'\b(Interviewer|Moderator):\s',
        r'\b\w+:\s[A-Z]',  # "Name: Sentence" pattern
        r'\[.*\]',  # Timestamps or annotations
        r'Q\d+:|Question \d+:',  # Question numbering
        r'\b(minute|minutes|timestamp|recorded)\b'
    ]
    
    pattern_matches = sum(1 for pattern in transcript_patterns 
                         if re.search(pattern, content, re.IGNORECASE))
    
    return pattern_matches >= 2


def generate_preview_analysis(content: str) -> Dict[str, Any]:
    """Generate preview of how the router will analyze the content"""
    
    # This is a simplified preview - the actual router agent will be more sophisticated
    analysis = {
        "is_transcript": detect_transcript_patterns(content),
        "content_type": detect_content_type(content),
        "industry_hints": extract_industry_hints(content),
        "stakeholder_mentions": extract_stakeholder_mentions(content),
        "solution_indicators": extract_solution_indicators(content),
        "urgency_level": detect_urgency_level(content),
        "budget_indicators": extract_budget_indicators(content),
        "timeline_mentions": extract_timeline_mentions(content),
        "rag_search_terms": generate_rag_search_terms(content)
    }
    
    return analysis


def detect_content_type(content: str) -> str:
    """Detect the type of business content"""
    
    content_lower = content.lower()
    
    if any(term in content_lower for term in ['transcript', 'customer:', 'client:', 'call recording']):
        return "customer_transcript"
    elif any(term in content_lower for term in ['strategy', 'initiative', 'roadmap', 'vision']):
        return "strategic_planning"
    elif any(term in content_lower for term in ['competitor', 'competitive', 'vs.', 'comparison']):
        return "competitive_analysis"
    elif any(term in content_lower for term in ['requirements', 'specs', 'specification', 'features']):
        return "solution_requirements"
    elif any(term in content_lower for term in ['feedback', 'thoughts', 'ideas', 'brainstorm']):
        return "feedback_ideas"
    else:
        return "general_business"


def extract_industry_hints(content: str) -> list:
    """Extract industry indicators from content"""
    
    industries = {
        "technology": ["software", "saas", "platform", "api", "cloud", "digital", "tech"],
        "manufacturing": ["production", "factory", "manufacturing", "supply chain", "inventory"],
        "healthcare": ["patient", "medical", "healthcare", "clinical", "hospital", "doctor"],
        "finance": ["banking", "financial", "investment", "trading", "fintech", "payments"],
        "retail": ["e-commerce", "shopping", "customer experience", "retail", "store"],
        "education": ["school", "university", "learning", "students", "education", "training"],
        "real_estate": ["property", "real estate", "construction", "building", "facility"]
    }
    
    content_lower = content.lower()
    detected_industries = []
    
    for industry, keywords in industries.items():
        if any(keyword in content_lower for keyword in keywords):
            detected_industries.append(industry)
    
    return detected_industries[:3]  # Top 3 matches


def extract_stakeholder_mentions(content: str) -> list:
    """Extract stakeholder roles mentioned in content"""
    
    stakeholder_patterns = [
        r'\b(CEO|CTO|CFO|COO|VP|Director|Manager)\b',
        r'\b(Decision maker|Stakeholder|Owner|Lead)\b',
        r'\b(Team|Department|Division)\s+\w+',
        r'\b(IT|Engineering|Sales|Marketing|Operations|Finance)\s+(team|department|manager)\b'
    ]
    
    stakeholders = []
    for pattern in stakeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        stakeholders.extend(matches)
    
    return list(set(stakeholders))[:5]  # Unique stakeholders, max 5


def extract_solution_indicators(content: str) -> list:
    """Extract solution types mentioned in content"""
    
    solutions = {
        "automation": ["automate", "automation", "workflow", "process improvement"],
        "analytics": ["analytics", "reporting", "dashboard", "insights", "data"],
        "integration": ["integrate", "api", "connection", "sync", "consolidate"],
        "transformation": ["digital transformation", "modernize", "upgrade", "replace"],
        "optimization": ["optimize", "efficiency", "performance", "streamline"],
        "security": ["security", "compliance", "audit", "governance", "risk"]
    }
    
    content_lower = content.lower()
    detected_solutions = []
    
    for solution, keywords in solutions.items():
        if any(keyword in content_lower for keyword in keywords):
            detected_solutions.append(solution)
    
    return detected_solutions


def detect_urgency_level(content: str) -> str:
    """Detect urgency level from content"""
    
    high_urgency = ["urgent", "asap", "immediately", "critical", "emergency", "deadline"]
    medium_urgency = ["soon", "quickly", "priority", "important", "needed by"]
    
    content_lower = content.lower()
    
    if any(term in content_lower for term in high_urgency):
        return "high"
    elif any(term in content_lower for term in medium_urgency):
        return "medium"
    else:
        return "low"


def extract_budget_indicators(content: str) -> list:
    """Extract budget-related information"""
    
    budget_patterns = [
        r'\$[\d,]+[km]?',  # $100k, $1.5m
        r'budget\s+of\s+[\$\d,]+',
        r'[\d,]+\s+dollar',
        r'cost\s+[\$\d,]+',
        r'investment\s+[\$\d,]+'
    ]
    
    budget_mentions = []
    for pattern in budget_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        budget_mentions.extend(matches)
    
    return budget_mentions[:3]


def extract_timeline_mentions(content: str) -> list:
    """Extract timeline-related information"""
    
    timeline_patterns = [
        r'\d+\s+(week|month|year|day)s?',
        r'by\s+(january|february|march|april|may|june|july|august|september|october|november|december)',
        r'Q[1-4]\s+\d{4}',
        r'end\s+of\s+\w+',
        r'next\s+(week|month|quarter|year)'
    ]
    
    timeline_mentions = []
    for pattern in timeline_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        timeline_mentions.extend(matches)
    
    return timeline_mentions[:3]


def generate_rag_search_terms(content: str) -> list:
    """Generate search terms for RAG system to find similar past proposals"""
    
    # Extract key business terms for RAG search
    business_terms = []
    
    # Industry terms
    business_terms.extend(extract_industry_hints(content))
    
    # Solution types
    business_terms.extend(extract_solution_indicators(content))
    
    # Extract important nouns and phrases
    important_patterns = [
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # Proper nouns
        r'\b\w+\s+(platform|system|solution|service|tool)\b',
        r'\b(implement|deploy|integrate|optimize|automate)\s+\w+\b'
    ]
    
    for pattern in important_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        business_terms.extend([match.lower() for match in matches])
    
    # Return unique terms, prioritized
    return list(dict.fromkeys(business_terms))[:10]