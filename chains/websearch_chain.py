from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser

def create_websearch_chain():
    """
    웹 검색을 위한 랭체인을 생성합니다.
    """

    websearch_tool = TavilySearchResults(max_results=10, search_depth="advanced", max_tokens=1000)
    
    def format_search_results(results):
        formatted = ""
        for result in results:
            if isinstance(result, dict):
                formatted += f"Title: {result.get('title', '')}\n"
                formatted += f"Content: {result.get('content', '')}\n\n"
            else:
                formatted += f"{str(result)}\n\n"
        return formatted
    
    # 검색 결과를 문자열로 변환하는 체인
    websearch_chain = websearch_tool | format_search_results

    return websearch_chain