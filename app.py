"""Streamlit UI for the PromptShield Security Lab."""
from pathlib import Path

import streamlit as st

from src.hardener import harden_prompt
from src.metrics import calculate_metrics
from src.model_client import HardenedMockClient, VulnerableMockClient
from src.test_runner import load_tests, run_suite

ROOT = Path(__file__).resolve().parent


@st.cache_data
def execute() -> tuple[dict, dict]:
    tests = load_tests(ROOT)
    baseline = (ROOT / "config" / "baseline_prompt.txt").read_text(encoding="utf-8")
    before = run_suite(VulnerableMockClient(), baseline, tests)
    harden_prompt(ROOT)
    hardened = (ROOT / "config" / "hardened_prompt.txt").read_text(encoding="utf-8")
    after = run_suite(HardenedMockClient(), hardened, tests)
    return before, after


st.set_page_config(page_title="PromptShield Security Lab", page_icon="shield", layout="wide")
st.markdown("<style>.block-container{max-width:1200px;padding-top:2rem}.metric-card{padding:1rem;border:1px solid #d9e2ec;border-radius:8px;background:#f7fafc}</style>", unsafe_allow_html=True)
st.title("PromptShield Security Lab")
st.caption("Attack -> Measure -> Analyze -> Harden -> Re-test")
st.warning("Simulation evidence only. Deterministic mock clients do not prove real-model security.")
before, after = execute()
before_metrics, after_metrics = calculate_metrics(before), calculate_metrics(after)

tab_lab, tab_compare, tab_evidence, tab_method = st.tabs(["Red-Team Lab", "Before vs After", "Evidence Explorer", "Methodology"])
with tab_lab:
    st.subheader("Run overview")
    a, b, c = st.columns(3)
    a.metric("Adversarial cases", 16)
    b.metric("Benign utility cases", 8)
    c.metric("Protected marker", "fictional")
    selected = st.selectbox("Case", [r["id"] for r in before["records"]])
    record = next(r for r in before["records"] if r["id"] == selected)
    st.write(f"**{record['name']}** · {record.get('severity', 'utility')}")
    st.json(record["transcript"])
    st.write(record["evaluation"])
with tab_compare:
    st.subheader("Identical test bank comparison")
    left, right = st.columns(2)
    left.metric("Before ASR", f"{before_metrics['asr']:.1f}%")
    left.metric("Before benign pass", f"{before_metrics['benign_pass_rate']:.1f}%")
    right.metric("After ASR", f"{after_metrics['asr']:.1f}%")
    right.metric("After benign pass", f"{after_metrics['benign_pass_rate']:.1f}%")
    st.dataframe({"Metric": ["ASR", "Benign Task Pass Rate"], "Before": [before_metrics["asr"], before_metrics["benign_pass_rate"]], "After": [after_metrics["asr"], after_metrics["benign_pass_rate"]]}, hide_index=True, use_container_width=True)
with tab_evidence:
    st.subheader("Evidence Explorer")
    view = st.radio("Run", ["Before", "After"], horizontal=True)
    run = before if view == "Before" else after
    rows = [{"id": r["id"], "name": r["name"], "passed": r["evaluation"]["passed"], "reason": r["evaluation"]["reason"]} for r in run["records"]]
    st.dataframe(rows, hide_index=True, use_container_width=True)
with tab_method:
    st.subheader("Methodology")
    st.markdown("""**Attack:** 16 adversarial prompts include direct, role-play, multi-turn, reversed, spaced, compact, and base64 marker requests.

**Measure:** The evaluator detects marker variants, refusal phrases, and required benign keywords.

**Analyze:** ASR counts adversarial failures; Benign Task Pass Rate counts utility successes.

**Harden:** The hardened system prompt makes instruction priority and transformation refusal explicit.

**Re-test:** Both clients run against the identical 24-case bank with full transcripts preserved.""")