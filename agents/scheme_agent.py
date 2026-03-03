"""
Scheme Recommendation Agent
Provides RAG-based government scheme recommendations
Supports both FAISS and Pinecone backends
"""

import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from rag.vectorstore_loader import load_scheme_vectorstore
from prompts.scheme_prompt import SCHEME_PROMPT
from tools.tavily_tool import government_focused_search
from config import GROQ_API_KEY


def get_llm():
    """Initialize Groq LLM"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )


def run_scheme_agent(profile_data: dict, use_web_search: bool = True, vectorstore=None) -> dict:
    """
    Recommends government schemes based on user profile
    
    Args:
        profile_data: Structured user profile
        use_web_search: Whether to use Tavily for live search
        vectorstore: Pre-loaded FAISS vectorstore (optional, avoids repeated loading)
        
    Returns:
        Scheme recommendations dictionary
    """
    try:
        # Use provided vectorstore or try to load it
        context = ""
        sources_used = 0
        
        if vectorstore is not None:
            print("✅ Using pre-loaded vectorstore")
            try:
                # Create search query from profile
                search_query = f"""
                User Profile:
                Income: {profile_data.get('income', 'N/A')}
                Caste: {profile_data.get('caste', 'N/A')}
                State: {profile_data.get('state', 'N/A')}
                Age: {profile_data.get('age', 'N/A')}
                Gender: {profile_data.get('gender', 'N/A')}
                Employment: {profile_data.get('employment_status', 'N/A')}
                """
                
                # RAG retrieval
                docs = vectorstore.similarity_search(search_query, k=5)
                context = "\n\n".join([f"Document {i+1}:\n{d.page_content}" for i, d in enumerate(docs)])
                sources_used = len(docs)
                print(f"✓ Retrieved {sources_used} scheme documents from vectorstore")
            except Exception as e:
                print(f"⚠️  Error querying vectorstore: {str(e)}")
                context = "Vectorstore query failed. Using live web search."
        else:
            print("ℹ️  No vectorstore provided, using web search only")
            context = "No local scheme database available. Using live web search."
        
        # Create profile string
        profile_str = json.dumps(profile_data, indent=2)
        
        # Web search (fallback or enhancement)
        web_context = ""
        if use_web_search:
            try:
                state = profile_data.get('state', 'India')
                caste = profile_data.get('caste', '')
                income = profile_data.get('income', '')
                web_query = f"government schemes India {state} {caste} eligibility benefits 2026"
                print(f"🔍 Searching web: {web_query}")
                web_results = government_focused_search(web_query)
                web_context = f"\n\nLive Web Search Results:\n{web_results}"
                print("✓ Web search completed")
            except Exception as e:
                web_context = f"\n\nWeb search unavailable: {str(e)}"
                print(f"⚠ Web search failed: {str(e)}")
        
        # Combine contexts
        full_context = context + web_context
        
        # If no context at all, return helpful message
        if not full_context.strip():
            return {
                "recommendations": "Unable to retrieve scheme information. Please ensure Tavily API key is configured or vectorstore is built.",
                "sources_used": 0,
                "web_search_used": use_web_search
            }
        
        # Generate recommendations
        llm = get_llm()
        
        prompt = SCHEME_PROMPT.format(
            context=full_context,
            profile=profile_str
        )
        
        messages = [
            SystemMessage(content="You are an expert government scheme advisor. Provide accurate, verified information only."),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        
        return {
            "recommendations": response.content,
            "sources_used": sources_used,
            "web_search_used": use_web_search
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "recommendations": []
        }


if __name__ == "__main__":
    # Test the agent
    test_profile = {
        "income": "300000",
        "caste": "OBC",
        "state": "Maharashtra",
        "age": 25,
        "gender": "Male",
        "employment_status": "Unemployed",
        "education": "Bachelor's in Engineering"
    }
    
    result = run_scheme_agent(test_profile, use_web_search=False)
    print(json.dumps(result, indent=2))
