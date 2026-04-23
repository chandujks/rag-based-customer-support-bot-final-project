from app.hitl.store import add_to_queue

def human_intervention(query: str):
    ticket_id = add_to_queue(query)
    return ticket_id