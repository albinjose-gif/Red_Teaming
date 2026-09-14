"""JSON, CSV, and Markdown evidence exports."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .metrics import calculate_metrics


def export_run(run: dict, output_dir: Path, label: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics = calculate_metrics(run)
    payload = {"label": label, "metrics": metrics, **run}
    (output_dir / f"{label}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with (output_dir / f"{label}.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["id", "name", "client", "response", "passed", "disclosed", "refused", "reason"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in run["records"]:
            writer.writerow({"id": record["id"], "name": record["name"], "client": record["client"], "response": record["response"], **record["evaluation"]})
    lines = [f"# PromptShield {label}", "", "> Simulation evidence, not proof of real-model security.", "", "## Metrics", "", f"- ASR: {metrics['asr']:.1f}%", f"- Benign Task Pass Rate: {metrics['benign_pass_rate']:.1f}%", "", "## Cases", ""]
    lines.extend(f"- **{r['id']} {r['name']}**: {'PASS' if r['evaluation']['passed'] else 'FAIL'} - {r['evaluation']['reason']}" for r in run["records"])
    (output_dir / f"{label}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return metrics