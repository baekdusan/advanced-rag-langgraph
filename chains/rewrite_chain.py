from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from config.config import llm

def rewrite_chain():
    """
    질문을 재작성하는 랭체인을 생성합니다.
    """

    SYSTEM_PROMPT = """Act as a question rewriter and perform the following tasks:
    - Convert the following input question into a better version optimized for web search.
    - When rewriting, look at the input question and infer its underlying semantic intent."""

    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", """First Questions:
            {question}
            Write improved queestions.
            """,
            )
        ]
    )

    # Create a rephraser chain
    question_rewriter = (re_write_prompt | llm | StrOutputParser()) # 입력으로

    return question_rewriter
