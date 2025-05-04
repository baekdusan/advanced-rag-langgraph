from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from utils.helpers import format_docs

def create_generation_chain():
    """
    답변 생성을 위한 랭체인을 생성합니다.
    """
    # 답변 생성 프롬프트
    prompt = """You are an Assistant for a Q&A.
    Answer the question using the following retrieved Context fragment.
    If there is no context or you do not know the answer, answer that you do not know the answer.
    Do not construct an answer unless it corresponds to the provided Context.
    If the Context value is null when constructing an answer, answer 'RAG does not have relevant information'.
    Please provide a detailed and summarized answer to the question.

    Question: {question}
    Context: {context}
    Answer:
    """

    # 프롬프트 템플릿 생성
    prompt_template = ChatPromptTemplate.from_template(prompt)
    
    # LLM 초기화
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 체인 생성
    chain = prompt_template | llm
    
    return chain