"""End-to-end smoke check without Streamlit."""
from pathlib import Path

from src.hardener import harden_prompt
from src.metrics import calculate_metrics
from src.model_client import HardenedMockClient, VulnerableMockClient
from src.test_runner import load_tests, run_suite


def test_expected_metrics() -> None:
    root = Path(__file__).resolve().parents[1]
    tests = load_tests(root)
    before = calculate_metrics(run_suite(VulnerableMockClient(), (root / "config/baseline_prompt.txt").read_text(encoding="utf-8"), tests))
    harden_prompt(root)
    after = calculate_metrics(run_suite(HardenedMockClient(), (root / "config/hardened_prompt.txt").read_text(encoding="utf-8"), tests))
    assert before["asr"] == 43.8
    assert before["benign_pass_rate"] == 87.5
    assert after["asr"] == 0.0
    assert after["benign_pass_rate"] == 100.0