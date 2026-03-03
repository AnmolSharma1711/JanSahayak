"""
RAG Retrieval Agent
Dedicated agent for vector database queries
Supports both FAISS and Pinecone backends
"""

import json
from rag.vectorstore_loader import load_scheme_vectorstore, load_exam_vectorstore


def run_rag_agent(query: str, database: str = "schemes", k: int = 5) -> dict:
    """
    Performs RAG retrieval from specified vectorstore
    
    Args:
        query: Search query
        database: "schemes" or "exams"
        k: Number of documents to retrieve
        
    Returns:
        Retrieved documents dictionary
    """
    try:
        if database == "schemes":
            vectorstore = load_scheme_vectorstore()
        elif database == "exams":
            vectorstore = load_exam_vectorstore()
        else:
            return {
                "error": f"Invalid database: {database}. Use 'schemes' or 'exams'",
                "documents": []
            }
        
        # Similarity search
        docs = vectorstore.similarity_search(query, k=k)
        
        # Format results
        formatted_docs = []
        for i, doc in enumerate(docs):
            formatted_docs.append({
                "id": i + 1,
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": doc.metadata.get('source', 'Unknown')
            })
        
        return {
            "query": query,
            "database": database,
            "documents_found": len(formatted_docs),
            "documents": formatted_docs
        }
    
    except FileNotFoundError as e:
        return {
            "error": f"Vectorstore not found for {database}. Please build it first.",
            "documents": []
        }
    except Exception as e:
        return {
            "error": str(e),
            "documents": []
        }


def hybrid_rag_search(query: str, k: int = 3) -> dict:
    """
    Searches both scheme and exam databases
    
    Args:
        query: Search query
        k: Number of documents per database
        
    Returns:
        Combined results from both databases
    """
    scheme_results = run_rag_agent(query, database="schemes", k=k)
    exam_results = run_rag_agent(query, database="exams", k=k)
    
    return {
        "query": query,
        "scheme_results": scheme_results,
        "exam_results": exam_results
    }


if __name__ == "__main__":
    # Test the agent
    result = run_rag_agent("agricultural schemes for farmers", database="schemes", k=3)
    print(json.dumps(result, indent=2))
