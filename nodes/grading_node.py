from typing import Dict, Any
from state.graph_state import GraphState
from chains.grading_chain import create_grading_chain

grading_chain = create_grading_chain()

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    문서 평가 노드: 검색된 문서의 관련성을 평가합니다.
    """
    print("\n=== grade_documents ===")
    question = state["question"]
    documents = state["documents"]
    print(f"Evaluating {len(documents)} documents")
    
    # 각 문서에 대해 평가 수행
    graded_docs = []
    for i, doc in enumerate(documents):
        print(f"\nEvaluating document {i+1}/{len(documents)}")
        result = grading_chain.invoke({
            "question": question,
            "document": doc.page_content
        })
        print(f"Document {i+1} relevance: {result.binary_score}")
        if result.binary_score == "yes":
            graded_docs.append(doc)
    
    print(f"\nTotal relevant documents: {len(graded_docs)}")
    return {**state, "documents": graded_docs} 