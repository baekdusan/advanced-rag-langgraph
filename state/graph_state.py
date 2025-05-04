from typing import TypedDict, List, Dict, Any
from langchain_core.documents import Document

class GraphState(TypedDict):
    """
    The state of the graph.
    Attributes:
        question: question
        generation: Generate LLM Answer
        web_search_add: Flag indicating whether to add web search - yes or no
        documents: List of context documents
    """
    question: str
    generation: str
    web_search_add: str
    documents: List[Document]