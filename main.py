from langgraph.graph import StateGraph, END
from nodes.retrieval_node import retrieve
from nodes.grading_node import grade_documents
from nodes.generation_node import generate
from nodes.rewrite_node import rewrite
from nodes.websearch_node import websearch
from state.graph_state import GraphState
from utils.helpers import decide_to_generate, grade_generation_v_documents_and_question
from langchain_core.documents import Document
from typing import List, TypedDict

if __name__ == "__main__":

    # 그래프 정의
    workflow = StateGraph(GraphState)

    # 노드 추가
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade", grade_documents)
    workflow.add_node("rewrite", rewrite)
    workflow.add_node("websearch", websearch)
    workflow.add_node("generate", generate)

    # 시작 노드 설정
    workflow.set_entry_point("retrieve")

    # 엣지 정의
    workflow.add_edge("retrieve", "grade")
    workflow.add_conditional_edges(
        "grade",
        decide_to_generate, {
            "rewrite_query": "rewrite",
            "generate_answer": "generate"
        }
    )
    workflow.add_edge("rewrite", "websearch")
    workflow.add_edge("websearch", "generate")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question, {
            "useful": END,
            "not useful": "websearch",
            "not supported": "generate"
        }
    )
    # 워크플로우 생성
    app = workflow.compile()

    result = app.invoke({"question": "What's BTS?", "documents": []})
    
    # 최종 답변만 출력
    print("\n=== 최종 답변 ===")
    print(result["generation"].content)