"""
Web Search Agent
Uses Tavily to search government websites for real-time information
"""

from tools.tavily_tool import tavily_search, government_focused_search


def run_search_agent(query: str, government_only: bool = True) -> dict:
    """
    Performs web search for government information
    
    Args:
        query: Search query
        government_only: If True, restricts to .gov.in domains
        
    Returns:
        Search results dictionary
    """
    try:
        if government_only:
            results = government_focused_search(query)
        else:
            results = tavily_search(query)
        
        return {
            "query": query,
            "results": results,
            "government_only": government_only
        }
    
    except Exception as e:
        return {
            "query": query,
            "error": str(e),
            "results": []
        }


def search_scheme_details(scheme_name: str) -> dict:
    """
    Search for specific scheme details
    
    Args:
        scheme_name: Name of the government scheme
        
    Returns:
        Scheme details from official sources
    """
    query = f"{scheme_name} official website application process eligibility"
    return run_search_agent(query, government_only=True)


def search_exam_details(exam_name: str) -> dict:
    """
    Search for specific exam details
    
    Args:
        exam_name: Name of the competitive exam
        
    Returns:
        Exam details from official sources
    """
    query = f"{exam_name} official notification eligibility exam pattern 2026"
    return run_search_agent(query, government_only=True)


if __name__ == "__main__":
    # Test the agent
    result = run_search_agent("pradhan mantri kisan samman nidhi yojana", government_only=True)
    print(result)
