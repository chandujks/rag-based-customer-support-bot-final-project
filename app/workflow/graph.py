from typing import List, TypedDict

from langgraph.graph import END, StateGraph

from app.config import settings
from app.hitl.store import add_to_queue
from app.llm.llm_client import get_llm


class GraphState(TypedDict):
    query: str
    context: List[str]
    response: str
    confidence: float
    escalate: bool
    ticket_id: str


def fallback_answer(query: str, context: List[str]) -> str:
    query_terms = {term for term in query.lower().split() if len(term) > 2}
    best_line = ""
    best_score = -1

    for chunk in context:
        for raw_line in chunk.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            score = sum(1 for term in query_terms if term in line.lower())
            if score > best_score:
                best_score = score
                best_line = line

    return best_line or context[0].strip()


def retrieve_node(state, retriever):
    try:
        query = state["query"]
        docs = retriever.invoke(query)
        context = [doc.page_content for doc in docs if getattr(doc, "page_content", None)]

        if not context:
            docs = retriever.invoke(query.lower())
            context = [doc.page_content for doc in docs if getattr(doc, "page_content", None)]
    except Exception as exc:
        print("Retriever error:", exc)
        context = []

    return {**state, "context": context}


def generate_node(state):
    context = state["context"]
    if not context:
        return {**state, "response": "I don't know"}

    try:
        llm = get_llm()
        prompt = f"""
        You are a customer support assistant.

        Answer ONLY from the context below.
        If answer is not found, say "I don't know".

        Context:
        {"\n\n".join(context)}

        Question:
        {state["query"]}
        """
        result = llm.invoke(prompt)
        response = str(getattr(result, "content", result)).strip()
    except Exception as exc:
        print("LLM error:", exc)
        return {
            **state,
            "response": fallback_answer(state["query"], context),
        }

    return {**state, "response": response}


def evaluate_node(state):
    try:
        response = state["response"].strip().lower()
        has_context = bool(state["context"])
        answered = bool(response) and "i don't know" not in response and "error" not in response
        confidence = 0.9 if has_context and answered else 0.3
        escalate = settings.ENABLE_HITL and confidence < settings.CONFIDENCE_THRESHOLD
    except Exception as exc:
        print("Evaluation error:", exc)
        confidence = 0.0
        escalate = settings.ENABLE_HITL

    return {**state, "confidence": confidence, "escalate": escalate}


def hitl_node(state):
    try:
        ticket_id = add_to_queue(state["query"])
    except Exception as exc:
        print("HITL error:", exc)
        ticket_id = "ERROR"

    return {
        **state,
        "response": f"Escalated to human. Ticket ID: {ticket_id}",
        "ticket_id": ticket_id,
    }


def build_graph(retriever):
    builder = StateGraph(GraphState)

    builder.add_node("retrieve", lambda state: retrieve_node(state, retriever))
    builder.add_node("generate", generate_node)
    builder.add_node("evaluate", evaluate_node)
    builder.add_node("hitl", hitl_node)

    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", "evaluate")
    builder.add_conditional_edges(
        "evaluate",
        lambda state: "hitl" if state["escalate"] else END,
        {"hitl": "hitl", END: END},
    )
    builder.add_edge("hitl", END)

    return builder.compile()
