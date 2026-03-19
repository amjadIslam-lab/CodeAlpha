import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_from_directory

from chatbot.engine import ChatbotEngine


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    intents_path = os.path.join(os.path.dirname(__file__), "data", "intents.json")
    engine = ChatbotEngine.from_json_file(intents_path)

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/health")
    def health():
        return jsonify(
            {
                "ok": True,
                "time": datetime.now(timezone.utc).isoformat(),
                "intents": engine.intent_count,
            }
        )

    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        message = (payload.get("message") or "").strip()
        if not message:
            return jsonify({"reply": "Please type a message so I can help."}), 400

        reply, meta = engine.reply(message)
        return jsonify({"reply": reply, "meta": meta})

    return app


app = create_app()

if __name__ == "__main__":
    # Local dev defaults: http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=True)

