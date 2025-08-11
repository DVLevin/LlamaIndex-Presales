"""
Input Router Agent - Intelligent analysis and routing for any business input
Analyzes content and creates structured JSON for multi-agent pipeline routing
"""
from typing import Dict, Any, List, Optional
import json
import re
from datetime import datetime
import structlog

from .base_agent import BasePresalesAgent

logger = structlog.get_logger()


class InputRouterAgent(BasePresalesAgent):
    """
    Input Router Agent specializes in analyzing any business input and creating
    structured routing information for the multi-agent pipeline.
    
    Handles:
    - Transcript detection and classification
    - Industry and solution type identification  
    - Stakeholder and decision-maker extraction
    - RAG search term generation for past proposal context
    - Dynamic agent routing recommendations
    """
    
    def __init__(self):
        super().__init__("input_router")
        
    async def process(
        self, 
        input_data: str, 
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze business input and create structured routing JSON
        
        Args:
            input_data: Raw business content (transcript, notes, ideas, etc.)
            context: Additional context (customer name, content type hints, etc.)
            stream: Whether to stream the response
            
        Returns:
            Structured routing information for multi-agent pipeline
        """
        try:
            logger.info(
                "Input Router processing content",
                content_length=len(input_data),
                has_context=bool(context)
            )
            
            # Enhance input for router analysis
            enhanced_input = self._prepare_router_analysis(input_data, context)
            
            # Get LLM analysis
            raw_response = await self._llm_complete(
                enhanced_input,
                context=context,
                stream=stream
            )
            
            # Parse and structure the response
            routing_info = self._parse_routing_response(raw_response, input_data, context)
            
            logger.info(
                "Input Router analysis complete",
                transcript_detected=routing_info.get("transcript", False),
                industry=routing_info.get("industry", "unknown"),
                agent_routing=routing_info.get("agent_routing", {})
            )
            
            return routing_info
            
        except Exception as e:
            logger.error(
                "Input Router processing failed",
                error=str(e),
                content_length=len(input_data) if input_data else 0
            )
            return self._create_fallback_routing(input_data, context)
    
    def _prepare_router_analysis(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Prepare input for intelligent router analysis"""
        
        analysis_prompt = f"""
BUSINESS INPUT ANALYSIS TASK:

Analyze the following business content and create a structured routing plan for our multi-agent proposal system.

INPUT CONTENT:
{input_data}

CONTEXT INFORMATION:
{json.dumps(context, indent=2) if context else "No additional context provided"}

ANALYSIS REQUIREMENTS:

1. TRANSCRIPT DETECTION:
   - Determine if this is a customer transcript/conversation (yes/no)
   - Look for conversation patterns, speaker labels, Q&A format
   
2. CONTENT CLASSIFICATION:
   - Primary type: customer_transcript, strategic_planning, competitive_analysis, solution_requirements, feedback_ideas, general_business
   - Confidence level: high/medium/low

3. BUSINESS METADATA EXTRACTION:
   - Industry: technology, manufacturing, healthcare, finance, retail, education, real_estate, other
   - Company size: startup, small, medium, enterprise, unknown
   - Solution type: automation, analytics, integration, transformation, optimization, security, custom
   - Urgency level: low, medium, high, critical
   - Budget indicators: specific amounts, ranges, or constraints mentioned
   - Timeline: specific dates, durations, or deadlines mentioned

4. STAKEHOLDER ANALYSIS:
   - Decision makers: C-level, VP, Director, Manager roles identified
   - Influencers: Technical leads, department heads, team leads
   - End users: People who will use the solution
   - Procurement: Purchasing, legal, compliance stakeholders

5. REQUIREMENTS EXTRACTION:
   - Functional requirements: what the solution must do
   - Technical requirements: platforms, integrations, specifications
   - Business requirements: outcomes, metrics, success criteria
   - Constraints: budget, timeline, technical, regulatory

6. RAG SEARCH OPTIMIZATION:
   - Key search terms: important business concepts for finding similar past proposals
   - Industry-specific terms: sector-relevant terminology
   - Solution keywords: technical and business solution terms
   - Company identifiers: size, type, geographic indicators

7. AGENT ROUTING RECOMMENDATIONS:
   - Which agents should process this content
   - Suggested processing order
   - Special instructions for each agent
   - Skip conditions (when to bypass certain agents)

8. COMPETITIVE INTELLIGENCE:
   - Competitors mentioned or implied
   - Competitive advantages to highlight
   - Differentiation opportunities
   - Market positioning insights

Provide a comprehensive analysis following this structure.
"""
        
        return analysis_prompt
    
    def _parse_routing_response(self, raw_response: str, original_input: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse LLM response into structured routing information"""
        
        try:
            # Create structured routing information
            routing_info = {
                "timestamp": datetime.now().isoformat(),
                "original_content_length": len(original_input),
                "analysis_confidence": self._assess_analysis_confidence(raw_response),
                
                # Core routing decision
                "transcript": self._extract_transcript_decision(raw_response, original_input),
                
                # Content classification
                "content_type": self._extract_content_type(raw_response),
                "content_confidence": self._extract_confidence_level(raw_response),
                
                # Business metadata
                "industry": self._extract_industry(raw_response),
                "company_size": self._extract_company_size(raw_response),
                "solution_types": self._extract_solution_types(raw_response),
                "urgency_level": self._extract_urgency(raw_response),
                "budget_indicators": self._extract_budget_info(raw_response, original_input),
                "timeline_indicators": self._extract_timeline_info(raw_response, original_input),
                
                # Stakeholder information
                "stakeholders": {
                    "decision_makers": self._extract_decision_makers(raw_response, original_input),
                    "influencers": self._extract_influencers(raw_response, original_input),
                    "end_users": self._extract_end_users(raw_response, original_input),
                    "procurement": self._extract_procurement_stakeholders(raw_response, original_input)
                },
                
                # Requirements extraction
                "requirements": {
                    "functional": self._extract_functional_requirements(raw_response),
                    "technical": self._extract_technical_requirements(raw_response),
                    "business": self._extract_business_requirements(raw_response),
                    "constraints": self._extract_constraints(raw_response)
                },
                
                # RAG optimization
                "rag_search_terms": self._extract_rag_search_terms(raw_response, original_input),
                "similar_proposal_indicators": self._generate_similarity_indicators(raw_response),
                
                # Agent routing
                "agent_routing": self._create_agent_routing_plan(raw_response),
                
                # Competitive intelligence
                "competitive_context": {
                    "competitors_mentioned": self._extract_competitors(raw_response, original_input),
                    "differentiation_opportunities": self._extract_differentiation_opps(raw_response),
                    "market_positioning": self._extract_market_positioning(raw_response)
                },
                
                # Processing metadata
                "processing_hints": self._create_processing_hints(raw_response, context),
                "quality_indicators": self._assess_content_quality(original_input, raw_response)
            }
            
            return routing_info
            
        except Exception as e:
            logger.error("Failed to parse routing response", error=str(e))
            return self._create_fallback_routing(original_input, context)
    
    def _extract_transcript_decision(self, analysis: str, original_input: str) -> bool:
        """Determine if content is a transcript"""
        
        # LLM analysis check
        analysis_lower = analysis.lower()
        if any(phrase in analysis_lower for phrase in [
            "is a transcript", "transcript: yes", "conversation transcript",
            "customer transcript", "call recording", "interview transcript"
        ]):
            return True
        
        if any(phrase in analysis_lower for phrase in [
            "not a transcript", "transcript: no", "not conversational",
            "strategic document", "planning document"
        ]):
            return False
        
        # Fallback: pattern-based detection
        return self._pattern_based_transcript_detection(original_input)
    
    def _pattern_based_transcript_detection(self, content: str) -> bool:
        """Pattern-based transcript detection as fallback"""
        
        transcript_patterns = [
            r'\\b(Customer|Client|Prospect|Interviewer):\\s',
            r'\\b(Sales|Rep|Account Manager|Moderator):\\s', 
            r'\\b\\w+:\\s+[A-Z].*[.!?]',  # "Speaker: Sentence" pattern
            r'\\[\\d{1,2}:\\d{2}\\]',  # Timestamps
            r'Q\\d+:|Question \\d+:',  # Question numbering
            r'A\\d+:|Answer \\d+:'  # Answer numbering
        ]
        
        pattern_matches = sum(1 for pattern in transcript_patterns 
                             if re.search(pattern, content, re.IGNORECASE))
        
        return pattern_matches >= 2
    
    def _extract_content_type(self, analysis: str) -> str:
        """Extract primary content type from analysis"""
        
        content_types = [
            "customer_transcript", "strategic_planning", "competitive_analysis",
            "solution_requirements", "feedback_ideas", "general_business"
        ]
        
        analysis_lower = analysis.lower()
        for content_type in content_types:
            if content_type.replace("_", " ") in analysis_lower:
                return content_type
        
        return "general_business"
    
    def _extract_industry(self, analysis: str) -> str:
        """Extract industry from analysis"""
        
        industries = [
            "technology", "manufacturing", "healthcare", "finance", 
            "retail", "education", "real_estate"
        ]
        
        analysis_lower = analysis.lower()
        for industry in industries:
            if industry in analysis_lower:
                return industry
        
        return "unknown"
    
    def _extract_solution_types(self, analysis: str) -> List[str]:
        """Extract solution types from analysis"""
        
        solution_types = [
            "automation", "analytics", "integration", "transformation",
            "optimization", "security"
        ]
        
        found_types = []
        analysis_lower = analysis.lower()
        
        for solution_type in solution_types:
            if solution_type in analysis_lower:
                found_types.append(solution_type)
        
        return found_types or ["custom"]
    
    def _create_agent_routing_plan(self, analysis: str) -> Dict[str, Any]:
        """Create agent routing plan based on analysis"""
        
        analysis_lower = analysis.lower()
        
        routing_plan = {
            "conversa": {
                "execute": "transcript" in analysis_lower or "conversation" in analysis_lower,
                "priority": 1,
                "special_instructions": "Focus on extracting structured requirements from conversation"
            },
            "conny": {
                "execute": True,  # Always run business consulting
                "priority": 2,
                "special_instructions": "Leverage industry and solution type context for strategic recommendations"
            },
            "prody": {
                "execute": True,  # Always generate documents
                "priority": 3,
                "special_instructions": "Customize document templates based on industry and solution type"
            },
            "preston": {
                "execute": "optimization" in analysis_lower or "process" in analysis_lower,
                "priority": 4,
                "special_instructions": "Focus on process optimization and efficiency improvements"
            },
            "marketing": {
                "execute": True,  # Always create sales materials
                "priority": 5,
                "special_instructions": "Tailor messaging based on stakeholder analysis and competitive context"
            }
        }
        
        return routing_plan
    
    def _extract_rag_search_terms(self, analysis: str, original_input: str) -> List[str]:
        """Extract key terms for RAG search of past proposals"""
        
        # Extract from LLM analysis
        search_terms = []
        
        # Look for explicit search terms in analysis
        search_sections = re.findall(r'search terms?:([^\\n]+)', analysis, re.IGNORECASE)
        for section in search_sections:
            terms = [term.strip() for term in section.split(',')]
            search_terms.extend(terms)
        
        # Extract business concepts from original input
        business_patterns = [
            r'\\b\\w+\\s+(platform|system|solution|service|tool|software)\\b',
            r'\\b(implement|deploy|integrate|optimize|automate|modernize)\\s+\\w+\\b',
            r'\\b\\w+\\s+(management|analytics|reporting|dashboard)\\b'
        ]
        
        for pattern in business_patterns:
            matches = re.findall(pattern, original_input, re.IGNORECASE)
            search_terms.extend([match.lower() for match in matches])
        
        # Add industry and solution type terms
        industry = self._extract_industry(analysis)
        if industry != "unknown":
            search_terms.append(industry)
        
        solution_types = self._extract_solution_types(analysis)
        search_terms.extend(solution_types)
        
        # Return unique terms, limited to top 15
        return list(dict.fromkeys(search_terms))[:15]
    
    def _create_fallback_routing(self, input_data: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Create fallback routing when analysis fails"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "original_content_length": len(input_data) if input_data else 0,
            "analysis_confidence": "low",
            "fallback_mode": True,
            
            "transcript": self._pattern_based_transcript_detection(input_data) if input_data else False,
            "content_type": "general_business",
            "industry": "unknown",
            "solution_types": ["custom"],
            "urgency_level": "medium",
            
            "agent_routing": {
                "conversa": {"execute": True, "priority": 1},
                "conny": {"execute": True, "priority": 2},
                "prody": {"execute": True, "priority": 3},
                "preston": {"execute": False, "priority": 4},
                "marketing": {"execute": True, "priority": 5}
            },
            
            "rag_search_terms": ["business solution", "proposal", "consulting"],
            "processing_hints": {"mode": "fallback", "use_default_templates": True}
        }
    
    # Helper methods for extracting specific information
    def _extract_confidence_level(self, analysis: str) -> str:
        """Extract confidence level from analysis"""
        analysis_lower = analysis.lower()
        if "high confidence" in analysis_lower or "confident" in analysis_lower:
            return "high"
        elif "medium confidence" in analysis_lower or "moderate" in analysis_lower:
            return "medium"
        else:
            return "low"
    
    def _extract_company_size(self, analysis: str) -> str:
        """Extract company size indicators"""
        analysis_lower = analysis.lower()
        if any(term in analysis_lower for term in ["enterprise", "large", "fortune", "corporation"]):
            return "enterprise"
        elif any(term in analysis_lower for term in ["medium", "mid-size", "growing"]):
            return "medium"
        elif any(term in analysis_lower for term in ["small", "startup", "sme"]):
            return "small"
        else:
            return "unknown"
    
    def _extract_urgency(self, analysis: str) -> str:
        """Extract urgency level from analysis"""
        analysis_lower = analysis.lower()
        if any(term in analysis_lower for term in ["critical", "urgent", "emergency", "asap"]):
            return "critical"
        elif any(term in analysis_lower for term in ["high", "priority", "soon", "quickly"]):
            return "high"
        elif any(term in analysis_lower for term in ["medium", "moderate", "standard"]):
            return "medium"
        else:
            return "low"
    
    def _extract_budget_info(self, analysis: str, original_input: str) -> List[str]:
        """Extract budget information"""
        budget_patterns = [
            r'\\$[\\d,]+[km]?\\b',
            r'budget[^\\n]*\\$[\\d,]+',
            r'investment[^\\n]*\\$[\\d,]+',
            r'[\\d,]+\\s+dollars?'
        ]
        
        budget_info = []
        combined_text = f"{analysis} {original_input}"
        
        for pattern in budget_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            budget_info.extend(matches)
        
        return list(set(budget_info))[:5]
    
    def _extract_timeline_info(self, analysis: str, original_input: str) -> List[str]:
        """Extract timeline information"""
        timeline_patterns = [
            r'\\d+\\s+(weeks?|months?|years?|days?)\\b',
            r'by\\s+(january|february|march|april|may|june|july|august|september|october|november|december)',
            r'Q[1-4]\\s+\\d{4}',
            r'end\\s+of\\s+\\w+',
            r'next\\s+(week|month|quarter|year)'
        ]
        
        timeline_info = []
        combined_text = f"{analysis} {original_input}"
        
        for pattern in timeline_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            timeline_info.extend(matches)
        
        return list(set(timeline_info))[:5]
    
    def _extract_decision_makers(self, analysis: str, original_input: str) -> List[str]:
        """Extract decision makers from content"""
        decision_maker_patterns = [
            r'\\b(CEO|CTO|CFO|COO|President|VP|Vice President)\\b',
            r'\\b(Director|Manager|Head)\\s+of\\s+\\w+',
            r'\\b(Decision maker|Stakeholder|Owner)\\b'
        ]
        
        decision_makers = []
        combined_text = f"{analysis} {original_input}"
        
        for pattern in decision_maker_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            decision_makers.extend(matches)
        
        return list(set(decision_makers))[:5]
    
    # Additional helper methods would be implemented similarly...
    def _extract_influencers(self, analysis: str, original_input: str) -> List[str]:
        return []  # Placeholder - implement similar to _extract_decision_makers
    
    def _extract_end_users(self, analysis: str, original_input: str) -> List[str]:
        return []  # Placeholder - implement similar to _extract_decision_makers
    
    def _extract_procurement_stakeholders(self, analysis: str, original_input: str) -> List[str]:
        return []  # Placeholder - implement similar to _extract_decision_makers
    
    def _extract_functional_requirements(self, analysis: str) -> List[str]:
        return []  # Placeholder - extract functional requirements
    
    def _extract_technical_requirements(self, analysis: str) -> List[str]:
        return []  # Placeholder - extract technical requirements
    
    def _extract_business_requirements(self, analysis: str) -> List[str]:
        return []  # Placeholder - extract business requirements
    
    def _extract_constraints(self, analysis: str) -> List[str]:
        return []  # Placeholder - extract constraints
    
    def _generate_similarity_indicators(self, analysis: str) -> List[str]:
        return []  # Placeholder - generate indicators for similar proposals
    
    def _extract_competitors(self, analysis: str, original_input: str) -> List[str]:
        return []  # Placeholder - extract competitor mentions
    
    def _extract_differentiation_opps(self, analysis: str) -> List[str]:
        return []  # Placeholder - extract differentiation opportunities
    
    def _extract_market_positioning(self, analysis: str) -> str:
        return "unknown"  # Placeholder - extract market positioning
    
    def _create_processing_hints(self, analysis: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {"mode": "standard"}  # Placeholder - create processing hints
    
    def _assess_content_quality(self, original_input: str, analysis: str) -> Dict[str, Any]:
        return {"quality": "medium", "completeness": "partial"}  # Placeholder - assess content quality
    
    def _assess_analysis_confidence(self, analysis: str) -> str:
        return "medium"  # Placeholder - assess analysis confidence