from typing import List
from langchain_core.documents import Document
from state.graph_state import GraphState
from chains.hallucination_relevance_chain import hallucination_chain, relevance_chain

def format_docs(docs: List[Document]) -> str:
    """
    문서들을 문자열로 변환합니다.
    """
    return "\n\n".join(doc.page_content for doc in docs) 

def decide_to_generate(state: dict) -> str:
    """
    grade_documents 노드의 결과를 받아서 다음 노드 이름을 반환합니다.
    documents가 2개 이상이면 generate_answer, 아니면 rewrite_query 반환
    """
    print("\n=== decide_to_generate ===")
    documents = state.get("documents", [])
    print(f"Documents count: {len(documents)}")
    
    if len(documents) >= 2:
        print("Decision: generate_answer")
        return "generate_answer"
    else:
        print("Decision: rewrite_query")
        return "rewrite_query"



def grade_generation_v_documents_and_question(state: dict) -> str:
    """
    state에서 question, generation, documents를 꺼내서
    hallucination_chain, relevance_chain을 실행하고
    usefulness를 판단해서 useful, not useful, not supported 중 하나를 반환
    """
    print("\n=== grade_generation_v_documents_and_question ===")
    question = state.get("question", "")
    generation = state.get("generation", "")
    documents = state.get("documents", [])

    # 문서 내용을 하나의 문자열로 합침 (필요시)
    docs_str = format_docs(documents)

    # hallucination 판단
    print("Checking for hallucinations...")
    hallucination_result = hallucination_chain().invoke({
        "documents": docs_str,
        "generation": generation
    })
    hallucination = hallucination_result.binary_score
    print(f"Hallucination check result: {hallucination}")

    # relevance 판단
    print("Checking relevance...")
    relevance_result = relevance_chain().invoke({
        "documents": docs_str,
        "generation": generation
    })
    relevance = relevance_result.binary_score
    print(f"Relevance check result: {relevance}")

    # 분기
    if relevance == "yes" and hallucination == "no":
        print("Final decision: useful")
        return "useful"
    elif relevance == "no" or hallucination == "yes":
        print("Final decision: not useful")
        return "not useful"
    else:
        print("Final decision: not supported")
        return "not supported"
