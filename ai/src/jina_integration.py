"""
Jina AI integration for embeddings, reranking, and document processing
"""
import asyncio
import json
import aiofiles
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import get_ai_settings

logger = structlog.get_logger()
settings = get_ai_settings()


class JinaEmbeddingsClient:
    """Client for Jina AI embeddings service"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.jina_api_key
        self.model = model or settings.default_embedding_model
        self.base_url = "https://api.jina.ai/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
        logger.info(
            "Jina embeddings client initialized",
            model=self.model,
            dimensions=settings.embedding_dimensions
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    async def create_embeddings(
        self, 
        texts: Union[str, List[str]], 
        task: str = "retrieval.passage"
    ) -> Dict[str, Any]:
        """
        Create embeddings for text(s) using Jina AI
        
        Args:
            texts: Single text or list of texts to embed
            task: Task type for embeddings (retrieval.passage, retrieval.query, etc.)
            
        Returns:
            Embeddings response with vectors and metadata
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            payload = {
                "model": self.model,
                "input": texts
            }
            
            logger.debug(
                "Creating embeddings",
                model=self.model,
                text_count=len(texts),
                task=task
            )
            
            response = await self.client.post(
                f"{self.base_url}/embeddings",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            logger.info(
                "Embeddings created successfully",
                model=self.model,
                embeddings_count=len(result.get("data", [])),
                total_tokens=result.get("usage", {}).get("total_tokens", 0)
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Embedding creation failed",
                model=self.model,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    async def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed documents for storage in vector database
        
        Args:
            documents: List of document texts to embed
            
        Returns:
            List of embedding vectors
        """
        result = await self.create_embeddings(documents, task="retrieval.passage")
        return [item["embedding"] for item in result["data"]]
    
    async def embed_query(self, query: str) -> List[float]:
        """
        Embed query for vector search
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        result = await self.create_embeddings(query, task="retrieval.query")
        return result["data"][0]["embedding"]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Jina embeddings service health"""
        try:
            test_result = await self.create_embeddings("Health check test")
            return {
                "status": "healthy",
                "model": self.model,
                "dimensions": len(test_result["data"][0]["embedding"]),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "model": self.model,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class JinaRerankerClient:
    """Client for Jina AI reranking service"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.jina_api_key
        self.model = model or settings.default_reranker_model
        self.base_url = "https://api.jina.ai/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
        logger.info("Jina reranker client initialized", model=self.model)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: Optional[int] = None,
        return_documents: bool = True
    ) -> Dict[str, Any]:
        """
        Rerank documents based on relevance to query
        
        Args:
            query: Search query
            documents: List of documents to rerank
            top_k: Number of top results to return
            return_documents: Whether to return document text
            
        Returns:
            Reranked results with scores and optionally documents
        """
        top_k = top_k or settings.rerank_top_k
        
        try:
            payload = {
                "model": self.model,
                "query": query,
                "documents": documents,
                "top_n": min(top_k, len(documents)),
                "return_documents": return_documents
            }
            
            logger.debug(
                "Reranking documents",
                model=self.model,
                query_length=len(query),
                doc_count=len(documents),
                top_k=top_k
            )
            
            response = await self.client.post(
                f"{self.base_url}/rerank",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            logger.info(
                "Reranking completed",
                model=self.model,
                results_count=len(result.get("results", [])),
                total_tokens=result.get("usage", {}).get("total_tokens", 0)
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Reranking failed",
                model=self.model,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Jina reranker service health"""
        try:
            test_result = await self.rerank(
                query="test query",
                documents=["test document 1", "test document 2"],
                top_k=1
            )
            return {
                "status": "healthy",
                "model": self.model,
                "results_returned": len(test_result.get("results", [])),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "model": self.model,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class JinaReaderClient:
    """Client for Jina AI reader service for document processing"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.jina_api_key
        self.base_url = "https://api.jina.ai/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0  # Longer timeout for document processing
        )
        
        logger.info("Jina reader client initialized")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    async def read_url(self, url: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Read and extract content from a URL
        
        Args:
            url: URL to read
            options: Additional processing options
            
        Returns:
            Extracted content and metadata
        """
        try:
            payload = {
                "url": url,
                **(options or {})
            }
            
            logger.debug("Reading URL", url=url)
            
            response = await self.client.post(
                f"{self.base_url}/readers",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            logger.info(
                "URL reading completed",
                url=url,
                content_length=len(result.get("content", ""))
            )
            
            return result
            
        except Exception as e:
            logger.error("URL reading failed", url=url, error=str(e))
            raise
    
    async def process_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Process uploaded file content
        
        Args:
            file_content: Raw file bytes
            filename: Original filename for type detection
            
        Returns:
            Extracted text content and metadata
        """
        try:
            # For now, implement basic text extraction
            # In production, you might use Jina's document processing APIs
            if filename.lower().endswith('.txt'):
                content = file_content.decode('utf-8')
                return {
                    "content": content,
                    "metadata": {
                        "filename": filename,
                        "type": "text/plain",
                        "length": len(content)
                    }
                }
            else:
                # Placeholder for other file types
                # Would integrate with actual Jina document processing APIs
                raise ValueError(f"Unsupported file type: {filename}")
                
        except Exception as e:
            logger.error("File processing failed", filename=filename, error=str(e))
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class JinaServicesManager:
    """Unified manager for all Jina AI services"""
    
    def __init__(self):
        self.embeddings = JinaEmbeddingsClient()
        self.reranker = JinaRerankerClient()
        self.reader = JinaReaderClient()
        
        logger.info("Jina services manager initialized")
    
    async def health_check_all(self) -> Dict[str, Dict[str, Any]]:
        """Check health of all Jina services"""
        results = {}
        
        try:
            results["embeddings"] = await self.embeddings.health_check()
        except Exception as e:
            results["embeddings"] = {"status": "error", "error": str(e)}
        
        try:
            results["reranker"] = await self.reranker.health_check()
        except Exception as e:
            results["reranker"] = {"status": "error", "error": str(e)}
        
        results["reader"] = {"status": "ready", "note": "File processing ready"}
        
        return results
    
    async def close_all(self):
        """Close all service clients"""
        await self.embeddings.close()
        await self.reranker.close()
        await self.reader.close()


# Global service manager instance
_jina_services: Optional[JinaServicesManager] = None


def get_jina_services() -> JinaServicesManager:
    """Get shared Jina services manager instance"""
    global _jina_services
    if _jina_services is None:
        _jina_services = JinaServicesManager()
    return _jina_services


async def test_jina_integration() -> Dict[str, Any]:
    """Test all Jina AI services"""
    try:
        services = get_jina_services()
        
        # Test embeddings
        embedding_result = await services.embeddings.embed_query("test query")
        
        # Test reranking
        rerank_result = await services.reranker.rerank(
            query="test query",
            documents=["relevant document", "less relevant document"],
            top_k=1
        )
        
        # Test health checks
        health_results = await services.health_check_all()
        
        return {
            "status": "success",
            "embedding_dimensions": len(embedding_result),
            "rerank_results": len(rerank_result.get("results", [])),
            "health_checks": health_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }