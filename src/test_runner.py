"""Load and execute the PromptShield test bank."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .evaluator import evaluate


def load_tests(project_root: Path) -> list[dict]:
    tests = []
    for filename in ("adversarial_tests.json", "benign_tests.json"):
        with (project_root / "data" / filename).open(encoding="utf-8") as handle:
            tests.extend(json.load(handle))
    return tests


def run_suite(client, system_prompt: str, tests: list[dict]) -> dict:
    records = []
    for test in tests:
        transcript = [{"role": "system", "content": system_prompt}]
        for turn in test["turns"]:
            transcript.append({"role": turn["role"], "content": turn["content"]})
        response = client.respond(test, system_prompt)
        transcript.append({"role": "assistant", "content": response.text})
        result = evaluate(test, response.text)
        records.append({**test, "client": response.client, "response": response.text, "transcript": transcript, "evaluation": result})
    return {"created_at": datetime.now(timezone.utc).isoformat(), "client": client.name, "records": records}