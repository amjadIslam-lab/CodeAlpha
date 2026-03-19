# Task 4 — Making a Chatbot (CodeAlpha)

This is a **retrieval-based** website chatbot that:
- Uses **predefined input patterns** (`data/intents.json`)
- Returns **instant responses** via a Flask API
- Integrates into a simple website UI (`static/`)

## Run locally (Windows / PowerShell)

```bash
cd d:\CodeAlpha\chatbot-task4
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000/`.

## Customize training data

Edit `data/intents.json`:
- Add new `tag`s (intents)
- Add more `patterns` (example user inputs)
- Add more `responses` (what the bot can reply)

