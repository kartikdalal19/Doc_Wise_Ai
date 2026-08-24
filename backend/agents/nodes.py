from agents.state import GraphState
from core.config import settings

from tools.wiki_search import wikipedia_search
from tools.tavily_search import tavily_search
from tools.summary_tool import SummaryTool

# =====================================================
# Retrieve Node
# =====================================================

class RetrieveNode:

    def __init__(self, retriever):
        self.retriever = retriever

    def __call__(self, state: GraphState):

        results = self.retriever.retrieve(
            state["question"],
            top_k=settings.TOP_K,
        )

        print("\nRetrieved Chunks")
        print("=" * 60)

        for i, result in enumerate(results, 1):
            print(f"\nChunk {i}")
            print("Score:", result["score"])
            print("Page :", result["chunk"].page_number)
            print(result["chunk"].text[:300])

        context = "\n\n".join(
            f"""
Source: {result['chunk'].source}
Page: {result['chunk'].page_number}

{result['chunk'].text}
"""
            for result in results
        )

        retrieval_score = 0.0

        if results:
            retrieval_score = results[0]["score"]

        return {

            "context": context,

            "doc_context": context,

            "retrieved_chunks": results,

            "retrieval_score": retrieval_score,

            "retrieved_pages": [
                result["chunk"].page_number
                for result in results
            ],

            "retrieved_sources": [
                {
                    "source": result["chunk"].source,
                    "page": result["chunk"].page_number,
                    "score": result["score"],
                }
                for result in results
            ],

            "sources": list(
                {
                    result["chunk"].source
                    for result in results
                }
            )
        }


# =====================================================
# Decide Node
# =====================================================

class DecideNode:

    def __call__(self, state):

        score = state["retrieval_score"]

        print(
            "Best Retrieval Score:",
            score
        )

        if score < settings.RETRIEVAL_THRESHOLD:


         return {


          "need_web_search":True,

          "document_available":False,


          "routing_decision":
          "Retrieval score low → Searching external tools",


          "thoughts":[
            "Document retrieval failed",
            "External knowledge required",
            "Calling Wikipedia and Tavily tools"
        ]

    }



        return {


         "need_web_search":False,

         "document_available":True,


         "routing_decision":
         "Retrieval score sufficient → Using document",


         "thoughts":[
          "Relevant document chunks found",
          "No external search required",
          "Generating answer from uploaded document"
    ]

}


# =====================================================
# Tool Node
# =====================================================

# class ToolNode:

#     """
#     Executes external tools.

#     Current:
#         - Wikipedia
#         - Tavily

#     Future:
#         - Calculator
#         - SQL
#         - Weather
#         - Python REPL
#         - Arxiv
#         - DuckDuckGo
#         - SerpAPI
#     """

#     def __call__(self, state):

#         question = state["question"]

#         try:
#             wiki = wikipedia_search.invoke(
#                 {
#                     "query": question
#                 }
#             )
#         except Exception as e:
#             wiki = f"Wikipedia search failed: {e}"


#         try:
#             tavily = tavily_search.invoke(
#                 {
#                     "query": question
#                 }
#             )
#         except Exception as e:
#             tavily = f"Tavily search failed: {e}"

#         combined = f"""
# Wikipedia

# {wiki}

# ----------------------------------------

# Tavily

# {tavily}
# """

#         return {

#             "wiki_result": wiki,

#             "tavily_result": tavily,

#             "web_results": combined,

#             "tools_used": [

#                 "Wikipedia",

#                 "Tavily"

#             ],

#             "thoughts":[

#              "Calling Wikipedia tool",

#              "Calling Tavily search tool",

#              "Combining external evidence"

# ],

#             "sources": [

#                 "Wikipedia",

#                 "Tavily"

#             ]
#         }

