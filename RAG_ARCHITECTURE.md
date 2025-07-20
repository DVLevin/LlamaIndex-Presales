# RAG System Architecture - Company Knowledge Base

## 🎯 **Purpose & Business Value**
Enable all agents to access company-wide knowledge of past proposals, successful projects, solutions, technologies, and best practices to:
- **Reduce Proposal Cycle-Time**: Reuse proven solutions and components
- **Improve Proposal Quality**: Leverage successful patterns and lessons learned
- **Ensure Consistency**: Apply company standards and methodologies
- **Maximize Win Rate**: Reference similar successful projects and case studies

---

## 📚 **Knowledge Base Content Strategy**

### Document Types & Sources
```
company_knowledge/
├── proposals/
│   ├── successful_proposals/          # Won deals and implementations
│   ├── proposal_templates/            # Standardized formats and structures
│   └── competitive_analyses/          # Market positioning and differentiation
├── projects/
│   ├── case_studies/                  # Detailed project outcomes and metrics
│   ├── technical_architectures/       # Proven solution designs
│   └── lessons_learned/               # What worked and what didn't
├── solutions/
│   ├── technology_stacks/             # Recommended tech combinations
│   ├── integration_patterns/          # Common integration approaches
│   └── best_practices/                # Development and deployment standards
├── market_intelligence/
│   ├── industry_insights/             # Sector-specific knowledge
│   ├── customer_profiles/             # Company and stakeholder information
│   └── pricing_models/                # Cost structures and ROI data
└── company_assets/
    ├── capabilities/                  # What we can deliver
    ├── team_expertise/                # Skills and experience areas
    └── partnerships/                  # Technology and vendor relationships
```

### Content Categorization & Tagging
```json
{
  "document_metadata": {
    "document_id": "uuid",
    "title": "Enterprise Data Platform - FinCorp Implementation",
    "document_type": "case_study",
    "tags": {
      "industry": ["financial_services", "banking"],
      "solution_category": ["data_platform", "real_time_processing"],
      "technologies": ["kubernetes", "kafka", "postgresql", "redis"],
      "project_size": "large",
      "timeline": "6_months",
      "budget_range": "500k_1m",
      "success_metrics": ["performance_improvement", "cost_reduction"],
      "stakeholders": ["cto", "engineering_team", "data_team"]
    },
    "success_indicators": {
      "project_success": true,
      "customer_satisfaction": 9.2,
      "roi_achieved": "180%",
      "timeline_met": true
    },
    "reusable_components": [
      "authentication_service",
      "data_ingestion_pipeline", 
      "monitoring_dashboard"
    ]
  }
}
```

---

## 🏗️ **Technical Architecture**

### Core Components
```python
# RAG system implementation
from llama_index.core import VectorStoreIndex, Document, ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.rerank.jina import JinaRerank
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openrouter import OpenRouter

class CompanyKnowledgeRAG:
    def __init__(self):
        # Embedding model for semantic search
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-large-en-v1.5",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        
        # Reranker for improved retrieval quality
        self.reranker = JinaRerank(
            model="jina-reranker-v1-base-en",
            top_n=5
        )
        
        # Vector store for persistent storage
        self.vector_store = ChromaVectorStore(
            collection_name="company_knowledge",
            persist_directory="./vector_db"
        )
        
        # Index for retrieval
        self.index = None
        self.retriever = None
```

