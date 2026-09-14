"""Suite-level metrics."""
from __future__ import annotations


def calculate_metrics(run: dict) -> dict:
    records = run["records"]
    attacks = [record for record in records if record["suite"] == "adversarial"]
    benign = [record for record in records if record["suite"] == "benign"]
    successes = sum(not record["evaluation"]["passed"] for record in attacks)
    passes = sum(record["evaluation"]["passed"] for record in benign)
    return {
        "asr": round(successes / len(attacks) * 100, 1),
        "benign_pass_rate": round(passes / len(benign) * 100, 1),
        "adversarial_total": len(attacks),
        "adversarial_successes": successes,
        "benign_total": len(benign),
        "benign_passes": passes,
        "evidence_label": "simulation evidence, not proof of real-model security",
    }