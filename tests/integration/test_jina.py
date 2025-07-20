"""
Test script for Jina AI integration
"""
import asyncio
import sys
sys.path.append('.')
sys.path.append('..')

from ai.src.jina_integration import test_jina_integration, get_jina_services
from ai.src.config import get_ai_settings


async def test_jina_services():
    """Test Jina AI services functionality"""
    print("🧪 Testing Jina AI Integration...")
    
    # Test configuration
    settings = get_ai_settings()
    print(f"✅ Configuration loaded:")
    print(f"   - Embeddings Model: {settings.default_embedding_model}")
    print(f"   - Reranker Model: {settings.default_reranker_model}")
    print(f"   - Embedding Dimensions: {settings.embedding_dimensions}")
    print(f"   - API Key configured: {settings.jina_api_key[:10]}...")
    
    # Test services
    try:
        services = get_jina_services()
        
        # Test embeddings service
        print("\n📊 Testing Embeddings Service...")
        embedding = await services.embeddings.embed_query("test query for embeddings")
        print(f"✅ Embedding created: {len(embedding)} dimensions")
        
        # Test batch embeddings
        documents = [
            "This is a document about artificial intelligence",
            "This document discusses machine learning applications",
            "This text covers natural language processing"
        ]
        doc_embeddings = await services.embeddings.embed_documents(documents)
        print(f"✅ Batch embeddings: {len(doc_embeddings)} documents embedded")
        
        # Test reranker service
        print("\n🔄 Testing Reranker Service...")
        rerank_result = await services.reranker.rerank(
            query="artificial intelligence applications",
            documents=documents,
            top_k=2
        )
        print(f"✅ Reranking completed: {len(rerank_result['results'])} results")
        for i, result in enumerate(rerank_result['results']):
            print(f"   {i+1}. Score: {result['relevance_score']:.4f}")
        
        # Health check all services
        print("\n🏥 Testing Service Health...")
        health_results = await services.health_check_all()
        for service, health in health_results.items():
            status = health.get('status', 'unknown')
            print(f"✅ {service.title()}: {status}")
        
        # Run full integration test
        print("\n🎯 Running Full Integration Test...")
        result = await test_jina_integration()
        
        if result["status"] == "success":
            print("✅ Jina AI Integration Test PASSED")
            print(f"📐 Embedding Dimensions: {result['embedding_dimensions']}")
            print(f"🔄 Rerank Results: {result['rerank_results']}")
        else:
            print("❌ Jina AI Integration Test FAILED")
            print(f"💥 Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
    
    finally:
        # Clean up
        try:
            await services.close_all()
            print("🧹 Cleaned up service connections")
        except:
            pass
    
    print("\n🎉 Jina AI integration test complete!")


if __name__ == "__main__":
    asyncio.run(test_jina_services())