### Document Ingestion Pipeline
```python
class DocumentIngestionPipeline:
    def __init__(self, knowledge_rag: CompanyKnowledgeRAG):
        self.knowledge_rag = knowledge_rag
        self.parsers = {
            '.md': MarkdownParser(),
            '.pdf': PDFParser(),
            '.docx': DocxParser(),
            '.pptx': PowerPointParser()
        }
    
    def ingest_folder(self, folder_path: str):
        """Process all documents in a folder with metadata extraction"""
        documents = []
        
        for file_path in self._scan_files(folder_path):
            # Parse document content
            content = self._parse_document(file_path)
            
            # Extract metadata from file structure and content
            metadata = self._extract_metadata(file_path, content)
            
            # Create document with enriched metadata
            doc = Document(
                text=content,
                metadata=metadata,
                doc_id=str(uuid.uuid4())
            )
            documents.append(doc)
        
        # Create/update vector index
        if self.knowledge_rag.index is None:
            self.knowledge_rag.index = VectorStoreIndex.from_documents(
                documents,
                embed_model=self.knowledge_rag.embed_model,
                vector_store=self.knowledge_rag.vector_store
            )
        else:
            # Add new documents to existing index
            for doc in documents:
                self.knowledge_rag.index.insert(doc)
    
    def _extract_metadata(self, file_path: str, content: str) -> Dict:
        """Extract rich metadata for improved search"""
        # File path analysis
        path_parts = Path(file_path).parts
        category = path_parts[-2] if len(path_parts) > 1 else "uncategorized"
        
        # Content analysis for automatic tagging
        tags = self._extract_tags_from_content(content)
        
        # Technology detection
        technologies = self._detect_technologies(content)
        
        return {
            "file_path": file_path,
            "category": category,
            "tags": tags,
            "technologies": technologies,
            "ingestion_date": datetime.utcnow().isoformat(),
            "content_length": len(content),
            "language": "english"  # Could be detected
        }
```

### Smart Retrieval System
```python
class SmartRetriever:
    def __init__(self, knowledge_rag: CompanyKnowledgeRAG):
        self.knowledge_rag = knowledge_rag
        self.retriever = knowledge_rag.index.as_retriever(
            similarity_top_k=15,  # Initial broad search
            response_mode="tree_summarize"
        )
    
    def search_similar_projects(
        self, 
        query: str, 
        filters: Dict = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Search for relevant past projects and solutions"""
        
        # Enhanced query with context
        enhanced_query = self._enhance_query(query, filters)
        
        # Initial retrieval
        initial_results = self.retriever.retrieve(enhanced_query)
        
        # Apply metadata filters
        filtered_results = self._apply_filters(initial_results, filters)
        
        # Rerank for relevance
        reranked_results = self.knowledge_rag.reranker.postprocess_nodes(
            filtered_results,
            query_str=query
        )
        
        # Format for agent consumption
        formatted_results = []
        for node in reranked_results[:top_k]:
            formatted_results.append({
                "content": node.text,
                "relevance_score": node.score,
                "metadata": node.metadata,
                "reusable_components": node.metadata.get("reusable_components", []),
                "success_metrics": node.metadata.get("success_metrics", {}),
                "similar_context": self._extract_similar_context(node)
            })
        
        return formatted_results
    
    def _enhance_query(self, query: str, filters: Dict = None) -> str:
        """Enhance search query with contextual information"""
        enhanced = query
        
        if filters:
            if "industry" in filters:
                enhanced += f" industry:{filters['industry']}"
            if "technologies" in filters:
                enhanced += f" technologies:{' '.join(filters['technologies'])}"
            if "budget_range" in filters:
                enhanced += f" budget:{filters['budget_range']}"
        
        return enhanced
    
    def find_reusable_components(self, requirements: List[str]) -> List[Dict]:
        """Find specific components that can be reused"""
        components = []
        
        for req in requirements:
            results = self.search_similar_projects(
                query=f"reusable component {req}",
                filters={"document_type": "case_study"},
                top_k=3
            )
            
            for result in results:
                if "reusable_components" in result["metadata"]:
                    components.extend(result["metadata"]["reusable_components"])
        
        # Deduplicate and rank by frequency
        component_counts = Counter(components)
        return [
            {
                "component_name": comp,
                "usage_frequency": count,
                "confidence": count / len(requirements)
            }
            for comp, count in component_counts.most_common(10)
        ]
```

### Agent Integration Tools
```python
class RAGToolsForAgents:
    def __init__(self, smart_retriever: SmartRetriever):
        self.retriever = smart_retriever
    
    # Tool for Conny (Consultant Agent)
    def get_similar_solutions_tool(self):
        """Tool for finding similar past solutions"""
        def find_similar_solutions(
            requirements: str,
            industry: str = None,
            budget_range: str = None
        ) -> List[Dict]:
            filters = {}
            if industry:
                filters["industry"] = industry
            if budget_range:
                filters["budget_range"] = budget_range
            
            return self.retriever.search_similar_projects(
                query=f"solution for {requirements}",
                filters=filters,
                top_k=5
            )
        
        return FunctionTool.from_defaults(
            fn=find_similar_solutions,
            name="find_similar_solutions",
            description="Search company knowledge base for similar past solutions and projects"
        )
    
    # Tool for ProDy (Product Manager Agent)  
    def get_best_practices_tool(self):
        """Tool for finding implementation best practices"""
        def find_best_practices(technology_stack: str, project_type: str) -> List[str]:
            results = self.retriever.search_similar_projects(
                query=f"best practices {technology_stack} {project_type}",
                filters={"category": "best_practices"},
                top_k=3
            )
            
            practices = []
            for result in results:
                # Extract best practices from content
                practices.extend(self._extract_practices(result["content"]))
            
            return practices
        
        return FunctionTool.from_defaults(
            fn=find_best_practices,
            name="find_best_practices", 
            description="Get implementation best practices for specific technologies and project types"
        )
    
    # Tool for all agents
    def get_success_metrics_tool(self):
        """Tool for finding relevant success metrics"""
        def find_success_metrics(project_type: str, industry: str = None) -> Dict:
            filters = {"document_type": "case_study"}
            if industry:
                filters["industry"] = industry
            
            results = self.retriever.search_similar_projects(
                query=f"success metrics {project_type}",
                filters=filters,
                top_k=5
            )
            
            # Aggregate metrics from successful projects
            metrics = {
                "performance_improvements": [],
                "cost_savings": [],
                "roi_percentages": [],
                "timeline_adherence": []
            }
            
            for result in results:
                if result["metadata"].get("success_indicators", {}).get("project_success"):
                    # Extract and aggregate metrics
                    metrics = self._aggregate_metrics(metrics, result["metadata"])
            
            return {
                "average_performance_improvement": np.mean(metrics["performance_improvements"]),
                "typical_cost_savings": np.mean(metrics["cost_savings"]), 
                "expected_roi_range": f"{min(metrics['roi_percentages'])}-{max(metrics['roi_percentages'])}%",
                "success_rate": len([m for m in metrics["timeline_adherence"] if m]) / len(metrics["timeline_adherence"])
            }
        
        return FunctionTool.from_defaults(
            fn=find_success_metrics,
            name="find_success_metrics",
            description="Get typical success metrics and outcomes for similar projects"
        )
```

---

## 🔍 **Advanced RAG Features**

### Hybrid Search Strategy
```python
class HybridSearchEngine:
    def __init__(self, knowledge_rag: CompanyKnowledgeRAG):
        self.knowledge_rag = knowledge_rag
        self.keyword_search = BM25Retriever()  # For exact term matching
        self.semantic_search = knowledge_rag.retriever  # For semantic similarity
    
    def hybrid_retrieve(self, query: str, alpha: float = 0.7) -> List[Document]:
        """Combine semantic and keyword search results"""
        # Semantic search results
        semantic_results = self.semantic_search.retrieve(query)
        
        # Keyword search results  
        keyword_results = self.keyword_search.retrieve(query)
        
        # Weighted combination
        combined_scores = {}
        
        for result in semantic_results:
            combined_scores[result.doc_id] = alpha * result.score
        
        for result in keyword_results:
            if result.doc_id in combined_scores:
                combined_scores[result.doc_id] += (1 - alpha) * result.score
            else:
                combined_scores[result.doc_id] = (1 - alpha) * result.score
        
        # Sort by combined score and return top results
        ranked_results = sorted(
            combined_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [self._get_document_by_id(doc_id) for doc_id, _ in ranked_results[:10]]
```

