"""
Prompt Management Component
Backend prompt saving and template management
"""
import streamlit as st
from typing import Dict, List, Optional, Any
import json
import os
from datetime import datetime


def render_prompt_management_section():
    """Render prompt management interface"""
    
    st.markdown("### 🔧 **Agent Prompt Management**")
    st.markdown("*Customize AI agent prompts and save them to backend for consistent results*")
    
    # Create tabs for different agents
    conversa_tab, conny_tab, prody_tab, marketing_tab, templates_tab = st.tabs([
        "🎯 Conversa", "🏗️ Conny", "📋 ProDy", "🎨 Marketing", "📄 Templates"
    ])
    
    with conversa_tab:
        render_agent_prompt_editor("conversa", "Conversa - Transcript Analysis Agent")
    
    with conny_tab:
        render_agent_prompt_editor("conny", "Conny - Business Consulting Agent")
    
    with prody_tab:
        render_agent_prompt_editor("prody", "ProDy - Documentation Agent")
    
    with marketing_tab:
        render_agent_prompt_editor("marketing", "Marketing - Sales Deck Agent")
    
    with templates_tab:
        render_document_templates_section()


def render_agent_prompt_editor(agent_name: str, agent_title: str):
    """Render prompt editor for specific agent"""
    
    st.markdown(f"#### {agent_title}")
    
    # Load current prompt
    current_prompt = load_agent_prompt(agent_name)
    default_prompt = get_default_agent_prompt(agent_name)
    
    # Prompt editor
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # System prompt editor
        edited_prompt = st.text_area(
            f"System Prompt for {agent_name.title()}",
            value=current_prompt,
            height=300,
            help=f"Customize the system prompt that guides {agent_name.title()} agent behavior",
            key=f"{agent_name}_prompt_editor"
        )
        
        # Prompt variables section
        with st.expander("Available Template Variables", expanded=False):
            variables = get_prompt_variables(agent_name)
            for var, description in variables.items():
                st.markdown(f"- **{{{var}}}**: {description}")
    
    with col2:
        # Prompt actions
        st.markdown("**Actions:**")
        
        if st.button(f"💾 Save Prompt", key=f"save_{agent_name}"):
            save_agent_prompt(agent_name, edited_prompt)
            st.success(f"✅ {agent_name.title()} prompt saved!")
        
        if st.button(f"🔄 Reset to Default", key=f"reset_{agent_name}"):
            save_agent_prompt(agent_name, default_prompt)
            st.success(f"✅ {agent_name.title()} prompt reset to default!")
            st.rerun()
        
        if st.button(f"📋 Copy Prompt", key=f"copy_{agent_name}"):
            st.code(edited_prompt)
            st.info("📋 Prompt displayed above - copy manually")
        
        # Prompt statistics
        st.markdown("**Statistics:**")
        word_count = len(edited_prompt.split())
        char_count = len(edited_prompt)
        st.metric("Words", f"{word_count:,}")
        st.metric("Characters", f"{char_count:,}")
        
        # Validation
        if word_count > 1000:
            st.warning("⚠️ Long prompt - may impact performance")
        elif word_count < 50:
            st.warning("⚠️ Short prompt - may lack specificity")
        else:
            st.success("✅ Good prompt length")
    
    # Prompt testing section
    with st.expander(f"🧪 Test {agent_name.title()} Prompt", expanded=False):
        test_input = st.text_area(
            f"Test input for {agent_name.title()}",
            height=100,
            placeholder=f"Enter sample input to test {agent_name} prompt behavior...",
            key=f"{agent_name}_test_input"
        )
        
        if st.button(f"🔬 Test Prompt", key=f"test_{agent_name}"):
            if test_input:
                # TODO: Connect to actual agent for testing
                st.info(f"🔬 Prompt testing for {agent_name.title()} - Integration coming soon!")
                st.code(f"Input: {test_input}\nPrompt: {edited_prompt[:200]}...")
            else:
                st.warning("Please enter test input")


