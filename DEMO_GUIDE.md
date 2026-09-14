# PromptShield Demo Guide

## Five-minute walkthrough

1. Install dependencies with `python -m pip install -r requirements.txt`.
2. Run `python .\run_comparison.py` and observe the baseline and hardened metrics.
3. Open the UI with `streamlit run .\app.py`.
4. In **Red-Team Lab**, inspect a direct disclosure case and a multi-turn case. The transcript includes the system message, every user turn, and the assistant response.
5. In **Before vs After**, compare the identical bank. Baseline is intentionally vulnerable; the hardened mock refuses adversarial requests while answering benign tasks.
6. In **Evidence Explorer**, filter through the per-case pass/fail reason.
7. In **Methodology**, review the evaluator's disclosure and refusal rules.

## What to say during the demo

The vulnerable and hardened clients are deterministic simulations. A lower ASR is evidence that this fixture's hardened behavior blocks this fixture's attacks; it is not proof of real-model security. The benign pass rate exists to show that refusal behavior should not make the assistant useless.

## Files to inspect

- `data/adversarial_tests.json`: 16 attack cases, including single-turn and multi-turn inputs.
- `data/benign_tests.json`: 8 ordinary utility tasks.
- `src/evaluator.py`: marker-variant and refusal detection.
- `results/*.json`: complete preserved transcripts.
- `reports/*.md`: human-readable summaries.