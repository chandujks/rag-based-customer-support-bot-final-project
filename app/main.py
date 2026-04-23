from fastapi import FastAPI, HTTPException

from app.bootstrap import initialize_graph
from app.hitl.store import HITL_QUEUE, get_pending, resolve_ticket
from app.schemas import HitlResponseRequest, QueryRequest, QueryResponse

app = FastAPI(title="RAG + Ollama + HITL")

graph = None
startup_error = None


@app.on_event("startup")
def startup_event():
    global graph, startup_error

    print("Starting application...")
    startup_error = None

    try:
        graph = initialize_graph()
        print("Application startup complete")
    except Exception as exc:
        graph = None
        startup_error = str(exc)
        print("Startup failed:", exc)


@app.post("/query", response_model=QueryResponse)
def query_bot(request: QueryRequest):
    global graph

    if graph is None:
        return QueryResponse(
            answer="System not initialized properly",
            confidence=0.0,
            escalated=True,
            ticket_id=None,
        )

    if request.ticket_id:
        ticket = HITL_QUEUE.get(request.ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Invalid ticket ID")

        if ticket["status"] == "resolved":
            return QueryResponse(
                answer=ticket["response"],
                confidence=1.0,
                escalated=False,
                ticket_id=request.ticket_id,
            )

    state = {
        "query": request.query,
        "context": [],
        "response": "",
        "confidence": 0.0,
        "escalate": False,
        "ticket_id": "",
    }

    try:
        result = graph.invoke(state)
        return QueryResponse(
            answer=result.get("response", ""),
            confidence=result.get("confidence", 0.0),
            escalated=result.get("escalate", False),
            ticket_id=result.get("ticket_id", None),
        )
    except Exception as exc:
        print("Runtime error:", exc)
        return QueryResponse(
            answer="System error occurred. Escalating.",
            confidence=0.0,
            escalated=True,
            ticket_id=None,
        )


@app.get("/hitl/pending")
def pending():
    return get_pending()


@app.post("/hitl/respond")
def respond(request: HitlResponseRequest):
    if request.ticket_id not in HITL_QUEUE:
        raise HTTPException(status_code=404, detail="Invalid ticket ID")

    resolve_ticket(request.ticket_id, request.response)
    return {"status": "resolved"}


@app.get("/health")
def health():
    return {"ready": graph is not None, "startup_error": startup_error}
