"""
Base agent functionality for LlamaIndex Presales AI System
"""
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
from abc import ABC, abstractmethod

import structlog
from llama_index.core.llms import ChatMessage, MessageRole

from ..llm_integration import get_agent_llm
from ..config import get_agent_prompt

logger = structlog.get_logger()


class BasePresalesAgent(ABC):
    """Base class for all presales agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.llm_wrapper = get_agent_llm(agent_name)
        self.prompt_config = get_agent_prompt(agent_name)
        self.system_prompt = self.prompt_config.get("system_prompt", "")
        self.response_format = self.prompt_config.get("response_format", {})
        
        logger.info(
            "Agent initialized",
            agent_name=agent_name,
            has_system_prompt=bool(self.system_prompt),
            response_format_keys=list(self.response_format.keys())
        )
    
    @abstractmethod
    async def process(
        self, 
        input_data: str, 
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Process input data and return structured output
        
        Args:
            input_data: Raw input to process
            context: Additional context from previous pipeline steps
            stream: Whether to stream the response
            
        Returns:
            Structured response with agent output
        """
        pass
    
    async def _llm_complete(
        self,
        input_data: str,
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> str:
        """Execute LLM completion with agent-specific prompt"""
        try:
            # Add format instructions to the prompt
            enhanced_prompt = self._enhance_prompt_with_format()
            
            response = await self.llm_wrapper.process_with_context(
                system_prompt=enhanced_prompt,
                user_input=input_data,
                context_data=context,
                stream=stream
            )
            
            logger.info(
                "Agent LLM completion successful",
                agent_name=self.agent_name,
                response_length=len(response)
            )
            
            return response
            
        except Exception as e:
            logger.error(
                "Agent LLM completion failed",
                agent_name=self.agent_name,
                error=str(e)
            )
            raise
    
    def _enhance_prompt_with_format(self) -> str:
        """Add response format instructions to system prompt"""
        if not self.response_format:
            return self.system_prompt
        
        format_instructions = "\n\nPlease structure your response using this format:\n"
        for key, description in self.response_format.items():
            format_instructions += f"- **{key}**: {description}\n"
        
        format_instructions += "\nProvide clear, actionable information for each section."
        
        return self.system_prompt + format_instructions
    
    def _create_structured_response(
        self,
        raw_response: str,
        step_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create structured response with metadata"""
        return {
            "agent_name": self.agent_name,
            "raw_output": raw_response,
            "processed_output": self._parse_structured_output(raw_response),
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "response_length": len(raw_response),
                "expected_format": list(self.response_format.keys()),
                **(step_metadata or {})
            }
        }
    
    def _parse_structured_output(self, raw_response: str) -> Dict[str, Any]:
        """
        Parse the LLM response into structured format
        This is a basic implementation - could be enhanced with more sophisticated parsing
        """
        parsed = {}
        
        # Simple parsing based on markdown-style headers
        current_section = None
        current_content = []
        
        lines = raw_response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check if line is a section header (starts with ** or #)
            if line.startswith('**') and line.endswith('**'):
                # Save previous section
                if current_section and current_content:
                    parsed[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.strip('*').lower().replace(' ', '_')
                current_content = []
                
            elif line.startswith('#'):
                # Handle markdown headers
                if current_section and current_content:
                    parsed[current_section] = '\n'.join(current_content).strip()
                
                current_section = line.strip('#').strip().lower().replace(' ', '_')
                current_content = []
                
            else:
                # Add content to current section
                if line:  # Skip empty lines
                    current_content.append(line)
        
        # Don't forget the last section
        if current_section and current_content:
            parsed[current_section] = '\n'.join(current_content).strip()
        
        # If no structured parsing worked, return the full response
        if not parsed:
            parsed["full_response"] = raw_response
        
        return parsed
    
    async def health_check(self) -> Dict[str, Any]:
        """Check agent health and readiness"""
        try:
            # Test with simple input
            test_response = await self._llm_complete("Health check test")
            
            return {
                "agent_name": self.agent_name,
                "status": "healthy",
                "llm_responsive": bool(test_response),
                "system_prompt_length": len(self.system_prompt),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "agent_name": self.agent_name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


class AgentStep:
    """Represents a single step in the agent pipeline"""
    
    def __init__(self, step_number: int, agent: BasePresalesAgent, description: str):
        self.step_number = step_number
        self.agent = agent
        self.description = description
        self.executed = False
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
    
    async def execute(
        self,
        input_data: str,
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Execute this agent step"""
        self.start_time = datetime.utcnow()
        
        try:
            logger.info(
                "Executing agent step",
                step_number=self.step_number,
                agent_name=self.agent.agent_name,
                description=self.description
            )
            
            self.result = await self.agent.process(input_data, context, stream)
            self.executed = True
            self.end_time = datetime.utcnow()
            
            # Calculate execution time
            execution_time = (self.end_time - self.start_time).total_seconds()
            
            logger.info(
                "Agent step completed",
                step_number=self.step_number,
                agent_name=self.agent.agent_name,
                execution_time=execution_time
            )
            
            # Add execution metadata
            if self.result and isinstance(self.result, dict):
                self.result["execution_metadata"] = {
                    "step_number": self.step_number,
                    "execution_time": execution_time,
                    "started_at": self.start_time.isoformat(),
                    "completed_at": self.end_time.isoformat()
                }
            
            return self.result
            
        except Exception as e:
            self.error = str(e)
            self.end_time = datetime.utcnow()
            
            logger.error(
                "Agent step failed",
                step_number=self.step_number,
                agent_name=self.agent.agent_name,
                error=str(e)
            )
            
            raise
    
    @property
    def execution_time(self) -> Optional[float]:
        """Get execution time in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary for serialization"""
        return {
            "step_number": self.step_number,
            "agent_name": self.agent.agent_name,
            "description": self.description,
            "executed": self.executed,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "execution_time": self.execution_time,
            "result": self.result,
            "error": self.error
        }