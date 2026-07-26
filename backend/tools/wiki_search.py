from langchain_core.tools import tool
import wikipedia
@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for factual information.
    Use this tool when the user asks for:
    - definitions
    - historical facts
    - people
    - places
    - concepts
    - general knowledge
    Input:
        query
    Returns:
        Wikipedia summary
    """
    try:
        result = wikipedia.summary(
            query,
            sentences=5
        )
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return (
            "Multiple Wikipedia pages found:\n"
            + ", ".join(e.options[:5])
        )
    except wikipedia.exceptions.PageError:

        return "No Wikipedia page found."
    except Exception as e:
        return f"Wikipedia search failed: {e}"