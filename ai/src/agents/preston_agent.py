"""
Preston Agent - Process Optimization & Technical Implementation Specialist

Analyzes current processes and designs optimized workflows:
- Maps current state processes and identifies inefficiencies
- Designs future state process flows with automation
- Creates technical implementation specifications
- Develops process improvement recommendations
"""

from typing import Dict, Any, List, Optional, Tuple
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime

from .base_agent import BasePresalesAgent
from ..llm_integration import OpenRouterLLMClient
from ..jina_integration import JinaAIClient


@dataclass
class ProcessStep:
    """Represents a single step in a process"""
    id: str
    name: str
    description: str
    time_estimate: str
    resources_required: List[str]
    automation_potential: str  # High/Medium/Low/None
    pain_points: List[str]


@dataclass
class ProcessAnalysis:
    """Complete process analysis result"""
    current_state: Dict[str, Any]
    future_state: Dict[str, Any]
    improvements: List[Dict[str, Any]]
    technical_requirements: Dict[str, Any]
    implementation_plan: Dict[str, Any]
    success_metrics: List[Dict[str, str]]


class PrestonAgent(BasePresalesAgent):
    """Process Optimization and Technical Implementation Specialist Agent"""
    
    def __init__(self, llm_client: OpenRouterLLMClient, jina_client: JinaAIClient):
        super().__init__(
            name="Preston",
            role="Process Optimization & Technical Implementation Specialist",
            llm_client=llm_client,
            jina_client=jina_client
        )
        
        # Process analysis capabilities
        self.analysis_types = [
            "current_state_mapping",
            "future_state_design",
            "automation_opportunities", 
            "technical_requirements",
            "implementation_planning"
        ]
        
        # Process diagram templates
        self.process_templates = {
            "linear_workflow": """
graph TD
    A[{start}] --> B[{step1}]
    B --> C[{step2}]
    C --> D[{step3}]
    D --> E[{end}]
""",
            "decision_workflow": """
graph TD
    A[{start}] --> B{{decision}}
    B -->|{condition1}| C[{path1}]
    B -->|{condition2}| D[{path2}]
    C --> E[{converge}]
    D --> E
    E --> F[{end}]
""",
            "parallel_workflow": """
graph TD
    A[{start}] --> B[{split}]
    B --> C[{parallel1}]
    B --> D[{parallel2}]
    C --> E[{merge}]
    D --> E
    E --> F[{end}]
""",
            "automation_flow": """
graph TD
    A[{input}] --> B{{Auto-Process?}}
    B -->|Yes| C[Automated Path]
    B -->|No| D[Manual Path]
    C --> E[{output}]
    D --> F[Human Review]
    F --> E
"""
        }

    def get_system_prompt(self) -> str:
        """Get the system prompt for Preston agent"""
        return """You are Preston, a process optimization and technical implementation specialist.

Your role is to analyze current processes and design optimized workflows:
- Map current state processes and identify inefficiencies
- Design future state process flows with automation opportunities
- Create technical implementation specifications
- Develop process improvement recommendations
- Ensure technical feasibility and integration compatibility

You excel at bridging business processes with technical solutions, ensuring practical and efficient implementations.

When analyzing processes, always include:
1. Current state process mapping with pain points
2. Future state design with automation opportunities
3. Technical requirements for implementation
4. Phased implementation plan
5. Quantified improvement metrics

Focus on practical, achievable optimizations that deliver measurable business value."""

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None,
                     stream: bool = False) -> Dict[str, Any]:
        """
        Process input to perform comprehensive process analysis and optimization
        
        Expected input: Business requirements and current process descriptions
        Expected output: Process analysis with current/future state and implementation plan
        """
        try:
            # Parse context for process analysis requirements
            analysis_context = context or {}
            process_scope = analysis_context.get("process_scope", "Business Process")
            optimization_focus = analysis_context.get("focus", "efficiency")
            technical_constraints = analysis_context.get("constraints", [])
            
            # Perform comprehensive process analysis
            analysis = await self._perform_process_analysis(
                input_data, process_scope, optimization_focus, technical_constraints
            )
            
            return {
                "agent": self.name,
                "status": "success", 
                "process_analysis": asdict(analysis),
                "summary": f"Completed process analysis for {process_scope}",
                "metadata": {
                    "process_scope": process_scope,
                    "optimization_focus": optimization_focus,
                    "improvement_count": len(analysis.improvements),
                    "automation_opportunities": len([imp for imp in analysis.improvements 
                                                   if imp.get("type") == "automation"])
                }
            }
            
        except Exception as e:
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "process_analysis": None
            }

    async def _perform_process_analysis(self, input_data: str, process_scope: str,
                                      optimization_focus: str, 
                                      constraints: List[str]) -> ProcessAnalysis:
        """Perform comprehensive process analysis"""
        
        # Analyze current state
        current_state = await self._analyze_current_state(input_data, process_scope)
        
        # Design future state
        future_state = await self._design_future_state(
            input_data, current_state, optimization_focus
        )
        
        # Identify improvements
        improvements = await self._identify_improvements(
            current_state, future_state, optimization_focus
        )
        
        # Define technical requirements
        technical_requirements = await self._define_technical_requirements(
            future_state, improvements, constraints
        )
        
        # Create implementation plan
        implementation_plan = await self._create_implementation_plan(
            improvements, technical_requirements
        )
        
        # Define success metrics
        success_metrics = await self._define_success_metrics(
            improvements, optimization_focus
        )
        
        return ProcessAnalysis(
            current_state=current_state,
            future_state=future_state,
            improvements=improvements,
            technical_requirements=technical_requirements,
            implementation_plan=implementation_plan,
            success_metrics=success_metrics
        )

    async def _analyze_current_state(self, input_data: str, process_scope: str) -> Dict[str, Any]:
        """Analyze current state processes"""
        prompt = f"""Analyze the current state processes described in the following information:

Input Data:
{input_data}

Process Scope: {process_scope}

Provide a detailed current state analysis including:
1. Process steps and workflow
2. Time estimates for each step
3. Resources required
4. Pain points and inefficiencies
5. Bottlenecks and delays
6. Manual tasks and potential automation opportunities

Create a Mermaid diagram showing the current workflow."""

        response = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return {
            "description": response,
            "process_scope": process_scope,
            "analysis_type": "current_state",
            "timestamp": datetime.now().isoformat()
        }

    async def _design_future_state(self, input_data: str, current_state: Dict[str, Any],
                                 optimization_focus: str) -> Dict[str, Any]:
        """Design optimized future state"""
        prompt = f"""Based on the current state analysis and optimization focus, design an optimized future state process.

Current State Analysis:
{current_state['description']}

Optimization Focus: {optimization_focus}

Design an optimized future state including:
1. Streamlined workflow with eliminated steps
2. Automation opportunities and automated tasks
3. Improved stakeholder collaboration
4. Reduced cycle times and improved efficiency
5. Better resource utilization
6. Integration points and system connections

Create a Mermaid diagram showing the optimized workflow."""

        response = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return {
            "description": response,
            "optimization_focus": optimization_focus,
            "analysis_type": "future_state",
            "timestamp": datetime.now().isoformat()
        }

    async def _identify_improvements(self, current_state: Dict[str, Any], 
                                   future_state: Dict[str, Any],
                                   optimization_focus: str) -> List[Dict[str, Any]]:
        """Identify specific process improvements"""
        prompt = f"""Compare the current and future states to identify specific process improvements.

Current State:
{current_state['description']}

Future State:
{future_state['description']}

Optimization Focus: {optimization_focus}

Identify specific improvements with:
1. Improvement type (automation, elimination, optimization, integration)
2. Description of the change
3. Quantified benefits (time savings, cost reduction, efficiency gains)
4. Implementation complexity (High/Medium/Low)
5. Dependencies and requirements
6. Success criteria

Provide at least 5 specific improvements."""

        response = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        # Parse improvements (simplified - would be more sophisticated in production)
        improvements = []
        for i in range(5):  # Assume 5 improvements for now
            improvements.append({
                "id": f"IMP-{i+1:03d}",
                "type": "optimization",  # Would parse from response
                "description": f"Process improvement {i+1}",
                "benefits": "TBD",  # Would parse from response
                "complexity": "Medium",
                "priority": "High" if i < 2 else "Medium"
            })
        
        return improvements

    async def _define_technical_requirements(self, future_state: Dict[str, Any],
                                           improvements: List[Dict[str, Any]],
                                           constraints: List[str]) -> Dict[str, Any]:
        """Define technical requirements for implementation"""
        prompt = f"""Based on the future state design and process improvements, define technical requirements.

Future State:
{future_state['description']}

Process Improvements:
{[imp['description'] for imp in improvements[:3]]}

Technical Constraints:
{constraints}

Define technical requirements including:
1. System architecture requirements
2. Integration patterns and APIs needed
3. Data flow and storage requirements
4. Performance and scalability specifications
5. Security and compliance considerations
6. Infrastructure and deployment needs
7. Monitoring and observability requirements

Focus on practical, implementable technical specifications."""

        response = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return {
            "description": response,
            "constraints": constraints,
            "analysis_type": "technical_requirements",
            "timestamp": datetime.now().isoformat()
        }

    async def _create_implementation_plan(self, improvements: List[Dict[str, Any]],
                                        technical_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create phased implementation plan"""
        prompt = f"""Create a phased implementation plan for the process improvements and technical requirements.

Process Improvements:
{[f"{imp['id']}: {imp['description']}" for imp in improvements[:5]]}

Technical Requirements:
{technical_requirements['description']}

Create an implementation plan with:
1. Phase breakdown (3-4 phases maximum)
2. Activities and deliverables for each phase
3. Timeline estimates and dependencies
4. Resource requirements and skills needed
5. Risk factors and mitigation strategies
6. Success criteria for each phase
7. Change management considerations

Focus on practical, achievable phases that build value incrementally."""

        response = await self.llm_client.complete([{"role": "user", "content": prompt}])
        
        return {
            "description": response,
            "total_improvements": len(improvements),
            "analysis_type": "implementation_plan",
            "timestamp": datetime.now().isoformat()
        }

    async def _define_success_metrics(self, improvements: List[Dict[str, Any]],
                                    optimization_focus: str) -> List[Dict[str, str]]:
        """Define success metrics for process optimization"""
        metrics = [
            {"metric": "Process Cycle Time", "target": "50% reduction", "measurement": "Time to completion"},
            {"metric": "Manual Effort", "target": "40% reduction", "measurement": "Hours of manual work"},
            {"metric": "Error Rate", "target": "30% reduction", "measurement": "Defects per transaction"},
            {"metric": "Cost per Transaction", "target": "35% reduction", "measurement": "Total cost divided by volume"},
            {"metric": "Customer Satisfaction", "target": "20% improvement", "measurement": "CSAT score"}
        ]
        
        return metrics

    def create_process_diagram(self, diagram_type: str, variables: Dict[str, str]) -> str:
        """Create a process diagram from template and variables"""
        if diagram_type not in self.process_templates:
            raise ValueError(f"Unknown diagram type: {diagram_type}")
        
        template = self.process_templates[diagram_type]
        
        # Simple variable substitution
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", value)
        
        return template

    def get_capabilities(self) -> List[str]:
        """Return list of Preston's capabilities"""
        return [
            "current_state_process_mapping",
            "future_state_process_design",
            "automation_opportunity_identification",
            "technical_requirements_definition",
            "implementation_planning",
            "process_diagram_creation",
            "efficiency_analysis",
            "integration_pattern_design",
            "performance_optimization"
        ]