class ToolNode:
    """
    Executes external tools.

    Current:
        - Wikipedia
        - Tavily

    Future:
        - Calculator
        - SQL
        - Weather
        - Python REPL
        - Arxiv
        - DuckDuckGo
        - SerpAPI
    """

    def __call__(self, state):

        question = state["question"]

        wiki = None
        tavily = None

        tools_used = []
        successful_sources = []
        failed_sources = []

        thoughts = []

        # ==================================================
        # WIKIPEDIA
        # ==================================================

        try:

            wiki = wikipedia_search.invoke(
                {
                    "query": question
                }
            )

            if (
                wiki
                and not wiki.startswith("WIKIPEDIA_")
            ):

                successful_sources.append(
                    "Wikipedia"
                )

                tools_used.append(
                    "Wikipedia"
                )

                thoughts.append(
                    "Wikipedia returned usable evidence"
                )

            else:

                failed_sources.append(
                    "Wikipedia"
                )

                thoughts.append(
                    "Wikipedia search failed or returned no usable evidence"
                )

        except Exception as e:

            print(
                f"[ToolNode] Wikipedia error: {e}"
            )

            wiki = None

            failed_sources.append(
                "Wikipedia"
            )

            thoughts.append(
                "Wikipedia tool failed"
            )


        # ==================================================
        # TAVILY
        # ==================================================

        try:

            tavily = tavily_search.invoke(
                {
                    "query": question
                }
            )

            if tavily and str(tavily).strip():

                successful_sources.append(
                    "Tavily"
                )

                tools_used.append(
                    "Tavily"
                )

                thoughts.append(
                    "Tavily returned usable evidence"
                )

            else:

                failed_sources.append(
                    "Tavily"
                )

                thoughts.append(
                    "Tavily returned no usable evidence"
                )

        except Exception as e:

            print(
                f"[ToolNode] Tavily error: {e}"
            )

            tavily = None

            failed_sources.append(
                "Tavily"
            )

            thoughts.append(
                "Tavily search failed"
            )


        # ==================================================
        # BUILD CLEAN WEB EVIDENCE
        # ==================================================

        evidence_parts = []


        if wiki:

            evidence_parts.append(
                f"""
SOURCE: Wikipedia

{wiki}
"""
            )


        if tavily:

            evidence_parts.append(
                f"""
SOURCE: Tavily

{tavily}
"""
            )


        if evidence_parts:

            combined = "\n\n".join(
                evidence_parts
            )

        else:

            combined = (
                "No external evidence was available."
            )


        # ==================================================
        # FINAL TOOL STATE
        # ==================================================

        return {

            "wiki_result":
                wiki
                if wiki
                else "Wikipedia unavailable.",

            "tavily_result":
                tavily
                if tavily
                else "Tavily unavailable.",

            "web_results":
                combined,

            "tools_used":
                tools_used,

            "successful_sources":
                successful_sources,

            "failed_sources":
                failed_sources,

            "thoughts":
                thoughts,

            "sources":
                successful_sources
        }



# =====================================================
# Summary Node
# =====================================================

class SummaryNode:

    def __init__(self, retriever):

        self.tool = SummaryTool(retriever)

    def __call__(self, state):

        summary = self.tool.invoke(
            state["question"]
        )

        return {

            "summary": summary,

            "answer": summary,

            "answer_source": "summary",

            "document_answer": summary,

            "thoughts":[

                "Summary tool generated document summary"

            ]

        }
    
# =====================================================
# Generate Node
# =====================================================

class GenerateNode:

    def __init__(self, chain):

        self.chain = chain

    def __call__(self, state):

        # ----------------------------------------
        # Answer using Uploaded Document
        # ----------------------------------------

        if state["document_available"]:

            answer = self.chain.document_invoke(

                context=state["context"],

                question=state["question"]

            )

            return {


                "document_answer":answer,


                "answer":answer,


                "answer_source":"document",


                "thoughts":[

                "LLM generated answer from document context"

]


}

        # ----------------------------------------
        # Answer using External Tools
        # ----------------------------------------

        answer = self.chain.web_invoke(

            question=state["question"],

            wiki=state["wiki_result"],

            tavily=state["tavily_result"]

        )

        return {


            "web_answer":answer,


            "answer":answer,


            "answer_source":"web",


            "thoughts":[

            "LLM generated answer using external evidence"

]


}
       
