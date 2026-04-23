import uuid

HITL_QUEUE = {}

def add_to_queue(query):
    ticket_id = str(uuid.uuid4())

    HITL_QUEUE[ticket_id] = {
        "query": query,
        "status": "pending",
        "response": None
    }

    return ticket_id

def get_pending():
    return {k: v for k, v in HITL_QUEUE.items() if v["status"] == "pending"}

def resolve_ticket(ticket_id, response):
    if ticket_id in HITL_QUEUE:
        HITL_QUEUE[ticket_id]["status"] = "resolved"
        HITL_QUEUE[ticket_id]["response"] = response