"""Run identical before/after deterministic comparisons and export evidence."""
from pathlib import Path
import json

from src.hardener import harden_prompt
from src.model_client import HardenedMockClient, VulnerableMockClient
from src.report_generator import export_run
from src.test_runner import load_tests, run_suite


def main() -> None:
    root = Path(__file__).resolve().parent
    tests = load_tests(root)
    baseline = (root / "config" / "baseline_prompt.txt").read_text(encoding="utf-8")
    before = run_suite(VulnerableMockClient(), baseline, tests)
    before_metrics = export_run(before, root / "results", "before")
    hardened_path = harden_prompt(root)
    after = run_suite(HardenedMockClient(), hardened_path.read_text(encoding="utf-8"), tests)
    after_metrics = export_run(after, root / "results", "after")
    comparison = {"before": before_metrics, "after": after_metrics, "identical_test_ids": [r["id"] for r in before["records"]] == [r["id"] for r in after["records"]]}
    (root / "reports").mkdir(exist_ok=True)
    (root / "reports" / "comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    print("PromptShield Security Lab - simulation evidence")
    print(f"Before: ASR {before_metrics['asr']:.1f}% | Benign Task Pass Rate {before_metrics['benign_pass_rate']:.1f}%")
    print(f"After:  ASR {after_metrics['asr']:.1f}% | Benign Task Pass Rate {after_metrics['benign_pass_rate']:.1f}%")
    print(f"Identical test IDs: {comparison['identical_test_ids']}")
    print("Evidence is simulation evidence, not proof of real-model security.")


if __name__ == "__main__":
    main()