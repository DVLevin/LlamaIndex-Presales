"""
ProDy Agent - Product Manager & Documentation Specialist

Generates comprehensive project documentation and deliverables:
- Problem analysis documents
- Process flow diagrams and visualizations  
- Investment proposals with roadmaps
- Technical specifications and requirements
"""

from typing import Dict, Any, List, Optional
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from .base_agent import BasePresalesAgent
from ..llm_integration import OpenRouterLLMClient
from ..jina_integration import JinaAIClient


@dataclass
class DocumentArtifact:
    """Represents a generated document artifact"""
    document_type: str
    title: str
    content: str
    mermaid_diagrams: List[str]
    metadata: Dict[str, Any]
    created_at: datetime


class ProDyAgent(BasePresalesAgent):
    """Product Manager and Documentation Specialist Agent"""
    
    def __init__(self, llm_client: OpenRouterLLMClient, jina_client: JinaAIClient):
        super().__init__(
            name="ProDy",
            role="Product Manager & Documentation Specialist",
            llm_client=llm_client,
            jina_client=jina_client
        )
        
        # Document generation capabilities
        self.document_types = [
            "problem_overview",
            "process_overview", 
            "process_visualization",
            "investment_proposal",
            "next_steps"
        ]
        
        # Mermaid diagram templates
        self.diagram_templates = {
            "process_flow": """
graph TD
    A[{start}] --> B{{decision}}
    B -->|Yes| C[{action1}]
    B -->|No| D[{action2}]
    C --> E[{end}]
    D --> E
""",
            "timeline": """
gantt
    title {title}
    dateFormat  YYYY-MM-DD
    section {phase1}
    {task1}    :{status1}, {id1}, {start1}, {duration1}
    {task2}    :{status2}, {id2}, {start2}, {duration2}
    section {phase2}
    {task3}    :{status3}, {id3}, {start3}, {duration3}
""",
            "architecture": """
graph LR
    subgraph "Current State"
        CS[{current_systems}]
    end
    subgraph "Proposed Solution"
        PS[{proposed_solution}]
    end
    CS -->|{integration_type}| PS
"""
        }

    def get_system_prompt(self) -> str:
        """Get the system prompt for ProDy agent"""
        return """You are ProDy, an expert product manager and technical documentation specialist.

Your role is to create comprehensive project documentation and deliverables:
- Generate detailed problem analysis documents
- Create process flow diagrams and visualizations
- Develop investment proposals with roadmaps and timelines
- Produce technical specifications and requirements
- Ensure all documentation follows professional standards

You are meticulous about structure, clarity, and actionability in all documentation.

When generating documents, always include:
1. Clear executive summaries
2. Quantified business impacts
3. Structured section organization
4. Relevant Mermaid diagrams
5. Actionable next steps

Focus on professional, comprehensive documentation that stakeholders can use for decision-making."""

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None, 
                     stream: bool = False) -> Dict[str, Any]:
        """
        Process input to generate comprehensive documentation artifacts
        
        Expected input: Project brief from Conny agent or business requirements
        Expected output: 5 document artifacts (problem, process, visualization, investment, next_steps)
        """
        try:
            # Parse context for specific document generation requirements
            generation_context = context or {}
            customer_name = generation_context.get("customer_name", "Customer")
            project_scope = generation_context.get("project_scope", "Digital Transformation")
            timeline = generation_context.get("timeline", "6 months")
            
            # Generate all 5 document artifacts
            artifacts = []
            
            # 1. Problem Overview Document
            problem_doc = await self._generate_problem_overview(
                input_data, customer_name, project_scope
            )
            artifacts.append(problem_doc)
            
            # 2. Process Overview Document
            process_doc = await self._generate_process_overview(
                input_data, project_scope, timeline
            )
            artifacts.append(process_doc)
            
            # 3. Process Visualization Document
            visualization_doc = await self._generate_process_visualization(
                input_data, project_scope
            )
            artifacts.append(visualization_doc)
            
            # 4. Investment Proposal Document  
            investment_doc = await self._generate_investment_proposal(
                input_data, customer_name, project_scope, timeline
            )
            artifacts.append(investment_doc)
            
            # 5. Next Steps Document
            next_steps_doc = await self._generate_next_steps(
                input_data, customer_name, timeline
            )
            artifacts.append(next_steps_doc)
            
            return {
                "agent": self.name,
                "status": "success",
                "artifacts": [asdict(artifact) for artifact in artifacts],
                "summary": f"Generated {len(artifacts)} comprehensive documentation artifacts",
                "metadata": {
                    "customer_name": customer_name,
                    "project_scope": project_scope,
                    "timeline": timeline,
                    "total_documents": len(artifacts)
                }
            }
            
        except Exception as e:
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "artifacts": []
            }

    async def _generate_problem_overview(self, input_data: str, customer_name: str, 
                                       project_scope: str) -> DocumentArtifact:
        """Generate problem overview document"""
        prompt = f"""Based on the following project information, generate a comprehensive Problem Overview document.

Project Information:
{input_data}

Customer: {customer_name}
Project Scope: {project_scope}

Generate a detailed problem overview document with these sections:
1. Executive Summary
2. Current State Assessment  
3. Key Challenges and Pain Points
4. Business Impact Analysis
5. Success Criteria Definition

Focus on quantified impacts, specific challenges, and measurable outcomes."""

        content = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return DocumentArtifact(
            document_type="problem_overview",
            title=f"{customer_name} - Problem Overview",
            content=content,
            mermaid_diagrams=[],
            metadata={"customer": customer_name, "scope": project_scope},
            created_at=datetime.now()
        )

    async def _generate_process_overview(self, input_data: str, project_scope: str,
                                       timeline: str) -> DocumentArtifact:
        """Generate process overview document"""
        prompt = f"""Based on the following project information, generate a comprehensive Process Overview document.

Project Information:
{input_data}

Project Scope: {project_scope}
Timeline: {timeline}

Generate a detailed process overview document with these sections:
1. Approach Overview
2. Implementation Phases  
3. Key Activities and Deliverables
4. Resource Requirements
5. Timeline and Milestones

Focus on actionable phases, clear deliverables, and realistic timelines."""

        content = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return DocumentArtifact(
            document_type="process_overview",
            title=f"{project_scope} - Process Overview",
            content=content,
            mermaid_diagrams=[],
            metadata={"scope": project_scope, "timeline": timeline},
            created_at=datetime.now()
        )

    async def _generate_process_visualization(self, input_data: str, 
                                            project_scope: str) -> DocumentArtifact:
        """Generate process visualization document with Mermaid diagrams"""
        prompt = f"""Based on the following project information, generate a Process Visualization document with Mermaid diagrams.

Project Information:
{input_data}

Project Scope: {project_scope}

Generate:
1. Process flow diagram showing key phases and decision points
2. Timeline/Gantt chart showing project phases
3. System integration diagram showing current vs proposed state
4. Explanatory text for each diagram

Provide the Mermaid diagram code for each visualization."""

        content = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        # Extract Mermaid diagrams from content (simplified - in real implementation would parse more carefully)
        diagrams = []
        if "```mermaid" in content:
            # Simple extraction - would be more sophisticated in production
            diagrams = ["process_flow", "timeline", "architecture"]
        
        return DocumentArtifact(
            document_type="process_visualization",
            title=f"{project_scope} - Process Visualization", 
            content=content,
            mermaid_diagrams=diagrams,
            metadata={"scope": project_scope, "diagram_count": len(diagrams)},
            created_at=datetime.now()
        )

    async def _generate_investment_proposal(self, input_data: str, customer_name: str,
                                          project_scope: str, timeline: str) -> DocumentArtifact:
        """Generate investment proposal document"""
        prompt = f"""Based on the following project information, generate a comprehensive Investment Proposal document.

Project Information:
{input_data}

Customer: {customer_name}
Project Scope: {project_scope}
Timeline: {timeline}

Generate a detailed investment proposal with these sections:
1. Investment Summary
2. Cost-Benefit Analysis
3. ROI Projections
4. Risk Assessment and Mitigation
5. Recommended Next Steps

Focus on quantified benefits, realistic costs, and clear ROI calculations."""

        content = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return DocumentArtifact(
            document_type="investment_proposal",
            title=f"{customer_name} - Investment Proposal",
            content=content,
            mermaid_diagrams=[],
            metadata={"customer": customer_name, "scope": project_scope, "timeline": timeline},
            created_at=datetime.now()
        )

    async def _generate_next_steps(self, input_data: str, customer_name: str,
                                 timeline: str) -> DocumentArtifact:
        """Generate next steps document"""
        prompt = f"""Based on the following project information, generate a comprehensive Next Steps document.

Project Information:
{input_data}

Customer: {customer_name}
Timeline: {timeline}

Generate a detailed next steps document with these sections:
1. Immediate Actions Required
2. Decision Points and Timelines
3. Resource Allocation Needs
4. Success Metrics and KPIs
5. Follow-up Schedule

Focus on actionable items, clear deadlines, and measurable success criteria."""

        content = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return DocumentArtifact(
            document_type="next_steps",
            title=f"{customer_name} - Next Steps",
            content=content,
            mermaid_diagrams=[],
            metadata={"customer": customer_name, "timeline": timeline},
            created_at=datetime.now()
        )

    def create_mermaid_diagram(self, diagram_type: str, variables: Dict[str, str]) -> str:
        """Create a Mermaid diagram from template and variables"""
        if diagram_type not in self.diagram_templates:
            raise ValueError(f"Unknown diagram type: {diagram_type}")
        
        template = self.diagram_templates[diagram_type]
        
        # Simple variable substitution
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", value)
        
        return template

    def get_capabilities(self) -> List[str]:
        """Return list of ProDy's capabilities"""
        return [
            "problem_analysis_documentation",
            "process_flow_documentation", 
            "process_visualization_diagrams",
            "investment_proposal_generation",
            "next_steps_planning",
            "mermaid_diagram_creation",
            "technical_specification_writing",
            "business_impact_quantification"
        ]