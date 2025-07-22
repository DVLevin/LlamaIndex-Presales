"""
Model Selection Component for Streamlit Application
Handle LLM model selection and configuration
"""
import streamlit as st
from typing import Dict, Optional
from streamlit_app.config import AppConfig


def render_model_selection(config: AppConfig):
    """Render model selection interface"""
    
    st.markdown("### 🤖 Model Configuration")
    
    # Model selection dropdown
    selected_model_key = st.selectbox(
        "Select LLM Model",
        options=list(config.available_models.keys()),
        index=0,
        help="Choose the language model for AI agent processing"
    )
    
    # Save selection to session state
    st.session_state["selected_model"] = {
        "name": selected_model_key,
        "model_id": config.available_models[selected_model_key]
    }
    
    # Display model information
    with st.expander("Model Information", expanded=False):
        display_model_info(selected_model_key)
    
    # Advanced model configuration
    with st.expander("Advanced Model Settings", expanded=False):
        render_advanced_model_settings()


def display_model_info(model_key: str):
    """Display information about the selected model"""
    
    model_descriptions = {
        "gpt-4o": {
            "provider": "OpenAI",
            "description": "Latest GPT-4 model with improved reasoning and multimodal capabilities",
            "strengths": ["Complex reasoning", "Business writing", "Document analysis"],
            "ideal_for": "General purpose, high-quality output"
        },
        "claude-3.5-sonnet": {
            "provider": "Anthropic", 
            "description": "Advanced reasoning model with strong analytical capabilities",
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