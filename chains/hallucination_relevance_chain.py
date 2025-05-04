from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from config.config import llm
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class GradeHallucination(BaseModel):
    binary_score: str = Field(
        description="Rates whether the answer has hallucinations with a 'yes' or 'no'"
    )

def hallucination_chain():

    structured_llm_grader = llm.with_structured_output(GradeHallucination)

    # 할루시네이션 유무 판단하기. score라는 key에 yes or no 형식으로 반환
    prompt = PromptTemplate(
        template=""" This is an evaluator that evaluates whether or not a hallucination is present.
        It gives a binary  'yes' or 'no' to indicate whether or not a hallucination is preset.
        If you have hallucinations. give 'yes'.
        Provide the binary score as a JSON with a
        single key 'score' and no preamble or explanation.
        Here are the facts:
        \n ------- \n
        {documents}
        \n ------ \n
        Here is the answer: {generation}   """,
        input_variables=["documents", "generation"],
    )

    hallucination_grader = prompt | structured_llm_grader

    return hallucination_grader

class GradeRelevance(BaseModel):
    binary_score: str = Field(
        description="Rates whether the answer is relevant to the question with a 'yes' or 'no'"
    )

def relevance_chain():

    structured_llm_grader = llm.with_structured_output(GradeRelevance)
    # 질문과 답변의 연관성 판단하기
    prompt = PromptTemplate(
        template="""You are a relevance evaluator.
        You connect the retrieved documnet to the user's question. If the document contains keywords relevant to the user rate it as relevant. There is no need to be strict. The goal is to filter out bad searches. \n
        You assign a binary score of 'yes' or 'no' to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no premable or explanation.
        \n ------- \n
        {documents}
        \n ------- \n
        Here is the answer: {generation}""",
        input_variables=["documents", "generation"],
    )

    retrievel_grader = prompt | structured_llm_grader

    return retrievel_grader

