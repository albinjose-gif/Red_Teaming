# PromptShield Security Lab

PromptShield is a local educational LLM red-team regression framework. It runs 16 adversarial tests and 8 benign utility tests through deterministic mock clients, preserving every transcript and exporting JSON, CSV, and Markdown evidence.

The workflow is **Attack -> Measure -> Analyze -> Harden -> Re-test**. The protected marker `INTERNAL_PROJECT_CODE = ORCHID-47` is fictional training data and is not a real secret.

## Setup

From PowerShell in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

No API key or network connection is needed after installation. All model behavior is deterministic and local.

## Verification

```powershell
python .\tests\validate_test_bank.py
python .\tests\smoke_test.py
python -m pytest -q
python .\run_comparison.py
```

Expected comparison metrics are baseline ASR **43.8%**, baseline benign pass rate **87.5%**, hardened ASR **0.0%**, and hardened benign pass rate **100.0%**. These are simulation evidence, not proof of real-model security.

## Streamlit UI

```powershell
streamlit run .\app.py
```

The four tabs provide the lab overview and transcript inspector, before/after metrics, an evidence explorer, and methodology. The app creates `results/` and `reports/` automatically and can start from a clean checkout.

## Outputs

`run_comparison.py` writes `results/before.*`, `results/after.*`, and `reports/comparison.json`. JSON keeps full transcripts; CSV is convenient for analysis; Markdown is a readable evidence summary.

## Limitations

This project demonstrates regression mechanics, evaluator design, and prompt hardening with mocks. It does not establish that any real model, deployment, system prompt, or secret is secure. Real evaluation requires representative models, threat modeling, authorization, privacy review, and human analysis.
