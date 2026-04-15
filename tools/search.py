from tavily import TavilyClient
from langchain.tools import tool
from config import TAVILY_API_KEY
from langsmith import traceable

tavily = TavilyClient(api_key=TAVILY_API_KEY)



@tool
@traceable(name="Tavily Search")
def search(query: str) -> str:
    """Search the web for latest information"""
    results = tavily.search(query=query)

    if not results or "results" not in results:
        return "No results found"

    
    # Clean output
    return "\n".join([r["content"][:500] for r in results["results"][:2]])