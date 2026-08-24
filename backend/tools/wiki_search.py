# from langchain_core.tools import tool
# import wikipedia
# @tool
# def wikipedia_search(query: str) -> str:
#     """
#     Search Wikipedia for factual information.
#     Use this tool when the user asks for:
#     - definitions
#     - historical facts
#     - people
#     - places
#     - concepts
#     - general knowledge
#     Input:
#         query
#     Returns:
#         Wikipedia summary
#     """
#     try:
#         result = wikipedia.summary(
#             query,
#             sentences=5
#         )
#         return result
#     except wikipedia.exceptions.DisambiguationError as e:
#         return (
#             "Multiple Wikipedia pages found:\n"
#             + ", ".join(e.options[:5])
#         )
#     except wikipedia.exceptions.PageError:

#         return "No Wikipedia page found."
#     except Exception as e:
#         return f"Wikipedia search failed: {e}"





from langchain_core.tools import tool
import wikipedia
import time


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for factual information.

    Use this tool for:
    - definitions
    - historical facts
    - people
    - places
    - concepts
    - general knowledge

    Returns:
        Wikipedia summary or a clear failure message.
    """

    try:

        # Set language explicitly
        wikipedia.set_lang("en")

        # First try the exact query
        try:

            result = wikipedia.summary(
                query,
                sentences=5,
                auto_suggest=True
            )

        except wikipedia.exceptions.DisambiguationError as e:

            # Try the first few suggested pages
            if not e.options:
                return "WIKIPEDIA_UNAVAILABLE"

            for option in e.options[:3]:

                try:

                    result = wikipedia.summary(
                        option,
                        sentences=5,
                        auto_suggest=False
                    )

                    if result and result.strip():
                        return result

                except Exception:
                    continue

            return "WIKIPEDIA_NO_RELEVANT_PAGE"

        except wikipedia.exceptions.PageError:

            # Try Wikipedia search manually
            search_results = wikipedia.search(
                query,
                results=3
            )

            if not search_results:
                return "WIKIPEDIA_NO_RELEVANT_PAGE"

            for result_title in search_results:

                try:

                    result = wikipedia.summary(
                        result_title,
                        sentences=5,
                        auto_suggest=False
                    )

                    if result and result.strip():
                        return result

                except Exception:
                    continue

            return "WIKIPEDIA_NO_RELEVANT_PAGE"

        # Validate response
        if not result or not result.strip():

            return "WIKIPEDIA_EMPTY_RESPONSE"

        return result.strip()

    except Exception as e:

        print(
            f"[Wikipedia Error] {type(e).__name__}: {e}"
        )

        return (
            "WIKIPEDIA_UNAVAILABLE"
        )
