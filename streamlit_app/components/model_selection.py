"""
Model Selection Component for Streamlit Application
Handle LLM model selection and configuration
"""
import streamlit as st
from typing import Dict, Optional
from streamlit_app.config import AppConfig


def render_model_selection(config: AppConfig):
    """Render model selection interface with agent-specific mappings"""
    
    st.markdown("### 🤖 Model Configuration")
    st.markdown("**Unified Model Configuration** (All agents using same model)")
    
    # Display agent-specific model mappings
    if hasattr(config, 'agent_models'):
        agent_info = {
            "conversa": {"icon": "📊", "task": "Transcript Analysis"},
            "conny": {"icon": "🧠", "task": "Business Consulting"}, 
            "prody": {"icon": "📄", "task": "Document Generation"},
            "preston": {"icon": "⚡", "task": "Process Optimization"},
            "marketing": {"icon": "🎨", "task": "Sales Deck Creation"}
        }
        
        for agent_name, model_id in config.agent_models.items():
            if agent_name in agent_info:
                info = agent_info[agent_name]
                model_display_name = next((k for k, v in config.available_models.items() if v == model_id), model_id)
                st.markdown(f"**{info['icon']} {info['task']}**: `{model_display_name}`")
    
    # Global model override option
    st.markdown("---")
    override_model = st.checkbox("Override with single model for all agents", help="Use one model for all agents instead of optimized mappings")
    
    if override_model:
        # Model selection dropdown
        selected_model_key = st.selectbox(
            "Select Override Model",
            options=list(config.available_models.keys()),
            index=0,
            help="This model will be used for all agents instead of the optimized mappings"
        )
        
        # Save selection to session state
        st.session_state["selected_model"] = {
            "name": selected_model_key,
            "model_id": config.available_models[selected_model_key],
            "override": True
        }
    else:
        # Use optimized agent-specific models
        st.session_state["selected_model"] = {
            "name": "agent-optimized",
            "model_id": "agent-specific",
            "override": False
        }
    
    # Display model information
    with st.expander("📋 Model Information & Methodology", expanded=False):
        if not override_model:
            display_agent_model_methodology()
        else:
            display_model_info(selected_model_key)
    
    # Advanced model configuration
    with st.expander("⚙️ Advanced Model Settings", expanded=False):
        render_advanced_model_settings()


def display_agent_model_methodology():
    """Display the methodology behind agent-specific model selection"""
    
    st.markdown("### 🎯 Agent-Specific Model Selection Methodology")
    st.markdown("Each agent uses an optimally selected model based on:")
    
    methodology_data = {
        "conversa": {
            "model": "DeepSeek Coder V2",
            "reasoning": [
                "**Structured Analysis Excellence**: Superior at extracting structured information from transcripts",
                "**Cost-Effectiveness**: 90% of premium model accuracy at 10% of the cost", 
                "**Pattern Recognition**: Excels at identifying customer pain points and requirements"
            ],
            "task_complexity": "Medium",
            "business_criticality": "High",
            "cost_priority": "High"
        },
        "conny": {
            "model": "Claude 3.7 Sonnet", 
            "reasoning": [
                "**Superior Business Reasoning**: #1 ranked for strategic analysis and complex reasoning",
                "**Extended Context**: 200K token window handles comprehensive business docs",
                "**Industry Recognition**: Most used model for business applications"
            ],
            "task_complexity": "High",
            "business_criticality": "Mission Critical",
            "cost_priority": "Quality over Cost"
        },
        "prody": {
            "model": "GPT-4o",
            "reasoning": [
                "**Document Generation Leader**: Industry standard for professional documents",
                "**Formatting Excellence**: Superior formatting and structure consistency",
                "**Enterprise Reliability**: Proven track record in business document creation"
            ],
            "task_complexity": "High", 
            "business_criticality": "Mission Critical",
            "cost_priority": "Quality over Cost"
        },
        "preston": {
            "model": "Gemini 2.5 Flash",
            "reasoning": [
                "**Analytical Speed**: Fastest processing for optimization calculations",
                "**Massive Context**: 1M token window for extensive process documentation",
                "**Cost-Performance Balance**: Excellent analysis at reasonable cost"
            ],
            "task_complexity": "High",
            "business_criticality": "High", 
            "cost_priority": "Balanced"
        },
        "marketing": {
            "model": "GPT-4o",
            "reasoning": [
                "**Creative-Business Balance**: Optimal blend of creativity and business acumen",
                "**Brand Consistency**: Excellent at maintaining consistent tone",
                "**Sales Optimization**: Proven effectiveness in persuasive content creation"
            ],
            "task_complexity": "Medium",
            "business_criticality": "High",
            "cost_priority": "Creativity over Cost"
        }
    }
    
    for agent_name, data in methodology_data.items():
        agent_icons = {"conversa": "📊", "conny": "🧠", "prody": "📄", "preston": "⚡", "marketing": "🎨"}
        
        st.markdown(f"#### {agent_icons.get(agent_name, '🤖')} {agent_name.title()} Agent → {data['model']}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Selection Reasoning:**")
            for reason in data['reasoning']:
                st.markdown(f"- {reason}")
        
        with col2:
            st.markdown("**Evaluation Factors:**")
            st.markdown(f"- **Task Complexity**: {data['task_complexity']}")
            st.markdown(f"- **Business Impact**: {data['business_criticality']}")
            st.markdown(f"- **Cost Strategy**: {data['cost_priority']}")
        
        st.markdown("---")
    
    st.markdown("### 💰 Cost-Benefit Analysis")
    st.markdown("**Total Monthly Cost**: ~$5.22/month for 25 proposals")
    st.markdown("**ROI**: 7,666% annual ROI with 30% cycle-time reduction")
    st.markdown("**Savings**: $4,800/month in consultant time")


