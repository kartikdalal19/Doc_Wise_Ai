import os

from tavily import TavilyClient
from langchain_core.tools import tool


@tool
def tavily_search(query: str) -> str:
    """
    Search the web using Tavily.

    Args:
        query: User question

    Returns:
        Relevant web results.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Tavily API key is not configured."

    client = TavilyClient(api_key)


    try:
      result = client.search(
        query=query,
        max_results=3
    )
    except Exception as e:
      return f"Tavily search failed: {e}"

    text = ""

    for r in result["results"]:

        text += (
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"{r['content']}\n\n"
        )

    return text