# Installation, execution and verification (reviewer instructions)

## Requirements

**Frozen repository:** `IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`. Install the complete directory, not an isolated script.

- Python **3.13.5** tested (64-bit). The code uses standard `csv`, `pathlib`, `hashlib`, `itertools` and other built-in modules.
- NumPy **2.3.5**, SciPy **1.17.0**; exact dependencies are pinned in `requirements.txt`. A virtual environment is recommended.
- No Excel, image packages, proprietary data packages or network calls are used by the analysis scripts. Network is required only once for installing packages unless cached.

### One-time setup

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:
```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Reviewer functional test (does not alter the frozen results)

```bash
python -m unittest discover -s tests -v
```

This standard-library test executes shortened calculations in an isolated temporary directory, without overwriting the published 200,000-permutation CSVs.

### Single-command reproduction

```bash
python run_all.py
```

This runs 15 baseline Spearman tests, 15×200,000 baseline Monte Carlo permutations, 1,500 additional fixed seeded 200,000-permutation sensitivity tests, and **full deterministic reexecution** of all 1,515 streams. Each `run_all.py` execution retains the fixed ID mapping, and a changed mapping is a hard error. All outputs are CSV. Large `B` and complete verification require substantial CPU time. Do not alter seeds or select on p-values.

Optional independent 8-variable extension:
```bash
python run_all.py --include-exploratory8
```

For a faster **functional smoke test only** (NOT the published precision or a replacement for full results):
```bash
python run_all.py --permutations 1000 --repeats 3 --verification sample
```
This overwrites current numeric output CSVs in that copied working directory; use a separate disposable copy and re-run the default publication settings afterward.

### Independent module calls (after input and registry validation)

```bash
python code/01_define_fixed_ids.py
python code/00_build_analysis_input.py
python code/08_reference_statistical_checks.py
python code/02_derived_metrics.py
python code/10_audit_derived_against_SI.py
python code/03_spearman.py --mode manuscript6
python code/04_permutation.py --mode manuscript6 --permutations 200000
python code/05_multiple_testing.py --mode manuscript6
python code/06_seed_sensitivity.py --mode manuscript6 --permutations 200000 --repeats 100
python code/11_export_replacement_TableS5.py
python code/12_validate_fixedseed_reporting.py
python code/07_verify_reproducibility.py --mode manuscript6 --permutations 200000 --repeats 100 --full
python code/09_audit_submission_files.py
```

The standalone modules are organized by algorithm. `run_all.py` invokes them in the correct order and writes CSV metadata and seed registries. `07_verify_reproducibility.py` checks exact `k` and calculated p-values upon rerunning each stored stream. `12_validate_fixedseed_reporting.py` compares the final reported Table S5 snapshot with the fixed-seed recomputation. `08_reference_statistical_checks.py` checks rank and permutation calculations on independent toy data.

### Seed audit details

- Fixed IDs: Q_CA=01, L_Ir=02, j_1.75=03, eta_10=04, C_app=05, b=06, E_dep=07, t_dep=08.
- Main pairs: `01000002`, `01000003`, ..., `05000006` (15 unique sorted pairs).
- Baseline: `SeedSequence(entropy=int(pair_label), spawn_key=(0,))` then `PCG64`.
- Sensitivity: same pair entropy with `spawn_key=(1,)` through `(100,)`.
- `seed_label` e.g. `01000002000` is a padded text label, **not** one scalar integer supplied to NumPy.
- Pair order and random stream generation are fixed; changing seeds legitimately changes Monte Carlo p-values but not measured rho.

### Limits of what is reproduced

The source CSVs are transcribed from the reported Word tables at their printed precision. No original CA time series are integrated, no CV C_app regressions or raw LSV Tafel fits are repeated, and no raw ICP-MS files are available. The computational verification tests statistics derived from reported measurements and should not be described as independent confirmation of those measurements. The potential–time design is fixed and unrestricted permutations do not adjust these covariates. P-values reported for 15 exploratory relationships are nominal/unadjusted; Holm/BH corrections are separate supplementary CSVs.

### Fixed GitHub URL and version identification

The public repository is available at `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`. Cite the public repository URL and record the full Git commit SHA, with the tagged GitHub Release URL when available. The homepage can evolve, but the cited commit identifies the exact reviewed code snapshot. No DOI is requested. See `GITHUB_RELEASE_CHECKLIST.md`.
