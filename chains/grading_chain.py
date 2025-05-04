from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from config.config import llm

class GradeDocument(BaseModel):
    binary_score: str = Field(
        description="Rates whether the document is relevant to the question with a 'yes' or 'no'"
    )

def create_grading_chain():
    """
    문서 평가를 위한 랭체인을 생성합니다.
    """
    # 문서 평가 LLM
    structured_llm_grader = llm.with_structured_output(GradeDocument)

    # 평가 프롬프트 템플릿
    SYSTEM_PROMPT = """
    You are a professional evaluator who evaluates the relevance of searched documents.
        - We assign a relevance rating to documents if they contain keywords or semantic meaning of the question.
        - Your rating should be 'yes' or 'no' indicating whether the article is relevant to the question.
    """

    # 평가 프롬프트 템플릿 생성
    grade_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", """Searched Documents: {document}
                    UserQuestion: {question} """),
    ])

    # 평가 체인 생성
    grader = grade_prompt | structured_llm_grader
    
    return grader 