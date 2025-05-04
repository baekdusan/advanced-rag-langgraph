from typing import Dict, Any
from state.graph_state import GraphState
from chains.generation_chain import create_generation_chain
from utils.helpers import format_docs

generation_chain = create_generation_chain()

def generate(state: GraphState) -> Dict[str, Any]:
    """
    답변 생성 노드: 평가된 문서와 웹 검색 결과를 기반으로 답변을 생성합니다.
    """
    print("\n=== generate ===")
    question = state["question"]
    documents = state["documents"]
    web_search_add = state.get("web_search_add", "")
    
    print(f"Generating answer using {len(documents)} documents and web search results")
    
    # 문서를 문자열로 변환
    context = format_docs(documents)
    
    # 웹 검색 결과가 있으면 추가
    if web_search_add:
        context += "\n\nAdditional information from web search:\n" + web_search_add
    
    # 답변 생성
    print("Generating answer...")
    answer = generation_chain.invoke({
        "question": question,
        "context": context
    })
    print("Answer generated successfully")
    
    return {**state, "generation": answer} 