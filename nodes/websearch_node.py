from typing import Dict, Any
from state.graph_state import GraphState
from chains.websearch_chain import create_websearch_chain
from langchain_core.documents import Document

websearch_chain = create_websearch_chain()

def websearch(state: GraphState) -> Dict[str, Any]:
    """
    웹 검색을 수행하는 노드
    """
    print("\n=== websearch ===")
    question = state["question"]
    print(f"Searching for: {question}")
    
    try:
        websearch_results = websearch_chain.invoke(question)
        print(f"Found {len(websearch_results)} results")
        
        # 검색 결과를 문자열로 변환하여 web_search_add에 저장
        web_search_content = ""
        for result in websearch_results:
            if isinstance(result, dict):
                content = f"Title: {result.get('title', '')}\nContent: {result.get('content', '')}\n\n"
            else:
                content = f"{str(result)}\n\n"
            web_search_content += content
        
        print(f"Converted web search results to string")
        return {**state, "web_search_add": web_search_content}
    except Exception as e:
        print(f"Error in websearch: {str(e)}")
        # 에러 발생 시 빈 문자열 반환
        return {**state, "web_search_add": ""}
    