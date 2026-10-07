from engine.bot_engine import InternSupportBot

def test():
    bot = InternSupportBot()

    test_queries = [
        "How do I submit my GitHub repository for weekly tasks?",
        "What are the requirements to get my completion certificate?",
        "My local server crashed and I need a refund for my college dorm fees"
    ]

    print("=" * 65)
    print("      TESTING INTERN SUPPORT BOT RETRIEVAL & ESCALATION")
    print("=" * 65)

    for q in test_queries:
        print(f"\nUser Query: '{q}'")
        res = bot.answer_query(q)
        print(f"Confidence : {int(res['confidence'] * 100)}%")
        print(f"Escalated? : {res['is_escalated']}")
        print(f"Bot Answer :\n{res['answer']}")
        if res['ticket']:
            print(f"Generated Ticket: {res['ticket']}")
        print("-" * 65)

if __name__ == "__main__":
    test()