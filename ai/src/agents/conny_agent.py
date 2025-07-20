"""
Conny Agent - Business consultant and solution architect
"""
from typing import Dict, Any, Optional, List
import structlog

from .base_agent import BasePresalesAgent

logger = structlog.get_logger()


class ConnyAgent(BasePresalesAgent):
    """
    Conny is a senior business consultant and solution architect who synthesizes
    customer insights into actionable business recommendations and solution designs.
    """
    
    def __init__(self):
        super().__init__("conny")
        
    async def process(
        self, 
        input_data: str, 
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Process requirements and create solution recommendations
        
        Args:
            input_data: Requirements analysis or project description request
            context: Previous agent outputs and conversation context
            stream: Whether to stream the response
            
        Returns:
            Solution architecture and business recommendations
        """
        try:
            logger.info(
                "Conny processing business consultation",
                input_length=len(input_data),
                has_context=bool(context)
            )
            
            # Determine consultation type based on context and input
            consultation_type = self._determine_consultation_type(input_data, context)
            
            # Prepare consultation prompt
            enhanced_input = self._prepare_consultation_prompt(
                input_data, 
                context, 
                consultation_type
            )
            
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
                    "consultation_type": consultation_type,
                    "solution_components": self._count_solution_components(raw_response),
                    "recommendations_count": self._count_recommendations(raw_response)
                }
            )
            
            logger.info(
                "Conny consultation completed",
                consultation_type=consultation_type,
                solution_components=result["metadata"]["solution_components"]
            )
            
            return result
            
        except Exception as e:
            logger.error("Conny processing failed", error=str(e))
            raise
    
    def _determine_consultation_type(
        self, 
        input_data: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Determine what type of consultation is needed"""
        
        input_lower = input_data.lower()
        
        # Check for specific consultation types
        if "project description" in input_lower or "solution approach" in input_lower:
            return "project_description"
        elif "quality review" in input_lower or "review" in input_lower:
            return "quality_review" 
        elif "pm handover" in input_lower or "handover" in input_lower:
            return "pm_handover"
        elif "requirements" in input_lower and context and context.get("previous_steps"):
            return "solution_design"
        else:
            return "general_consultation"
    
    def _prepare_consultation_prompt(
        self,
        input_data: str,
        context: Optional[Dict[str, Any]] = None,
        consultation_type: str = "general_consultation"
    ) -> str:
        """Prepare consultation prompt based on type"""
        
        base_context = ""
        if context and context.get("previous_steps"):
            base_context = "\n**PREVIOUS ANALYSIS:**\n"
            for step in context["previous_steps"]:
                base_context += f"**{step.get('agent', 'Unknown')}**: {step.get('output', '')[:200]}...\n\n"
        
        if consultation_type == "project_description":
            return f"""
{base_context}

Based on the customer requirements analysis above, create a comprehensive project description that includes:

**REQUEST:** {input_data}

Please provide:
1. **Solution Approach** - High-level strategy and methodology
2. **Architecture Overview** - Key components and integration points  
3. **Implementation Plan** - Phased delivery approach with timelines
4. **Value Proposition** - Business benefits and ROI potential
5. **Risk Assessment** - Potential challenges and mitigation strategies
6. **Resource Requirements** - Team structure and skill sets needed
7. **Success Metrics** - How we'll measure project success

Focus on practical, actionable recommendations that align with the customer's business objectives.
"""
        
        elif consultation_type == "quality_review":
            return f"""
{base_context}

Please review the project deliverables above for quality and completeness:

**REVIEW REQUEST:** {input_data}

Evaluate:
1. **Content Quality** - Accuracy, clarity, and completeness
2. **Business Alignment** - Match with customer requirements
3. **Technical Feasibility** - Realistic implementation approach
4. **Value Articulation** - Clear benefits and ROI
5. **Risk Coverage** - Comprehensive risk assessment
6. **Actionability** - Clear next steps and deliverables
7. **Professional Standards** - Presentation and formatting

Provide specific feedback and recommendations for improvement.
"""
        
        elif consultation_type == "pm_handover":
            return f"""
{base_context}

Create a comprehensive project manager handover document based on the analysis above:

**HANDOVER REQUEST:** {input_data}

Include:
1. **Executive Summary** - Project overview and objectives
2. **Customer Profile** - Key stakeholders and decision makers
3. **Requirements Summary** - Functional and non-functional requirements
4. **Solution Overview** - Recommended approach and architecture
5. **Implementation Roadmap** - Detailed project phases and milestones
6. **Risk Register** - Identified risks and mitigation plans
7. **Success Criteria** - Measurable outcomes and KPIs
8. **Next Steps** - Immediate actions and follow-up activities

This should be a zero-knowledge brief that enables a project manager to understand and execute the project.
"""
        
        elif consultation_type == "solution_design":
            return f"""
{base_context}

Based on the requirements analysis, design a comprehensive solution:

**SOLUTION REQUEST:** {input_data}

Design:
1. **Technical Architecture** - System components and data flows
2. **Integration Strategy** - How solution fits with existing systems
3. **Implementation Phases** - Logical delivery sequence
4. **Technology Stack** - Recommended tools and platforms
5. **Resource Plan** - Team size, roles, and timeline
6. **Investment Model** - Cost structure and ROI projections
7. **Change Management** - User adoption and training approach

Ensure the solution is scalable, maintainable, and aligned with customer objectives.
"""
        
        else:  # general_consultation
            return f"""
{base_context}

Provide strategic business consulting on the following:

**CONSULTATION REQUEST:** {input_data}

Please analyze and recommend:
1. **Strategic Approach** - Best path forward
2. **Business Impact** - Expected outcomes and benefits
3. **Implementation Considerations** - Key factors for success
4. **Risk Mitigation** - Potential challenges and solutions
5. **Resource Optimization** - Efficient use of time and budget
6. **Success Factors** - Critical elements for project success

Provide actionable insights and clear recommendations.
"""
    
    def _count_solution_components(self, response: str) -> int:
        """Count solution components mentioned"""
        components = 0
        component_keywords = [
            "component", "module", "service", "system", "platform",
            "integration", "database", "api", "interface", "dashboard"
        ]
        
        for keyword in component_keywords:
            components += response.lower().count(keyword)
        
        return components
    
    def _count_recommendations(self, response: str) -> int:
        """Count recommendations provided"""
        recommendations = 0
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip().lower()
            if any(word in line for word in ["recommend", "suggest", "propose", "should"]):
                recommendations += 1
        
        return recommendations
    
    async def create_solution_architecture(
        self, 
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create detailed solution architecture from requirements
        
        Args:
            requirements: Structured requirements from Conversa
            
        Returns:
            Detailed solution architecture and implementation plan
        """
        architecture_request = f"""
Create a detailed solution architecture based on these requirements:

{requirements}

Focus on:
- System architecture and component design
- Integration patterns and data flows  
- Technology stack recommendations
- Scalability and performance considerations
- Security and compliance requirements
- Deployment and infrastructure needs
"""
        
        return await self.process(architecture_request, {"requirements": requirements})
    
    async def perform_quality_review(
        self, 
        deliverables: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Perform quality review of project deliverables
        
        Args:
            deliverables: List of project deliverables to review
            
        Returns:
            Quality assessment and improvement recommendations
        """
        review_content = "**DELIVERABLES FOR REVIEW:**\n\n"
        
        for i, deliverable in enumerate(deliverables, 1):
            review_content += f"**Deliverable {i}: {deliverable.get('type', 'Unknown')}**\n"
            review_content += f"{deliverable.get('content', '')}\n\n"
        
        review_request = "Please perform a comprehensive quality review of these project deliverables."
        
        return await self.process(review_request, {"deliverables": deliverables})
    
    async def create_pm_handover(
        self, 
        project_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create project manager handover document
        
        Args:
            project_context: Complete project context and analysis
            
        Returns:
            Comprehensive PM handover document
        """
        handover_request = """
Create a comprehensive project manager handover document that enables
a PM to understand and execute this project with zero additional context.
"""
        
        return await self.process(
            handover_request, 
            {"project_context": project_context}
        )