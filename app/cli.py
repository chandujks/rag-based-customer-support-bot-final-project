from app.bootstrap import initialize_graph


def main():
    print("Starting CLI RAG Bot...")

    try:
        graph = initialize_graph()
    except Exception as exc:
        print(f"Startup failed: {exc}")
        return

    print("Ready! Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            print("Bot: Please enter a question.")
            print("-" * 50)
            continue

        state = {
            "query": query,
            "context": [],
            "response": "",
            "confidence": 0.0,
            "escalate": False,
            "ticket_id": "",
        }

        try:
            result = graph.invoke(state)
        except Exception as exc:
            print(f"Bot: System error: {exc}")
            print("-" * 50)
            continue

        print(f"\nBot: {result.get('response', '')}")
        print(f"Confidence: {result.get('confidence', 0.0)}")
        print(f"Escalated: {result.get('escalate', False)}")

        ticket_id = result.get("ticket_id")
        if ticket_id:
            print(f"Ticket ID: {ticket_id}")

        print("-" * 50)


if __name__ == "__main__":
    main()
