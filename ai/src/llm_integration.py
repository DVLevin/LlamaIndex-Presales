"""
OpenRouter LLM integration for LlamaIndex Presales AI System
"""
import asyncio
import json
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
from llama_index.llms.openrouter import OpenRouter
from llama_index.core.llms import LLM
from llama_index.core.llms import ChatMessage, MessageRole

from .config import get_ai_settings

logger = structlog.get_logger()
settings = get_ai_settings()


class OpenRouterClient:
    """Enhanced OpenRouter client with streaming and error handling"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.openrouter_api_key
        self.model = model or settings.default_llm_model
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = settings.llm_timeout
        
        # Initialize LlamaIndex OpenRouter LLM
        self.llm = OpenRouter(
            api_key=self.api_key,
            model=self.model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            timeout=self.timeout
        )
        
        logger.info(
            "OpenRouter client initialized",
            model=self.model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def complete(
        self, 
        messages: List[ChatMessage], 
        **kwargs
    ) -> str:
        """
        Complete chat with retry logic and error handling
        
        Args:
            messages: List of ChatMessage objects
            **kwargs: Additional parameters for completion
            
        Returns:
            Generated response text
        """
        try:
            logger.debug("Starting LLM completion", model=self.model, message_count=len(messages))
            
            response = await self.llm.achat(messages, **kwargs)
            
            logger.info(
                "LLM completion successful",
                model=self.model,
                response_length=len(response.message.content)
            )
            
            return response.message.content
            
        except Exception as e:
            logger.error(
                "LLM completion failed",
                model=self.model,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    async def stream_complete(
        self, 
        messages: List[ChatMessage], 
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion for real-time updates
        
        Args:
            messages: List of ChatMessage objects
            **kwargs: Additional parameters for completion
            
        Yields:
            Streaming response chunks
        """
        try:
            logger.debug("Starting LLM streaming", model=self.model)
            
            response_stream = await self.llm.astream_chat(messages, **kwargs)
            
            async for chunk in response_stream:
                if chunk.delta:
                    yield chunk.delta
                    
        except Exception as e:
            logger.error(
                "LLM streaming failed",
                model=self.model, 
                error=str(e)
            )
            raise
    
    def create_messages(
        self, 
        system_prompt: str, 
        user_input: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> List[ChatMessage]:
        """
        Create ChatMessage objects for LLM completion
        
        Args:
            system_prompt: System instruction for the agent
            user_input: User's input or query
            conversation_history: Previous conversation messages
            
        Returns:
            List of formatted ChatMessage objects
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)
        ]
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history:
                role = MessageRole.USER if msg.get("role") == "user" else MessageRole.ASSISTANT
                messages.append(ChatMessage(role=role, content=msg.get("content", "")))
        
        # Add current user input
        messages.append(ChatMessage(role=MessageRole.USER, content=user_input))
        
        return messages
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check OpenRouter service health and model availability
        
        Returns:
            Health check results
        """
        try:
            # Test with simple completion
            messages = [
                ChatMessage(role=MessageRole.USER, content="Hello")
            ]
            
            response = await self.complete(messages)
            
            return {
                "status": "healthy",
                "model": self.model,
                "response_received": bool(response),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("OpenRouter health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "model": self.model,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


class AgentLLMWrapper:
    """Wrapper for agent-specific LLM interactions"""
    
    def __init__(self, agent_name: str, client: Optional[OpenRouterClient] = None):
        self.agent_name = agent_name
        self.client = client or OpenRouterClient()
        
    async def process_with_context(
        self,
        system_prompt: str,
        user_input: str,
        context_data: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> str:
        """
        Process input with agent-specific context and formatting
        
        Args:
            system_prompt: Agent's system instruction
            user_input: Input to process
            context_data: Additional context (previous steps, etc.)
            stream: Whether to use streaming completion
            
        Returns:
            Processed response
        """
        try:
            # Format input with context if provided
            formatted_input = self._format_input_with_context(user_input, context_data)
            
            # Create messages
            messages = self.client.create_messages(system_prompt, formatted_input)
            
            # Process with or without streaming
            if stream:
                response_parts = []
                async for chunk in self.client.stream_complete(messages):
                    response_parts.append(chunk)
                    # Could emit streaming events here for real-time updates
                
                return "".join(response_parts)
            else:
                return await self.client.complete(messages)
                
        except Exception as e:
            logger.error(
                "Agent LLM processing failed",
                agent_name=self.agent_name,
                error=str(e)
            )
            raise
    
    def _format_input_with_context(
        self, 
        user_input: str, 
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format user input with additional context"""
        if not context_data:
            return user_input
        
        context_sections = []
        
        # Add previous step outputs
        if context_data.get("previous_steps"):
            context_sections.append("## Previous Pipeline Steps:")
            for step in context_data["previous_steps"]:
                context_sections.append(f"**{step['agent']}**: {step['output']}")
        
        # Add conversation metadata
        if context_data.get("conversation_metadata"):
            context_sections.append("## Conversation Context:")
            metadata = context_data["conversation_metadata"]
            for key, value in metadata.items():
                context_sections.append(f"- **{key}**: {value}")
        
        # Combine with user input
        if context_sections:
            return f"{chr(10).join(context_sections)}\n\n## Current Task:\n{user_input}"
        
        return user_input


# Global client instances
_openrouter_client: Optional[OpenRouterClient] = None
_agent_llm_wrappers: Dict[str, AgentLLMWrapper] = {}


def get_openrouter_client() -> OpenRouterClient:
    """Get shared OpenRouter client instance"""
    global _openrouter_client
    if _openrouter_client is None:
        _openrouter_client = OpenRouterClient()
    return _openrouter_client


def get_agent_llm(agent_name: str) -> AgentLLMWrapper:
    """Get agent-specific LLM wrapper"""
    global _agent_llm_wrappers
    if agent_name not in _agent_llm_wrappers:
        _agent_llm_wrappers[agent_name] = AgentLLMWrapper(agent_name)
    return _agent_llm_wrappers[agent_name]


async def test_llm_integration() -> Dict[str, Any]:
    """Test LLM integration functionality"""
    try:
        client = get_openrouter_client()
        
        # Test basic completion
        messages = [
            ChatMessage(
                role=MessageRole.USER, 
                content="Respond with 'LLM integration test successful' if you can understand this."
            )
        ]
        
        response = await client.complete(messages)
        
        # Test agent wrapper
        agent_llm = get_agent_llm("conversa")
        agent_response = await agent_llm.process_with_context(
            system_prompt="You are a test agent. Respond briefly.",
            user_input="Test agent wrapper functionality."
        )
        
        return {
            "status": "success",
            "llm_response": response,
            "agent_response": agent_response,
            "model": client.model,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }