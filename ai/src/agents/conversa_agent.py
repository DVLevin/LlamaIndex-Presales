"""
Conversa Agent - Transcript analysis and requirement extraction specialist
"""
from typing import Dict, Any, Optional
import structlog

from .base_agent import BasePresalesAgent

logger = structlog.get_logger()


class ConversaAgent(BasePresalesAgent):
    """
    Conversa specializes in analyzing customer discovery call transcripts
    and extracting structured business requirements and insights.
    """
    
    def __init__(self):
        super().__init__("conversa")
        
    async def process(
        self, 
        input_data: str, 
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze transcript and extract structured requirements
        
        Args:
            input_data: Customer transcript text
            context: Additional context (conversation metadata, etc.)
            stream: Whether to stream the response
            
        Returns:
            Structured analysis with requirements, pain points, stakeholders, etc.
        """
        try:
            logger.info(
                "Conversa processing transcript",
                transcript_length=len(input_data),
                has_context=bool(context)
            )
            
            # Enhance input with analysis instructions
            enhanced_input = self._prepare_transcript_analysis(input_data, context)
            
            # Process with LLM
            raw_response = await self._llm_complete(
                enhanced_input, 
                context, 
                stream
            )
            
            # Create structured response
            result = self._create_structured_response(
                raw_response,
                step_metadata={
                    "analysis_type": "transcript_analysis",
                    "transcript_length": len(input_data),
                    "extracted_sections": self._count_extracted_sections(raw_response)
                }
            )
            
            logger.info(
                "Conversa analysis completed",
                sections_extracted=result["metadata"]["extracted_sections"],
                output_length=len(raw_response)
            )
            
            return result
            
        except Exception as e:
            logger.error("Conversa processing failed", error=str(e))
            raise
    
    def _prepare_transcript_analysis(
        self, 
        transcript: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Prepare transcript for analysis with context and instructions"""
        
        analysis_instructions = """
Please analyze the following customer discovery call transcript and extract key business insights:

**TRANSCRIPT TO ANALYZE:**
---
{transcript}
---

Focus on identifying:
1. **Explicit requirements** mentioned by the customer
2. **Pain points and challenges** they're experiencing
3. **Key stakeholders** involved in decision-making
4. **Technical constraints** or preferences mentioned
5. **Budget and timeline** indicators
6. **Success criteria** or desired outcomes
7. **Current solutions** they're using or evaluating
8. **Decision-making process** and next steps

Provide specific quotes from the transcript where relevant to support your analysis.
"""
        
        formatted_input = analysis_instructions.format(transcript=transcript)
        
        # Add context information if available
        if context and context.get("conversation_metadata"):
            metadata = context["conversation_metadata"]
            context_section = "\n\n**CONVERSATION CONTEXT:**\n"
            for key, value in metadata.items():
                context_section += f"- {key}: {value}\n"
            formatted_input = context_section + formatted_input
        
        return formatted_input
    
    def _count_extracted_sections(self, response: str) -> int:
        """Count how many analysis sections were extracted"""
        # Count markdown headers and bold sections
        sections = 0
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('**') and line.endswith('**'):
                sections += 1
            elif line.startswith('#'):
                sections += 1
        
        return sections
    
    async def analyze_requirements(
        self, 
        transcript: str, 
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Focused requirement analysis with specific areas of interest
        
        Args:
            transcript: Customer transcript
            focus_areas: Specific areas to focus analysis on
            
        Returns:
            Focused requirement analysis
        """
        context = {
            "analysis_focus": focus_areas or [
                "technical_requirements",
                "business_requirements", 
                "timeline_requirements",
                "budget_constraints"
            ]
        }
        
        return await self.process(transcript, context)
    
    async def extract_stakeholders(self, transcript: str) -> Dict[str, Any]:
        """
        Extract stakeholder information and decision-making structure
        
        Args:
            transcript: Customer transcript
            
        Returns:
            Stakeholder analysis with roles and influence levels
        """
        stakeholder_prompt = f"""
Analyze this transcript specifically for stakeholder information:

{transcript}

Extract:
1. **Decision Makers** - Who has final authority?
2. **Influencers** - Who influences the decision?
3. **Technical Evaluators** - Who assesses technical aspects?
4. **Budget Owners** - Who controls the budget?
5. **End Users** - Who will use the solution?
6. **Project Champions** - Who advocates for the project?

For each stakeholder, identify:
- Name/Role mentioned
- Department/Function
- Level of influence (High/Medium/Low)
- Key concerns or interests
- Decision-making involvement
"""
        
        raw_response = await self._llm_complete(stakeholder_prompt)
        
        return self._create_structured_response(
            raw_response,
            step_metadata={
                "analysis_type": "stakeholder_extraction",
                "stakeholder_count": self._count_stakeholders(raw_response)
            }
        )
    
    def _count_stakeholders(self, response: str) -> int:
        """Count identified stakeholders"""
        # Simple heuristic - count bullet points and numbered items
        count = 0
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '* ', '1.', '2.', '3.', '4.', '5.')):
                if any(keyword in line.lower() for keyword in ['name', 'role', 'title', 'manager', 'director', 'ceo', 'cto']):
                    count += 1
        
        return count