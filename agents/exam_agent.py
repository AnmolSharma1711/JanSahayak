"""
Exam Recommendation Agent
Provides competitive exam recommendations based on student profile
Supports both FAISS and Pinecone backends
"""

import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from rag.vectorstore_loader import load_exam_vectorstore
from prompts.exam_prompt import EXAM_PROMPT
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


def run_exam_agent(profile_data: dict, use_web_search: bool = True, vectorstore=None) -> dict:
    """
    Recommends competitive exams based on student profile
    
    Args:
        profile_data: Structured user profile
        use_web_search: Whether to use Tavily for live search
        vectorstore: Pre-loaded FAISS vectorstore (optional, avoids repeated loading)
        
    Returns:
        Exam recommendations dictionary
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
                Student Profile:
                Education: {profile_data.get('education', 'N/A')}
                Age: {profile_data.get('age', 'N/A')}
                Interests: {profile_data.get('interests', 'N/A')}
                Skills: {profile_data.get('skills', 'N/A')}
                Occupation: {profile_data.get('occupation', 'N/A')}
                """
                
                # RAG retrieval
                docs = vectorstore.similarity_search(search_query, k=5)
                context = "\n\n".join([f"Document {i+1}:\n{d.page_content}" for i, d in enumerate(docs)])
                sources_used = len(docs)
                print(f"✓ Retrieved {sources_used} exam documents from vectorstore")
            except Exception as e:
                print(f"⚠️  Error querying vectorstore: {str(e)}")
                context = "Vectorstore query failed. Using live web search."
        else:
            print("ℹ️  No vectorstore provided, using web search only")
            context = "No local exam database available. Using live web search."
        
        # Create profile string
        profile_str = json.dumps(profile_data, indent=2)
        
        # Web search (fallback or enhancement)
        web_context = ""
        if use_web_search:
            try:
                education = profile_data.get('education', 'graduate')
                interests = profile_data.get('interests', 'government jobs')
                web_query = f"competitive exams India {education} {interests} eligibility 2026"
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
                "recommendations": "Unable to retrieve exam information. Please ensure Tavily API key is configured or vectorstore is built.",
                "sources_used": 0,
                "web_search_used": use_web_search
            }
        
        # Generate recommendations
        llm = get_llm()
        
        prompt = EXAM_PROMPT.format(
            context=full_context,
            profile=profile_str
        )
        
        messages = [
            SystemMessage(content="You are an expert competitive exam advisor. Provide accurate, verified information only."),
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
        "education": "Bachelor's in Engineering",
        "age": 25,
        "interests": "Technical jobs, government sector",
        "skills": "Programming, problem solving",
        "occupation": "Student"
    }
    
    result = run_exam_agent(test_profile, use_web_search=False)
    print(json.dumps(result, indent=2))
