from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from embedding import retriever  # retriever import

def create_retrieval_chain():
    """
    검색을 위한 랭체인을 생성합니다.
    """
    # 검색 체인은 retriever를 사용하여 문서를 검색합니다
    return retriever 