def render_document_templates_section():
    """Render document template management"""
    
    st.markdown("#### 📄 Document Templates")
    st.markdown("*Customize the templates used for generating output documents*")
    
    # Template selection
    template_types = [
        "Problem Overview",
        "Process Overview", 
        "Process Visualization",
        "Investment Proposal",
        "Next Steps",
        "Sales Presentation"
    ]
    
    selected_template = st.selectbox(
        "Select Template Type",
        template_types,
        key="template_selector"
    )
    
    # Template editor
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_template = load_document_template(selected_template)
        
        edited_template = st.text_area(
            f"{selected_template} Template",
            value=current_template,
            height=400,
            help=f"Markdown template for {selected_template} document generation",
            key="template_editor"
        )
        
        # Template variables
        with st.expander("Template Variables Reference", expanded=False):
            template_vars = get_template_variables(selected_template)
            st.markdown("**Available variables to use in your template:**")
            for var, desc in template_vars.items():
                st.markdown(f"- **{{{{{var}}}}}**: {desc}")
    
    with col2:
        # Template actions
        st.markdown("**Template Actions:**")
        
        if st.button("💾 Save Template", key="save_template"):
            save_document_template(selected_template, edited_template)
            st.success(f"✅ {selected_template} template saved!")
        
        if st.button("🔄 Reset Template", key="reset_template"):
            default_template = get_default_template(selected_template)
            save_document_template(selected_template, default_template)
            st.success(f"✅ {selected_template} template reset!")
            st.rerun()
        
        if st.button("👁️ Preview Template", key="preview_template"):
            render_template_preview(selected_template, edited_template)
        
        # Template stats
        st.markdown("**Template Stats:**")
        lines = len(edited_template.split('\n'))
        words = len(edited_template.split())
        st.metric("Lines", lines)
        st.metric("Words", words)
    
    # Template preview
    if st.session_state.get("show_template_preview"):
        render_template_preview(selected_template, edited_template)


def load_agent_prompt(agent_name: str) -> str:
    """Load agent prompt from backend storage"""
    
    # Try to load from file system first
    prompt_file = f"streamlit_app/data/prompts/{agent_name}_prompt.txt"
    
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r') as f:
            return f.read()
    
    # Otherwise return default
    return get_default_agent_prompt(agent_name)


def save_agent_prompt(agent_name: str, prompt: str) -> bool:
    """Save agent prompt to backend storage"""
    
    try:
        # Ensure directory exists
        os.makedirs("streamlit_app/data/prompts", exist_ok=True)
        
        # Save to file
        prompt_file = f"streamlit_app/data/prompts/{agent_name}_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        # Also save to session state
        if "agent_prompts" not in st.session_state:
            st.session_state.agent_prompts = {}
        st.session_state.agent_prompts[agent_name] = prompt
        
        # Log the save
        log_prompt_save(agent_name, prompt)
        
        return True
    
    except Exception as e:
        st.error(f"Failed to save prompt: {str(e)}")
        return False


