"""
Tavily Search Tool
Enables live government website search
"""

from langchain_core.tools import Tool
from tavily import TavilyClient
from config import TAVILY_API_KEY


def get_tavily_client():
    """
    Initializes Tavily client with API key
    """
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    
    return TavilyClient(api_key=TAVILY_API_KEY)


def tavily_search(query: str) -> str:
    """
    Performs advanced search using Tavily API
    Optimized for government websites and official portals
    
    Args:
        query: Search query string
        
    Returns:
        Formatted search results
    """
    try:
        client = get_tavily_client()
        result = client.search(
            query=query, 
            search_depth="advanced",
            max_results=5
        )
        
        # Format results for agent consumption
        formatted_results = []
        for item in result.get('results', []):
            formatted_results.append({
                'title': item.get('title', 'N/A'),
                'url': item.get('url', 'N/A'),
                'content': item.get('content', 'N/A')
            })
        
        return str(formatted_results)
    
    except Exception as e:
        return f"Search error: {str(e)}"


def government_focused_search(query: str) -> str:
    """
    Enhanced search specifically for Indian government domains
    Adds .gov.in filter to queries
    
    Args:
        query: Base search query
        
    Returns:
        Search results from government websites
    """
    enhanced_query = f"{query} site:gov.in"
    return tavily_search(enhanced_query)


# LangChain Tool wrapper
tavily_tool = Tool(
    name="Tavily_Search",
    func=tavily_search,
    description="Search government websites and official portals for real-time information about schemes, exams, and policies"
)

government_search_tool = Tool(
    name="Government_Search",
    func=government_focused_search,
    description="Search specifically Indian government (.gov.in) websites for official scheme and exam information"
)
