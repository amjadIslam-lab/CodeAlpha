from chatbot.engine import ChatbotEngine


def main() -> None:
    e = ChatbotEngine.from_json_file("data/intents.json")
    for msg in ["hello", "what are your opening hours", "pricing", "contact support"]:
        reply, meta = e.reply(msg)
        print(">", msg)
        print(reply)
        print(meta)
        print()


if __name__ == "__main__":
    main()

