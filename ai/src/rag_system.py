"""
RAG System for Past Proposal Context
Finds and integrates similar past proposals to provide relevant context
"""
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import asyncio
import structlog

from .jina_integration import JinaAIClient
from .config import get_ai_settings

logger = structlog.get_logger()
settings = get_ai_settings()


class ProposalRAGSystem:
    """
    RAG system for finding and integrating similar past proposals
    
    Provides context from organizational knowledge to improve proposal quality
    and reuse successful patterns from previous engagements.
    """
    
    def __init__(self, jina_client: Optional[JinaAIClient] = None):
        self.jina_client = jina_client or JinaAIClient()
        
        # Proposal database paths
        self.knowledge_base_path = "./knowledge_base/past_proposals"
        self.embeddings_cache_path = "./knowledge_base/embeddings_cache.json"
        self.proposal_index_path = "./knowledge_base/proposal_index.json"
        
        # Initialize knowledge base structure
        self._ensure_knowledge_base_structure()
        
        # Load or create proposal index
        self.proposal_index = self._load_proposal_index()
        
        logger.info("ProposalRAG system initialized", 
                   knowledge_base_path=self.knowledge_base_path,
                   indexed_proposals=len(self.proposal_index))
    
    async def find_similar_proposals(self, 
                                   search_terms: List[str], 
                                   industry: str = None,
                                   solution_types: List[str] = None,
                                   company_size: str = None,
                                   top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find similar past proposals based on search criteria
        
        Args:
            search_terms: Key business terms for similarity search
            industry: Target industry filter
            solution_types: Solution type filters
            company_size: Company size filter
            top_k: Number of similar proposals to return
            
        Returns:
            List of similar proposal summaries with relevance scores
        """
        try:
            logger.info("Searching for similar proposals",
                       search_terms=search_terms,
                       industry=industry,
                       solution_types=solution_types)
            
            # Create search query from terms
            search_query = " ".join(search_terms)
            
            # Get semantic matches using embeddings
            semantic_matches = await self._get_semantic_matches(search_query, top_k * 2)
            
            # Apply business filters
            filtered_matches = self._apply_business_filters(
                semantic_matches, 
                industry=industry,
                solution_types=solution_types,
                company_size=company_size
            )
            
            # Rank and return top matches
            ranked_matches = self._rank_matches(filtered_matches, search_terms)
            
            logger.info("Similar proposals found",
                       total_matches=len(ranked_matches),
                       top_match_score=ranked_matches[0].get("relevance_score", 0) if ranked_matches else 0)
            
            return ranked_matches[:top_k]
            
        except Exception as e:
            logger.error("Failed to find similar proposals", error=str(e))
            return self._get_fallback_proposals(search_terms, industry, solution_types)
    
    async def get_proposal_context(self, 
                                 routing_info: Dict[str, Any],
                                 max_context_length: int = 2000) -> Dict[str, Any]:
        """
        Get comprehensive proposal context based on routing analysis
        
        Args:
            routing_info: Output from InputRouterAgent
            max_context_length: Maximum context length to return
            
        Returns:
            Structured context information for agents
        """
        try:
            # Extract search criteria from routing info
            search_terms = routing_info.get("rag_search_terms", [])
            industry = routing_info.get("industry", "unknown")
            solution_types = routing_info.get("solution_types", [])
            company_size = routing_info.get("company_size", "unknown")
            
            # Find similar proposals
            similar_proposals = await self.find_similar_proposals(
                search_terms=search_terms,
                industry=industry,
                solution_types=solution_types,
                company_size=company_size,
                top_k=5
            )
            
            # Extract relevant context patterns
            context_patterns = self._extract_context_patterns(similar_proposals)
            
            # Create structured context
            proposal_context = {
                "timestamp": datetime.now().isoformat(),
                "search_criteria": {
                    "search_terms": search_terms,
                    "industry": industry,
                    "solution_types": solution_types,
                    "company_size": company_size
                },
                "similar_proposals": similar_proposals,
                "context_patterns": context_patterns,
                "reusable_content": self._extract_reusable_content(similar_proposals),
                "lessons_learned": self._extract_lessons_learned(similar_proposals),
                "competitive_insights": self._extract_competitive_insights(similar_proposals),
                "pricing_benchmarks": self._extract_pricing_benchmarks(similar_proposals),
                "implementation_patterns": self._extract_implementation_patterns(similar_proposals),
                "success_factors": self._extract_success_factors(similar_proposals)
            }
            
            # Trim context to fit length constraints
            trimmed_context = self._trim_context_to_length(proposal_context, max_context_length)
            
            logger.info("Proposal context generated",
                       similar_proposals_count=len(similar_proposals),
                       context_patterns_count=len(context_patterns),
                       final_context_length=len(str(trimmed_context)))
            
            return trimmed_context
            
        except Exception as e:
            logger.error("Failed to get proposal context", error=str(e))
            return self._get_fallback_context(routing_info)
    
    def add_proposal_to_knowledge_base(self, 
                                     proposal_data: Dict[str, Any],
                                     customer_name: str,
                                     industry: str = "unknown",
                                     solution_types: List[str] = None,
                                     outcome: str = "unknown") -> str:
        """
        Add a new proposal to the knowledge base for future RAG searches
        
        Args:
            proposal_data: Complete proposal data from pipeline
            customer_name: Customer name for identification
            industry: Industry classification
            solution_types: Types of solutions proposed
            outcome: Proposal outcome (won, lost, pending)
            
        Returns:
            Unique identifier for the stored proposal
        """
        try:
            # Create unique identifier
            proposal_id = f"{customer_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Structure proposal for storage
            stored_proposal = {
                "id": proposal_id,
                "timestamp": datetime.now().isoformat(),
                "customer_name": customer_name,
                "industry": industry,
                "solution_types": solution_types or [],
                "outcome": outcome,
                "metadata": {
                    "content_length": len(str(proposal_data)),
                    "document_count": len(proposal_data.get("document_artifacts", [])),
                    "agents_involved": list(proposal_data.keys())
                },
                "proposal_data": proposal_data
            }
            
            # Save to file system
            proposal_file_path = os.path.join(self.knowledge_base_path, f"{proposal_id}.json")
            with open(proposal_file_path, 'w') as f:
                json.dump(stored_proposal, f, indent=2)
            
            # Update proposal index
            self.proposal_index[proposal_id] = {
                "file_path": proposal_file_path,
                "customer_name": customer_name,
                "industry": industry,
                "solution_types": solution_types,
                "timestamp": stored_proposal["timestamp"],
                "outcome": outcome
            }
            
            # Save updated index
            self._save_proposal_index()
            
            logger.info("Proposal added to knowledge base",
                       proposal_id=proposal_id,
                       customer_name=customer_name,
                       industry=industry)
            
            return proposal_id
            
        except Exception as e:
            logger.error("Failed to add proposal to knowledge base", 
                        customer_name=customer_name,
                        error=str(e))
            return ""
    
    async def _get_semantic_matches(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Get semantic matches using Jina embeddings"""
        
        try:
            # For now, return mock semantic matches
            # In production, this would use actual vector embeddings
            mock_matches = [
                {
                    "proposal_id": "acme_corp_digital_transform_20240115",
                    "customer_name": "Acme Corp",
                    "industry": "manufacturing",
                    "solution_types": ["automation", "analytics"],
                    "semantic_score": 0.85,
                    "summary": "Digital transformation initiative for manufacturing optimization",
                    "outcome": "won"
                },
                {
                    "proposal_id": "techstart_ai_implementation_20240203", 
                    "customer_name": "TechStart Inc",
                    "industry": "technology",
                    "solution_types": ["automation", "integration"],
                    "semantic_score": 0.78,
                    "summary": "AI implementation for workflow automation",
                    "outcome": "won"
                },
                {
                    "proposal_id": "retail_analytics_platform_20240220",
                    "customer_name": "Retail Chain Co",
                    "industry": "retail", 
                    "solution_types": ["analytics", "optimization"],
                    "semantic_score": 0.72,
                    "summary": "Customer analytics and optimization platform",
                    "outcome": "lost"
                }
            ]
            
            return mock_matches[:top_k]
            
        except Exception as e:
            logger.error("Semantic matching failed", error=str(e))
            return []
    
    def _apply_business_filters(self, 
                              matches: List[Dict[str, Any]], 
                              industry: str = None,
                              solution_types: List[str] = None,
                              company_size: str = None) -> List[Dict[str, Any]]:
        """Apply business filters to semantic matches"""
        
        filtered_matches = []
        
        for match in matches:
            # Industry filter
            if industry and industry != "unknown":
                if match.get("industry") != industry:
                    continue
            
            # Solution type filter
            if solution_types:
                match_solutions = match.get("solution_types", [])
                if not any(solution in match_solutions for solution in solution_types):
                    continue
            
            # Company size filter (would need to be in proposal data)
            # For now, accept all matches
            
            filtered_matches.append(match)
        
        return filtered_matches
    
    def _rank_matches(self, matches: List[Dict[str, Any]], search_terms: List[str]) -> List[Dict[str, Any]]:
        """Rank matches by relevance"""
        
        for match in matches:
            # Calculate composite relevance score
            semantic_score = match.get("semantic_score", 0.0)
            
            # Boost for successful outcomes
            outcome_boost = 0.1 if match.get("outcome") == "won" else 0.0
            
            # Boost for search term matches in summary
            summary = match.get("summary", "").lower()
            term_boost = sum(0.05 for term in search_terms if term.lower() in summary)
            
            match["relevance_score"] = semantic_score + outcome_boost + term_boost
        
        return sorted(matches, key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    def _extract_context_patterns(self, proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract common patterns from similar proposals"""
        
        patterns = []
        
        # Common solution approaches
        solution_approaches = {}
        for proposal in proposals:
            for solution_type in proposal.get("solution_types", []):
                if solution_type not in solution_approaches:
                    solution_approaches[solution_type] = []
                solution_approaches[solution_type].append(proposal.get("summary", ""))
        
        patterns.append({
            "type": "solution_approaches",
            "data": solution_approaches
        })
        
        # Success factors from won deals
        won_deals = [p for p in proposals if p.get("outcome") == "won"]
        if won_deals:
            patterns.append({
                "type": "success_factors",
                "data": {
                    "count": len(won_deals),
                    "common_solutions": list(set(
                        solution for proposal in won_deals 
                        for solution in proposal.get("solution_types", [])
                    ))
                }
            })
        
        return patterns
    
    def _extract_reusable_content(self, proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract reusable content from similar proposals"""
        
        reusable_content = []
        
        for proposal in proposals:
            if proposal.get("outcome") == "won":
                reusable_content.append({
                    "source": proposal.get("customer_name"),
                    "type": "successful_approach",
                    "content": proposal.get("summary"),
                    "solution_types": proposal.get("solution_types", []),
                    "industry": proposal.get("industry")
                })
        
        return reusable_content
    
    def _get_fallback_proposals(self, search_terms: List[str], industry: str, solution_types: List[str]) -> List[Dict[str, Any]]:
        """Return fallback proposals when search fails"""
        
        return [
            {
                "proposal_id": "fallback_general_business",
                "customer_name": "General Business Solution",
                "industry": industry or "general",
                "solution_types": solution_types or ["consulting"],
                "relevance_score": 0.5,
                "summary": "General business consulting and solution development approach",
                "outcome": "template"
            }
        ]
    
    def _get_fallback_context(self, routing_info: Dict[str, Any]) -> Dict[str, Any]:
        """Return fallback context when RAG fails"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "fallback_mode": True,
            "search_criteria": {
                "search_terms": routing_info.get("rag_search_terms", []),
                "industry": routing_info.get("industry", "unknown")
            },
            "similar_proposals": [],
            "context_patterns": [],
            "reusable_content": [],
            "general_guidance": [
                "Focus on customer's stated pain points and requirements",
                "Emphasize business value and ROI in proposals", 
                "Include clear implementation timeline and milestones",
                "Address potential risks and mitigation strategies"
            ]
        }
    
    def _ensure_knowledge_base_structure(self):
        """Ensure knowledge base directory structure exists"""
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        os.makedirs(os.path.dirname(self.embeddings_cache_path), exist_ok=True)
    
    def _load_proposal_index(self) -> Dict[str, Any]:
        """Load proposal index from file"""
        try:
            if os.path.exists(self.proposal_index_path):
                with open(self.proposal_index_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning("Failed to load proposal index", error=str(e))
        
        return {}
    
    def _save_proposal_index(self):
        """Save proposal index to file"""
        try:
            with open(self.proposal_index_path, 'w') as f:
                json.dump(self.proposal_index, f, indent=2)
        except Exception as e:
            logger.error("Failed to save proposal index", error=str(e))
    
    # Additional helper methods (placeholders for full implementation)
    def _extract_lessons_learned(self, proposals: List[Dict[str, Any]]) -> List[str]:
        return ["Focus on business outcomes", "Include clear timelines", "Address integration concerns"]
    
    def _extract_competitive_insights(self, proposals: List[Dict[str, Any]]) -> List[str]:
        return ["Emphasize unique value proposition", "Address common competitor weaknesses"]
    
    def _extract_pricing_benchmarks(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"typical_range": "$50K-$500K", "factors": ["complexity", "timeline", "integrations"]}
    
    def _extract_implementation_patterns(self, proposals: List[Dict[str, Any]]) -> List[str]:
        return ["3-phase approach", "Pilot then scale", "Change management focus"]
    
    def _extract_success_factors(self, proposals: List[Dict[str, Any]]) -> List[str]:
        return ["Executive sponsorship", "Clear requirements", "Realistic timeline"]
    
    def _trim_context_to_length(self, context: Dict[str, Any], max_length: int) -> Dict[str, Any]:
        # For now, return full context - implement trimming logic as needed
        return context