"""Structural validation for the exact 24-case bank."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate() -> None:
    adversarial = json.loads((ROOT / "data" / "adversarial_tests.json").read_text(encoding="utf-8"))
    benign = json.loads((ROOT / "data" / "benign_tests.json").read_text(encoding="utf-8"))
    all_tests = adversarial + benign
    ids = [test["id"] for test in all_tests]
    assert len(adversarial) == 16, len(adversarial)
    assert len(benign) == 8, len(benign)
    assert len(ids) == len(set(ids)) == 24
    required_fields = {"id", "suite", "category", "name", "turns", "expected_behavior", "severity", "tags"}
    assert all(required_fields.issubset(test) for test in all_tests)
    assert all(test["suite"] == "adversarial" for test in adversarial)
    assert all(test["suite"] == "benign" for test in benign)
    assert all(test["tags"] and all(isinstance(tag, str) for tag in test["tags"]) for test in all_tests)
    assert all(test["turns"] and all(turn["role"] == "user" and turn["content"] for turn in test["turns"]) for test in all_tests)
    assert all("required_keywords" in test and test["required_keywords"] for test in benign)
    assert all("required_keywords" not in test for test in adversarial)
    print("Test bank valid: 16 adversarial + 8 benign = 24 unique cases")


if __name__ == "__main__":
    validate()