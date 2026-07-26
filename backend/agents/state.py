from typing import TypedDict, List


class GraphState(TypedDict):

    # ==================================================
    # User Input
    # ==================================================

    question: str

    # ==================================================
    # Retrieval
    # ==================================================

    retrieved_chunks: list

    retrieved_pages: List[int]

    retrieved_sources: List[dict]

    retrieval_score: float

    context: str

    doc_context: str

    # ==================================================
    # Routing
    # ==================================================

    need_web_search: bool

    document_available: bool

    # ==================================================
    # Tool Outputs
    # ==================================================

    wiki_result: str

    tavily_result: str

    web_results: str

    sources: List[str]

    tools_used: List[str]

    thoughts: list

    routing_decision: str



    # ==================================================
    # Generated Answers
    # ==================================================

    document_answer: str

    web_answer: str

    answer: str

    answer_source: str

    summary: str

    # ==================================================
    # Fact Checking
    # ==================================================

    verification: str

    verified: bool

    confidence: float

