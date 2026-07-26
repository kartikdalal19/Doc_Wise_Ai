from langgraph.graph import StateGraph, START, END

from agents.state import GraphState
from agents.fact_checker import FactChecker

from agents.nodes import (

    RetrieveNode,

    DecideNode,

    ToolNode,

    SummaryNode,

    GenerateNode,

)


def is_summary_request(question):

    q = question.lower()

    keywords = [

        "summary",

        "summarize",

        "summarise",

        "overview",

        "brief"

    ]

    return any(

        word in q

        for word in keywords

    )


# =====================================================
# Routing Function
# =====================================================
def route(state):

    if is_summary_request(

        state["question"]

    ):

        print(

            "Going to SUMMARY NODE"

        )

        return "summary"

    print(

        "ROUTING DECISION:",

        state["need_web_search"]

    )

    if state["need_web_search"]:

        print(

            "Going to TOOL NODE"

        )

        return "tool"

    print(

        "Going to GENERATE"

    )

    return "generate"

# =====================================================
# Graph
# =====================================================

class RAGGraph:

    def __init__(self, retriever, chain):

        builder = StateGraph(GraphState)

        # ---------------------------
        # Nodes
        # ---------------------------

        builder.add_node(
            "retrieve",
            RetrieveNode(retriever)
        )

        builder.add_node(
            "decide",
            DecideNode()
        )

        builder.add_node(
            "tool",
            ToolNode()
        )

        builder.add_node(
            "summary",
            SummaryNode(retriever)
        )

        builder.add_node(
            "generate",
            GenerateNode(chain)
        )

        builder.add_node(
            "fact_checker",
            FactChecker()
        )

        # ---------------------------
        # Flow
        # ---------------------------

        builder.add_edge(
            START,
            "retrieve"
        )

        builder.add_edge(
            "retrieve",
            "decide"
        )

        builder.add_conditional_edges(

            "decide",

            route,

            {

            "summary":"summary",

            "tool":"tool",

            "generate":"generate"

            }

        )

        builder.add_edge(
            "summary",
            "fact_checker"
        )

        builder.add_edge(

            "tool",

            "generate"

        )

        builder.add_edge(

            "generate",

            "fact_checker"

        )

        builder.add_edge(

            "fact_checker",

            END

        )

        self.graph = builder.compile()

    def invoke(self, question):

        return self.graph.invoke(

            {

                # User

                "question": question,

                # Retrieval

                "context": "",

                "retrieved_chunks": [],

                "retrieval_score": 0.0,

                # Routing

                "need_web_search": False,

                "document_available": False,

                # Tool Outputs

                "wiki_result": "",

                "tavily_result": "",

                "web_results": "",

                "tools_used": [],

                "doc_context": "",

                "retrieved_pages": [],

                "retrieved_sources": [],


                "thoughts":[],

                "routing_decision":"",

                # Answers

                "document_answer": "",

                "web_answer": "",

                "answer": "",

                "answer_source": "",

                "summary": "",

                # Metadata

                "sources": [],

                # Fact Checking

                "verification": "",

                "verified": False,

                "confidence": 0.0

            }

        )