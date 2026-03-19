from __future__ import annotations

import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _seq_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


@dataclass(frozen=True)
class Intent:
    tag: str
    patterns: list[str]
    responses: list[str]


class ChatbotEngine:
    """
    Retrieval-based chatbot:
    - Matches user message against predefined patterns
    - Returns a response from the best intent (if above threshold)
    """

    def __init__(self, intents: list[Intent], threshold: float = 0.55):
        self._intents = intents
        self._threshold = threshold

        self._pattern_index: list[tuple[Intent, str, set[str]]] = []
        for intent in intents:
            for p in intent.patterns:
                self._pattern_index.append((intent, p, set(_tokens(p))))

    @property
    def intent_count(self) -> int:
        return len(self._intents)

    @classmethod
    def from_json_file(cls, path: str | Path) -> ChatbotEngine:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        intents_raw = raw.get("intents")
        if not isinstance(intents_raw, list):
            raise ValueError("Invalid intents.json: missing `intents` list")

        intents: list[Intent] = []
        for item in intents_raw:
            tag = str(item.get("tag", "")).strip()
            patterns = item.get("patterns") or []
            responses = item.get("responses") or []
            if not tag or not isinstance(patterns, list) or not isinstance(responses, list):
                continue
            patterns_s = [str(p).strip() for p in patterns if str(p).strip()]
            responses_s = [str(r).strip() for r in responses if str(r).strip()]
            if patterns_s and responses_s:
                intents.append(Intent(tag=tag, patterns=patterns_s, responses=responses_s))

        if not intents:
            raise ValueError("No valid intents found in intents.json")

        return cls(intents=intents)

    def reply(self, message: str) -> tuple[str, dict[str, Any]]:
        msg = message.strip()
        msg_l = msg.lower()
        msg_tokens = set(_tokens(msg_l))

        best = None  # (score, intent, pattern)

        for intent, pattern, pattern_tokens in self._pattern_index:
            # Blend token overlap + fuzzy ratio for robustness.
            score = (0.65 * _jaccard(msg_tokens, pattern_tokens)) + (0.35 * _seq_ratio(msg_l, pattern.lower()))
            if best is None or score > best[0]:
                best = (score, intent, pattern)

        if not best or best[0] < self._threshold:
            return (
                "I’m not 100% sure I understood. Try asking about pricing, hours, support, or how to contact us.",
                {"matched": False, "score": best[0] if best else None},
            )

        score, intent, pattern = best
        response = intent.responses[hash(msg_l) % len(intent.responses)]
        return (
            response,
            {"matched": True, "tag": intent.tag, "pattern": pattern, "score": round(score, 3)},
        )

