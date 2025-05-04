from typing import Dict, Any
from state.graph_state import GraphState
from chains.rewrite_chain import rewrite_chain

rewrite_chain_instance = rewrite_chain()

def rewrite(state: GraphState) -> Dict[str, Any]:
    """
    질문을 재작성하는 노드
    """
    print("rewrite node documents:", type(state.get("documents")), state.get("documents"))
    question = state["question"]
    rewritten_question = rewrite_chain_instance.invoke({"question": question})
    return {**state, "question": rewritten_question}
    