def get_default_agent_prompt(agent_name: str) -> str:
    """Get default system prompt for agent"""
    
    default_prompts = {
        "conversa": """You are Conversa, an expert transcript analysis specialist for presales teams.

Your role is to analyze customer conversation transcripts and extract structured business intelligence that enables accurate proposal generation.

## Core Responsibilities:
1. **Stakeholder Analysis**: Identify key decision makers, their roles, concerns, and influence levels
2. **Requirement Extraction**: Parse functional and non-functional requirements from conversations
3. **Pain Point Identification**: Uncover current challenges, costs, and business impacts  
4. **Context Understanding**: Grasp business domain, industry specifics, and competitive landscape
5. **Success Criteria Definition**: Clarify what winning looks like for the customer

## Analysis Framework:
- **WHO**: Stakeholders, decision makers, technical contacts
- **WHAT**: Current state, desired future state, specific requirements
- **WHY**: Business drivers, pain points, costs of inaction
- **WHEN**: Timeline constraints, seasonal factors, urgency drivers
- **WHERE**: Geographic, system, or process boundaries
- **HOW**: Success metrics, acceptance criteria, evaluation process

## Output Format:
Structure your analysis using clear sections with bullet points. Focus on actionable insights that enable accurate proposal creation. Highlight critical business impacts and quantify problems where possible.

Remember: Your analysis directly impacts proposal quality and win rates. Be thorough, accurate, and business-focused.""",

        "conny": """You are Conny, a senior business consultant and solution architect specializing in presales engagements.

Your expertise lies in translating customer requirements into compelling business solutions and project approaches that maximize value and minimize risk.

## Core Responsibilities:
1. **Solution Architecture**: Design optimal approaches based on customer requirements
2. **Business Case Development**: Articulate clear value propositions and ROI scenarios
3. **Risk Assessment**: Identify implementation challenges and mitigation strategies
4. **Competitive Positioning**: Differentiate against alternatives and status quo
5. **Implementation Planning**: Define realistic project phases and success paths

## Knowledge Areas:
- Industry best practices and proven methodologies  
- Technology integration patterns and architecture principles
- Change management and stakeholder alignment strategies
- ROI modeling and business case development
- Risk assessment and mitigation planning

## Approach:
- **Business-First**: Always prioritize business outcomes over technical features
- **Evidence-Based**: Reference similar successful projects and proven approaches
- **Risk-Aware**: Identify potential challenges and plan mitigation strategies
- **Value-Focused**: Quantify benefits and build compelling business cases
- **Practical**: Recommend realistic, achievable implementation approaches

## Output Style:
Create comprehensive, business-ready documentation that executives and technical teams can both understand. Use clear structure, quantified benefits, and actionable recommendations.

Your solutions should instill confidence and demonstrate deep understanding of the customer's business context.""",

        "prody": """You are ProDy, an expert product manager and technical documentation specialist focused on creating comprehensive, professional project deliverables.

Your role is to transform business requirements and solution approaches into polished, actionable documentation that guides successful project execution.

## Core Responsibilities:
1. **Document Architecture**: Create comprehensive document suites covering all project aspects
2. **Process Design**: Define clear workflows, methodologies, and implementation approaches  
3. **Visual Communication**: Generate process diagrams, architectures, and visual aids
4. **Investment Planning**: Develop realistic budgets, timelines, and resource requirements
5. **Success Framework**: Define measurable outcomes and project success criteria

## Document Types You Create:
- **Problem Overview**: Executive-level business context and challenge analysis
- **Process Overview**: Detailed implementation methodology and approach
- **Process Visualization**: Mermaid diagrams showing current vs future state
- **Investment Proposal**: Budget, timeline, resource requirements, and ROI analysis
- **Next Steps**: Actionable roadmap with milestones and decision points

## Quality Standards:
- **Professional**: Board-room ready formatting and language
- **Comprehensive**: Complete coverage of all project aspects
- **Actionable**: Specific next steps and clear responsibilities  
- **Measurable**: Quantified success metrics and KPIs
- **Visual**: Diagrams and charts to illustrate complex concepts

## Writing Style:
- Executive summary approach with supporting detail
- Clear headings and structured information hierarchy
- Bullet points for easy scanning and comprehension
- Quantified benefits and realistic timelines
- Professional but accessible language

Your documentation should enable stakeholders to make confident decisions and guide successful project execution from approval through completion.""",

        "marketing": """You are the Marketing Agent, a specialist in creating compelling, customer-facing sales presentations that win business.

Your expertise is translating technical project details into persuasive value propositions that resonate with executive decision makers and drive purchase decisions.

## Core Responsibilities:
1. **Value Proposition Development**: Craft compelling business benefits and competitive advantages
2. **Executive Communication**: Create C-level appropriate presentations and messaging
3. **ROI Storytelling**: Transform numbers into compelling business narratives
4. **Competitive Differentiation**: Position solution advantages clearly against alternatives
5. **Call-to-Action Design**: Drive specific next steps and decision momentum

## Presentation Framework:
1. **Hook**: Attention-grabbing problem statement or opportunity
2. **Context**: Business challenge and current state pain points
3. **Solution**: Clear, benefit-focused solution overview
4. **Value**: Quantified business benefits and ROI projections  
5. **Proof**: Evidence, case studies, and credibility indicators
6. **Action**: Clear next steps and decision framework

## Communication Principles:
- **Customer-Centric**: Focus on their benefits, not our features
- **Executive-Level**: Board-room appropriate language and concepts
- **Results-Focused**: Emphasize business outcomes and measurable value
- **Credible**: Include proof points, testimonials, and risk mitigation
- **Actionable**: Clear next steps and decision criteria

## Content Style:
- Headlines that capture attention and communicate value
- Bullet points that are benefits-focused, not feature-focused
- Quantified claims with specific numbers and timeframes
- Visual elements that support key messages
- Compelling calls-to-action that drive decisions

Your sales presentations should make it easy for customers to say "yes" by clearly demonstrating value, addressing concerns, and providing a clear path forward."""
    }
    
    return default_prompts.get(agent_name, f"You are {agent_name.title()}, an AI agent specialized in presales support.")