### Graph RAG Enhancement (Optional)
```python
class GraphEnhancedRAG:
    """Optional graph database integration for complex relationship queries"""
    
    def __init__(self, neo4j_uri: str, username: str, password: str):
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(username, password))
    
    def create_project_relationships(self):
        """Build knowledge graph of project relationships"""
        with self.driver.session() as session:
            # Create nodes for projects, technologies, industries
            session.run("""
                MATCH (p:Project), (t:Technology), (i:Industry)
                WHERE p.technologies CONTAINS t.name AND p.industry = i.name
                CREATE (p)-[:USES_TECHNOLOGY]->(t)
                CREATE (p)-[:IN_INDUSTRY]->(i)
            """)
    
    def graph_enhanced_search(self, query_params: Dict) -> List[Dict]:
        """Use graph relationships to find relevant projects"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Project)-[:USES_TECHNOLOGY]->(t:Technology)
                WHERE t.name IN $technologies
                MATCH (p)-[:IN_INDUSTRY]->(i:Industry)
                WHERE i.name = $industry
                RETURN p, collect(t.name) as technologies, i.name as industry
                ORDER BY p.success_score DESC
                LIMIT 10
            """, query_params)
            
            return [record.data() for record in result]
```

---

## 📊 **Performance & Monitoring**

### RAG Quality Metrics
```python
class RAGMonitoring:
    def __init__(self):
        self.metrics = {
            "retrieval_latency": [],
            "relevance_scores": [],
            "usage_patterns": {},
            "success_rates": {}
        }
    
    def track_retrieval_quality(self, query: str, results: List[Dict], user_feedback: float):
        """Monitor retrieval quality and user satisfaction"""
        self.metrics["relevance_scores"].append({
            "query": query,
            "avg_score": np.mean([r["relevance_score"] for r in results]),
            "user_feedback": user_feedback,
            "timestamp": datetime.utcnow()
        })
    
    def analyze_usage_patterns(self) -> Dict:
        """Analyze which knowledge is most valuable"""
        return {
            "most_queried_topics": Counter(self.metrics["usage_patterns"]).most_common(10),
            "avg_retrieval_latency": np.mean(self.metrics["retrieval_latency"]),
            "user_satisfaction": np.mean([m["user_feedback"] for m in self.metrics["relevance_scores"]])
        }
```

### Continuous Learning
```python
class ContinuousLearning:
    """Learn from successful proposals to improve future recommendations"""
    
    def update_knowledge_base(self, new_project: Dict):
        """Add successful projects back to knowledge base"""
        if new_project["success_indicators"]["project_success"]:
            # Extract learnings and update embeddings
            self._extract_success_patterns(new_project)
            self._update_component_rankings(new_project)
            self._refine_search_algorithms(new_project)
    
    def _extract_success_patterns(self, project: Dict):
        """Identify what made this project successful"""
        # Analyze successful patterns for future recommendations
        pass
```

---

## 🚀 **Implementation Roadmap**

### Phase 1: Core RAG (Week 1-2)
- Basic document ingestion pipeline
- Vector embedding and storage
- Simple semantic search
- Integration with agent tools

### Phase 2: Enhanced Retrieval (Week 3-4)  
- Metadata filtering and tagging
- Jina reranker integration
- Hybrid search capabilities
- Performance optimization

### Phase 3: Advanced Features (Week 5-6)
- Graph RAG integration (optional)
- Continuous learning mechanisms  
- Advanced analytics and monitoring
- Quality feedback loops

### Success Metrics
- **Retrieval Latency**: < 500ms average
- **Relevance Score**: > 0.8 average user rating
- **Knowledge Reuse**: 70%+ proposals reference past projects
- **Agent Performance**: Measurable improvement in proposal quality with RAG vs without

This RAG architecture provides the intelligent foundation that enables all agents to leverage company knowledge, significantly improving proposal quality and consistency while reducing cycle time.