"""
AI-specific configuration for LlamaIndex Presales AI System
"""
import os
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class AISettings(BaseSettings):
    """AI service configuration settings"""
    
    # LLM Configuration
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    default_llm_model: str = Field("moonshotai/kimi-k2", env="DEFAULT_LLM_MODEL")
    llm_temperature: float = Field(0.1, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(4000, env="LLM_MAX_TOKENS")
    llm_timeout: int = Field(60, env="LLM_TIMEOUT")
    
    # Jina AI Configuration
    jina_api_key: str = Field(..., env="JINA_API_KEY")
    default_embedding_model: str = Field("jina-embeddings-v2-base-en", env="DEFAULT_EMBEDDING_MODEL")
    default_reranker_model: str = Field("jina-reranker-v1-base-en", env="DEFAULT_RERANKER_MODEL")
    embedding_dimensions: int = Field(768, env="EMBEDDING_DIMENSIONS")
    
    # Vector Database Configuration
    vector_db_path: str = Field("./vector_db", env="VECTOR_DB_PATH")
    vector_collection_name: str = Field("presales_knowledge", env="VECTOR_COLLECTION_NAME")
    similarity_top_k: int = Field(5, env="SIMILARITY_TOP_K")
    rerank_top_k: int = Field(3, env="RERANK_TOP_K")
    
    # Agent Configuration
    agent_max_iterations: int = Field(10, env="AGENT_MAX_ITERATIONS")
    agent_timeout: int = Field(300, env="AGENT_TIMEOUT")  # 5 minutes
    streaming_enabled: bool = Field(True, env="STREAMING_ENABLED")
    
    # Document Processing
    max_chunk_size: int = Field(1000, env="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    supported_file_types: list = Field(
        ["txt", "pdf", "docx", "md"], 
        env="SUPPORTED_FILE_TYPES"
    )
    
    # Pipeline Configuration
    pipeline_retry_attempts: int = Field(3, env="PIPELINE_RETRY_ATTEMPTS")
    pipeline_step_timeout: int = Field(120, env="PIPELINE_STEP_TIMEOUT")  # 2 minutes per step
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields from .env


# Agent-specific prompt templates
AGENT_PROMPTS = {
    "conversa": {
        "system_prompt": """You are Conversa, a specialized transcript analysis expert with deep expertise in customer discovery conversations.

Your role is to extract structured insights from customer transcripts, focusing on:
- Business requirements and pain points
- Stakeholder identification and decision-making structure  
- Technical constraints and preferences
- Budget and timeline indicators
- Success criteria and expected outcomes

Always maintain a professional, analytical tone and provide structured output that can be easily consumed by business consultants.""",
        
        "response_format": {
            "requirements": "List of explicit business requirements",
            "pain_points": "Customer challenges and frustrations",
            "stakeholders": "Decision makers and influencers identified",
            "constraints": "Technical, budget, or timeline limitations",
            "success_metrics": "Customer-defined success criteria"
        }
    },
    
    "conny": {
        "system_prompt": """You are Conny, a senior business consultant and solution architect with extensive experience in enterprise sales.

Your role is to synthesize customer insights into actionable business recommendations:
- Analyze requirements and recommend optimal solutions
- Design solution architecture and implementation approach
- Assess competitive positioning and differentiation opportunities
- Provide strategic guidance on proposal approach
- Ensure alignment between customer needs and company capabilities

You excel at translating technical requirements into business value and creating compelling solution narratives.""",
        
        "response_format": {
            "solution_approach": "Recommended solution strategy",
            "architecture_overview": "High-level solution design",
            "implementation_plan": "Phased delivery approach",
            "value_proposition": "Key business benefits and ROI",
            "competitive_position": "Differentiation and positioning"
        }
    },
    
    "prody": {
        "system_prompt": """You are ProDy, an expert product manager and technical documentation specialist.

Your role is to create comprehensive project documentation and deliverables:
- Generate detailed problem analysis documents
- Create process flow diagrams and visualizations
- Develop investment proposals with roadmaps and timelines
- Produce technical specifications and requirements
- Ensure all documentation follows professional standards

You are meticulous about structure, clarity, and actionability in all documentation.""",
        
        "response_format": {
            "document_type": "Type of document being generated",
            "content_outline": "Structured outline of document sections",
            "key_sections": "Main content blocks with detailed information",
            "diagrams_needed": "Mermaid diagrams or visualizations required",
            "next_steps": "Recommended follow-up actions"
        }
    },
    
    "marketing": {
        "system_prompt": """You are the Marketing Agent, a specialist in creating compelling customer-facing sales materials.

Your role is to transform technical proposals into persuasive sales presentations:
- Craft customer-centric value propositions
- Design engaging presentation flow and messaging
- Highlight business benefits and competitive advantages
- Create visually appealing slide structures
- Ensure messaging resonates with target audience

You excel at translating complex solutions into clear, compelling business narratives that drive decision-making.""",
        
        "response_format": {
            "presentation_outline": "Slide-by-slide presentation structure",
            "key_messages": "Core value propositions and benefits",
            "customer_benefits": "Specific benefits for this customer",
            "call_to_action": "Next steps and decision framework",
            "visual_elements": "Suggested charts, diagrams, and graphics"
        }
    }
}


# Document templates for consistent output
DOCUMENT_TEMPLATES = {
    "problem_overview": {
        "title": "Problem Overview and Analysis",
        "sections": [
            "Executive Summary",
            "Current State Assessment", 
            "Key Challenges and Pain Points",
            "Business Impact Analysis",
            "Success Criteria Definition"
        ]
    },
    
    "process_overview": {
        "title": "Solution Process and Methodology",
        "sections": [
            "Approach Overview",
            "Implementation Phases",
            "Key Activities and Deliverables",
            "Resource Requirements",
            "Timeline and Milestones"
        ]
    },
    
    "investment_proposal": {
        "title": "Investment Proposal and Business Case",
        "sections": [
            "Investment Summary",
            "Cost-Benefit Analysis",
            "ROI Projections",
            "Risk Assessment and Mitigation",
            "Recommended Next Steps"
        ]
    },
    
    "sales_deck": {
        "title": "Executive Presentation",
        "sections": [
            "Executive Summary",
            "Understanding Your Challenges", 
            "Our Recommended Approach",
            "Expected Business Outcomes",
            "Investment and Timeline",
            "Next Steps and Decision Process"
        ]
    }
}


# Global AI settings instance
ai_settings = AISettings()


def get_ai_settings() -> AISettings:
    """Get AI configuration settings"""
    return ai_settings


def get_agent_prompt(agent_name: str) -> Dict[str, Any]:
    """Get prompt configuration for specific agent"""
    return AGENT_PROMPTS.get(agent_name, {})


def get_document_template(template_name: str) -> Dict[str, Any]:
    """Get document template configuration"""
    return DOCUMENT_TEMPLATES.get(template_name, {})