def get_prompt_variables(agent_name: str) -> Dict[str, str]:
    """Get available template variables for agent prompts"""
    
    common_vars = {
        "customer_name": "Name of the customer/company",
        "transcript_content": "Full customer transcript content",
        "requirements": "Extracted customer requirements",
        "timeline": "Project timeline and deadlines",
        "budget": "Budget constraints and investment parameters"
    }
    
    agent_specific_vars = {
        "conversa": {
            "call_participants": "List of call participants and roles",
            "call_duration": "Length of customer conversation",
            "pain_points": "Identified customer pain points"
        },
        "conny": {
            "industry": "Customer industry and business context",
            "company_size": "Company size and scale information",
            "current_solutions": "Existing tools and systems in use"
        },
        "prody": {
            "solution_approach": "Recommended solution methodology",
            "deliverables": "Expected project deliverables",
            "success_metrics": "Defined success criteria"
        },
        "marketing": {
            "value_proposition": "Core value proposition messaging",
            "competitive_advantages": "Key differentiators",
            "roi_projections": "Return on investment calculations"
        }
    }
    
    return {**common_vars, **agent_specific_vars.get(agent_name, {})}


def load_document_template(template_type: str) -> str:
    """Load document template from storage"""
    
    template_file = f"streamlit_app/data/templates/{template_type.lower().replace(' ', '_')}_template.md"
    
    if os.path.exists(template_file):
        with open(template_file, 'r') as f:
            return f.read()
    
    return get_default_template(template_type)


def save_document_template(template_type: str, template_content: str) -> bool:
    """Save document template to storage"""
    
    try:
        os.makedirs("streamlit_app/data/templates", exist_ok=True)
        
        template_file = f"streamlit_app/data/templates/{template_type.lower().replace(' ', '_')}_template.md"
        with open(template_file, 'w') as f:
            f.write(template_content)
        
        return True
    
    except Exception as e:
        st.error(f"Failed to save template: {str(e)}")
        return False


