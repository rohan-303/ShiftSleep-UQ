# ShiftSleep-UQ Step 1 Report

## 1. Status

COMPLETE

## 2. Workspace

* project path: `C:\Users\rohan\ShiftSleep-UQ`
* git status: see Section 13; repository was cloned empty from the specified remote and populated locally.
* branch: `main`
* commit hash if applicable: NONE (no commit made; push explicitly not performed).

## 3. Environment

* OS: Microsoft Windows 11 Home, build family 10.0.26200, detected from live host.
* Python: 3.11.15 (`python` executable).
* package manager(s): pip 26.1.2, uv 0.12.1; conda NOT_AVAILABLE.
* CPU: AMD64 Family 23 Model 96 Stepping 1, detected via Python; detailed model string NOT_AVAILABLE from the probe.
* RAM: 32,175 MB total physical memory reported by `systeminfo`; 4,977 MB available at audit time.
* GPU: NVIDIA GeForce RTX 3060 Laptop GPU, 6,144 MiB total; 1,435 MiB in use at audit time.
* CUDA: NVIDIA driver 566.07 reported CUDA 12.7; CUDA runtime availability through PyTorch not tested because PyTorch is absent.
* PyTorch: NOT_AVAILABLE (`No module named 'torch'`).

## 4. Files Created

`README.md`, `LICENSE`, `.gitignore`, `pyproject.toml`, `AGENTS.md`, `data/README.md`, `docs/research_spec.md`, `docs/benchmark_spec.md`, `docs/evaluation_protocol.md`, `docs/leakage_policy.md`, `docs/hypothesis_registry.md`, `docs/dataset_registry.md`, `docs/reproducibility.md`, `docs/decisions.md`, `src/shiftsleep_uq/__init__.py`, `tests/test_import.py`, `reports/STEP_01_PROJECT_BOOTSTRAP_REPORT.md`.

## 5. Files Modified

NONE. The remote repository was empty and the local target directory did not exist before cloning.

## 6. Scientific Protocol Established

Primary objective: test whether multimodal sleep-staging uncertainty remains reliable under subject, cross-dataset, missing-modality, and compound shift.

RQ1-RQ6 were formally documented in `docs/research_spec.md`. H1-H7 were registered as UNTESTED in `docs/hypothesis_registry.md`; H7 is explicitly exploratory. Benchmark levels S0-S4, calibration regimes A/B/C, leakage protections, and the subject as preferred statistical unit were documented. PSG epochs from one participant are explicitly treated as correlated rather than independent observations.

## 7. Validation Performed

* `pwd`: returned `/c/Users/rohan`.
* Workspace inspection: current home directory was not a Git repository; `C:\Users\rohan\ShiftSleep-UQ` was absent; existing `AlignmentDelta` and `SHIFT-ICD` repositories were identified and not modified.
* `git clone https://github.com/rohan-303/ShiftSleep-UQ.git ShiftSleep-UQ`: succeeded; Git reported the remote repository was empty.
* `python --version`: `Python 3.11.15`.
* `python -m pip --version`: pip 26.1.2.
* `uv --version`: uv 0.12.1.
* `conda --version`: command not found / NOT_AVAILABLE.
* `git --version`: git 2.47.1.windows.1.
* `ruff --version`: command not found / NOT_AVAILABLE.
* `pytest --version`: pytest 9.1.1.
* `systeminfo` probe: Windows 11 Home; 32,175 MB total physical memory; 4,977 MB available.
* `nvidia-smi`: succeeded; RTX 3060 Laptop GPU, driver 566.07, CUDA 12.7, 6,144 MiB total, 1,435 MiB used.
* PyTorch import probe: failed with `No module named 'torch'`; recorded as absent, not installed during this step.
* `python -m compileall -q src tests`: exit 0.
* `pytest -q`: exit 0; `1 passed in 0.05s`.
* `PYTHONPATH=src python -c 'import shiftsleep_uq; print(shiftsleep_uq.__version__)'`: exit 0; printed `0.1.0`.
* TOML parse with Python `tomllib`: succeeded; project name `shiftsleep-uq`.
* Asset scan for model/data archive extensions (`.pt`, `.pth`, `.ckpt`, `.h5`, `.edf`, `.zip`, `.tar`, `.gz`): no matches.
* Git diff/status verification: completed below; all created files are untracked because no commit was made.

## 8. Problems / Blockers

* PyTorch and ruff are not installed. This is intentional for a documentation-only bootstrap; no heavy ML dependency was installed.
* Exact CPU model string was not available from the straightforward Python probe.
* Dataset/channel/annotation/licensing facts remain unresolved and are marked UNVERIFIED/TODO; this is an expected Step 2 gate.

## 9. Decisions Made

D001 through D007 are recorded in `docs/decisions.md`: benchmark-first; reliability-first under compound shift; candidate EEG/EOG/EMG families; provisional five-class harmonization; target-free calibration as main setting; oracle calibration only as upper bound; conditional later method.

## 10. Assumptions

* The empty remote repository specified by the user is the intended dedicated project repository.
* `C:\Users\rohan\ShiftSleep-UQ` is the appropriate local clone path.
* MIT licensing is suitable for the newly created scaffold; future dataset terms remain separate and unverified.
* The date `2026-09-01` is the local date observed during the audit.
* No final scientific benchmark specification can be frozen before the source audit.

## 11. What Was Explicitly NOT Done

* no dataset downloaded
* no model trained
* no test results invented
* no dataset metadata fabricated
* no target-domain labels used
* no push performed

## 12. Recommended Step 2

Perform a source-verified literature, dataset, licensing, annotation, duplicate/overlap, and EEG/EOG/EMG channel-harmonization audit before implementing preprocessing or split code. Record authoritative URLs, versions, access terms, label semantics, subject identifiers, and unresolved compatibility gates; do not download data until the acquisition decision is documented.

## 13. Exact Git Diff Summary

* `git status --short --untracked-files=all`:
  ```text
  ?? .gitignore
  ?? AGENTS.md
  ?? LICENSE
  ?? README.md
  ?? data/README.md
  ?? docs/benchmark_spec.md
  ?? docs/dataset_registry.md
  ?? docs/decisions.md
  ?? docs/evaluation_protocol.md
  ?? docs/hypothesis_registry.md
  ?? docs/leakage_policy.md
  ?? docs/reproducibility.md
  ?? docs/research_spec.md
  ?? pyproject.toml
  ?? reports/STEP_01_PROJECT_BOOTSTRAP_REPORT.md
  ?? src/shiftsleep_uq/__init__.py
  ?? tests/test_import.py
  ```
* `git diff --stat`: empty, because the repository has no prior commit and all files are untracked. The exact untracked file list above is the applicable diff summary.