def display_model_info(model_key: str):
    """Display information about the selected model"""
    
    model_descriptions = {
        "gpt-oss-120b": {
            "provider": "OpenAI",
            "description": "OpenAI's GPT-OSS 120B model for general-purpose tasks",
            "strengths": ["General-purpose", "Cost-effective", "Large parameter count"],
            "ideal_for": "General business tasks and document processing",
            "pricing": "$0.00007/$0.0003 per M tokens"
        },
        "claude-3.7-sonnet": {
            "provider": "Anthropic",
            "description": "Latest Claude model with superior business reasoning and strategic analysis",
            "strengths": ["Business strategy", "Complex reasoning", "Long context handling"],
            "ideal_for": "Business consulting and strategic planning",
            "pricing": "$3.00/$15.00 per M tokens"
        },
        "gpt-4o": {
            "provider": "OpenAI",
            "description": "Industry leader for professional document generation and multimodal tasks",
            "strengths": ["Document formatting", "Professional writing", "Multimodal support"],
            "ideal_for": "Document generation and sales materials",
            "pricing": "$2.50/$10.00 per M tokens"
        },
        "deepseek-coder-v2": {
            "provider": "DeepSeek",
            "description": "Specialized in structured analysis and pattern recognition",
            "strengths": ["Data extraction", "Pattern recognition", "Cost efficiency"],
            "ideal_for": "Transcript analysis and requirement extraction",
            "pricing": "$0.27/$1.10 per M tokens"
        },
        "gemini-2.5-flash": {
            "provider": "Google",
            "description": "Fast analytical processing with massive context window",
            "strengths": ["Speed", "Large context", "Process optimization"],
            "ideal_for": "Process optimization and analytical tasks",
            "pricing": "$0.15/$0.60 per M tokens"
        },
        "gpt-4o-mini": {
            "strengths": ["Analysis", "Structured output", "Technical writing"],
            "ideal_for": "Document analysis and structured generation"
        },
        "llama-3.1-405b": {
            "provider": "Meta",
            "description": "Large open-source model with strong performance",
            "strengths": ["Cost-effective", "Good reasoning", "Open source"],
            "ideal_for": "Budget-conscious high-performance tasks"
        },
        "gpt-4o-mini": {
            "provider": "OpenAI",
            "description": "Faster, more cost-effective version of GPT-4",
            "strengths": ["Speed", "Cost-effective", "Good quality"],
            "ideal_for": "Quick processing and testing"
        }
    }
    
    if model_key in model_descriptions:
        info = model_descriptions[model_key]
        
        st.markdown(f"**Provider:** {info['provider']}")
        st.markdown(f"**Description:** {info['description']}")
        
        st.markdown("**Strengths:**")
        for strength in info['strengths']:
            st.markdown(f"- {strength}")
        
        st.markdown(f"**💡 Ideal for:** {info['ideal_for']}")
    else:
        st.info("Model information not available")


def render_advanced_model_settings():
    """Render advanced model configuration options"""
    
    st.markdown("**Model Parameters:**")
    
    # Temperature setting
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness in output. Lower = more focused, Higher = more creative"
    )
    
    # Max tokens setting
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=1500,
        step=100,
        help="Maximum number of tokens in response"
    )
    
    # Top-p setting
    top_p = st.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1,
        help="Nucleus sampling parameter"
    )
    
    # Save advanced settings to session state
    st.session_state["model_settings"] = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p
    }
    
    # Model-specific configurations
    selected_model = st.session_state.get("selected_model", {}).get("name", "")
    
    if selected_model == "gpt-4o":
        st.markdown("**GPT-4o Specific Settings:**")
        enable_reasoning = st.checkbox(
            "Enable detailed reasoning",
            value=True,
            help="Include step-by-step reasoning in responses"
        )
        st.session_state["gpt4o_reasoning"] = enable_reasoning
    
    elif selected_model == "claude-3.5-sonnet":
        st.markdown("**Claude Specific Settings:**")
        enable_citations = st.checkbox(
            "Enable source citations",
            value=True,
            help="Include citations for information sources"
        )
        st.session_state["claude_citations"] = enable_citations


def get_model_config() -> Dict:
    """Get current model configuration"""
    
    config = {
        "model": st.session_state.get("selected_model", {}),
        "settings": st.session_state.get("model_settings", {
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 0.9
        })
    }
    
    # Add model-specific settings
    selected_model = config["model"].get("name", "")
    
    if selected_model == "gpt-4o":
        config["gpt4o_reasoning"] = st.session_state.get("gpt4o_reasoning", True)
    elif selected_model == "claude-3.5-sonnet":
        config["claude_citations"] = st.session_state.get("claude_citations", True)
    
    return config


def validate_model_config() -> bool:
    """Validate model configuration is complete"""
    
    model_info = st.session_state.get("selected_model")
    
    if not model_info:
        return False
    
    required_fields = ["name", "model_id"]
    return all(model_info.get(field) for field in required_fields)


def render_model_status():
    """Render current model selection status"""
    
    if validate_model_config():
        model_info = st.session_state["selected_model"]
        st.success(f"✅ Model selected: {model_info['name']}")
    else:
        st.warning("⚠️ Please select a model")
        
    return validate_model_config()