def get_default_template(template_type: str) -> str:
    """Get default template content"""
    
    templates = {
        "Problem Overview": """# Problem Overview: {{customer_name}}

## Executive Summary
{{executive_summary}}

## Current State Analysis
{{current_state_analysis}}

## Key Pain Points
{{pain_points}}

## Business Impact
- **Financial Impact**: {{financial_impact}}
- **Operational Impact**: {{operational_impact}}
- **Strategic Impact**: {{strategic_impact}}

## Stakeholder Impact
{{stakeholder_impact}}

## Cost of Inaction
{{cost_of_inaction}}

## Success Criteria
{{success_criteria}}""",

        "Process Overview": """# Process Overview: {{customer_name}} Implementation

## Solution Approach
{{solution_approach}}

## Implementation Methodology
{{implementation_methodology}}

## Key Phases
{{implementation_phases}}

## Technology Stack
{{technology_stack}}

## Integration Points
{{integration_points}}

## Risk Mitigation
{{risk_mitigation}}

## Success Metrics
{{success_metrics}}""",

        "Process Visualization": """# Process Visualization: {{customer_name}}

## Current State Process Flow
```mermaid
{{current_state_diagram}}
```

## Proposed Future State
```mermaid
{{future_state_diagram}}
```

## Process Improvement Analysis
{{process_improvements}}

## Efficiency Gains
{{efficiency_gains}}""",

        "Investment Proposal": """# Investment Proposal: {{customer_name}}

## Executive Summary
{{investment_executive_summary}}

## Investment Breakdown
{{investment_breakdown}}

## Timeline and Milestones
{{timeline_and_milestones}}

## Resource Requirements
{{resource_requirements}}

## ROI Analysis
{{roi_analysis}}

## Risk Assessment
{{risk_assessment}}

## Next Steps
{{next_steps}}""",

        "Next Steps": """# Next Steps: {{customer_name}}

## Immediate Actions
{{immediate_actions}}

## Decision Points
{{decision_points}}

## Stakeholder Involvement
{{stakeholder_involvement}}

## Timeline
{{timeline}}

## Success Criteria
{{success_criteria}}""",

        "Sales Presentation": """# {{customer_name}} - Digital Transformation Proposal

## The Challenge
{{challenge_summary}}

## Our Solution
{{solution_summary}}

## Value Proposition
{{value_proposition}}

## ROI Projection
{{roi_projection}}

## Implementation Plan
{{implementation_plan}}

## Why Choose Us
{{competitive_advantages}}

## Next Steps
{{next_steps}}"""
    }
    
    return templates.get(template_type, f"# {template_type} Template\n\nContent for {{customer_name}}")


def get_template_variables(template_type: str) -> Dict[str, str]:
    """Get available variables for document templates"""
    
    return {
        "customer_name": "Customer company name",
        "executive_summary": "High-level summary of the situation",
        "current_state_analysis": "Analysis of current business state",
        "pain_points": "Key customer pain points and challenges", 
        "financial_impact": "Financial implications and costs",
        "operational_impact": "Operational efficiency impacts",
        "strategic_impact": "Strategic business implications",
        "stakeholder_impact": "Impact on key stakeholders",
        "cost_of_inaction": "Cost of not addressing the problem",
        "success_criteria": "Definition of project success",
        "solution_approach": "Proposed solution methodology",
        "implementation_methodology": "How the solution will be implemented",
        "roi_analysis": "Return on investment calculations",
        "timeline": "Project timeline and milestones"
    }


def render_template_preview(template_type: str, template_content: str):
    """Render template preview with sample data"""
    
    st.markdown("### 👁️ Template Preview")
    
    # Sample data for preview
    sample_data = {
        "customer_name": "Acme Corp",
        "executive_summary": "Acme Corp requires digital transformation of their inventory management system to reduce operational costs and improve customer satisfaction.",
        "current_state_analysis": "Manual processes causing 15% inventory discrepancies and $50K monthly revenue loss",
        "pain_points": "• 3-4 hours daily manual updates\n• 15% inventory discrepancies\n• Customer satisfaction issues",
        "financial_impact": "$600K annual revenue loss potential",
        "roi_analysis": "Break-even within 12 months, $1.2M annual savings thereafter"
    }
    
    # Replace template variables with sample data
    preview_content = template_content
    for var, value in sample_data.items():
        preview_content = preview_content.replace(f"{{{{{var}}}}}", value)
    
    st.markdown(preview_content)
    st.session_state["show_template_preview"] = True


def log_prompt_save(agent_name: str, prompt: str):
    """Log prompt save for audit trail"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "action": "prompt_save",
        "prompt_length": len(prompt),
        "word_count": len(prompt.split())
    }
    
    # Save to session state for now (could extend to proper logging)
    if "prompt_audit_log" not in st.session_state:
        st.session_state.prompt_audit_log = []
    
    st.session_state.prompt_audit_log.append(log_entry)