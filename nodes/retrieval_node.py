from typing import Dict, Any
from state.graph_state import GraphState
from chains.retrieval_chain import create_retrieval_chain

retrieval_chain = create_retrieval_chain()

def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    검색 노드: 사용자 질문에 대한 관련 문서를 검색합니다.
    """
    print("\n=== retrieve ===")
    question = state["question"]
    print(f"Question: {question}")
    
    # 문서 검색
    documents = retrieval_chain.invoke(question)
    print(f"Retrieved {len(documents)} documents")
    
    return {**state, "documents": documents} 