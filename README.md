# IrOx/Ti PTL electrodeposition — statistical reproducibility

**Repository:** `IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`  
**Scope:** exactly reproducible 16-condition pairwise Spearman analysis and fixed-seed Monte Carlo permutation tests for the associated IrOx/Ti porous transport layer electrodeposition study.

> **Publication status:** The public GitHub repository URL has been verified: `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`. Record a tagged release and full Git commit SHA to identify the exact analyzed snapshot. No external DOI is required.

## Release integrity and provenance

The v1.0.0 candidate includes `RELEASE_SHA256_MANIFEST.csv` and a standalone Python standard-library verifier. On a freshly downloaded release snapshot, run `python tools/verify_release_snapshot.py --scope all` before any analyses. After running `python run_all.py`, use `--scope source` to verify that code, input tables, and fixed seeds remain byte-identical. The full release/check-out procedure is in `GITHUB_V1_0_0_RELEASE_VERIFICATION.md`. **The GitHub repository is public, but the v1.0.0 Release has not yet been published.**

## Review in three commands

Use Python 3.13 (tested: Python 3.13.5). The numerical dependencies are pinned in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_all.py
```

The first two commands install the pinned runtime and execute **non-destructive functional tests**. The third executes the full publication configuration: 15 pairwise Spearman tests, 200,000 permutation draws per pair, 100 additional seeded numerical repeats per pair and exact replay of **all 1,515 pseudorandom streams**. Computation is CPU-intensive; full checks may require sustained processing.

For only the standalone functional check, `python -m unittest discover -s tests -v` is sufficient. A shortened statistical test is **not** interchangeable with the published B=200,000 results.

## What is reproduced

| Property | Frozen setting |
| --- | --- |
| Analysis unit | One of 16 deposition potential × time conditions (4 × 4) |
| Manuscript variables | `Q_CA`, `L_Ir`, `j_1.75`, uncorrected `eta_10`, `C_app`, uncorrected `b` |
| Pairwise tests | 15 unique unordered pairs (six variables) |
| Fixed IDs | `01`, `02`, `03`, `04`, `05`, `06` (optional exploratory IDs `07`, `08`) |
| Pair label | `XX0000YY` using IDs sorted ascending, e.g. `01000002` |
| RNG | `Generator(PCG64(SeedSequence(entropy=int(pair_label), spawn_key=(r,))))` |
| Baseline and sensitivity | `r=0` baseline; `r=1..100` 100-seed sensitivity |
| Statistic | Pearson correlation of average ranks (`rho_s`) |
| Tail and tolerance | `abs(rho_perm) >= abs(rho_obs) - 1e-12` |
| Monte Carlo p-value | `(k + 1) / (B + 1)`; `B=200000` |
| Multiplicity | Nominal Table S5; Holm/BH are separate exploratory outputs |

**Important distinction:** the longer `XX0000YYRRR` is a display label, **not** an integer passed unchanged as a single RNG seed. The actual initialization pairs integer `XX0000YY` entropy with the independent `spawn_key=(r,)`.

### Scientific scope and limitations

The data files are **transcriptions of final manuscript Table 1 and Supporting Information Tables S1–S3**, not time-series instrument raw data. The scripts verify the summary-table calculations, correspondence of 16 design rows, Spearman rank correlations, numerical permutation p-values and fixed-seed replay. They **do not** integrate original CA current–time recordings, refit original LSV/CV curves, or independently validate the experiment. The 16 observations are a fixed 4 × 4 design; unrestricted pairwise permutation tests do **not** remove shared potential–time influences. Correlations are exploratory, noncausal associations.

## Repository map

```text
IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility/
├── README.md                    # reviewer entry point and scientific limitations
├── PUBLICATION_AUDIT.md         # public data scope, privacy, and reproducibility audit
├── INSTALL_AND_RUN.md          # detailed instructions and optional modes
├── GITHUB_RELEASE_CHECKLIST.md # public GitHub URL, tag, commit SHA, licensing checks
├── requirements.txt           # pinned NumPy / SciPy versions
├── run_all.py                  # single-command full analysis + verification
├── code/                       # independently documented analysis stages (00–12)
│   └── analysis_core.py       # shared input, RNG, correlation and p-value functions
├── config/                     # fixed variable IDs and physical constants
├── data/                       # 16-condition inputs and manuscript/SI reference tables
├── results/                    # precomputed numeric results and verification CSVs
└── tests/                      # isolated standard-library functional smoke test
```

## Result files reviewers should inspect

| Question | CSV artifact |
| --- | --- |
| Are the 15 rho coefficients correct? | `results/manuscript6/Spearman_Rank_Correlations.csv` |
| Do fixed seeds reproduce Table S5? | `results/manuscript6/Permutation_Baseline.csv` |
| Which exact seed produced each p-value? | `results/manuscript6/Seed_Registry_Baseline.csv` |
| How sensitive is p to 100 RNG streams? | `results/manuscript6/Seed_Sensitivity_Summary.csv` |
| Does each stream replay exactly? | `results/manuscript6/Verification_Deterministic_Reexecution.csv` |
| Did the run pass? | `results/manuscript6/Verification_Summary.csv` |
| Do final Table S5 values match? | `results/manuscript6/Verification_FixedSeed_Reported_TableS5.csv` |
| Was the output screened for common personal patterns? | `results/Privacy_Audit.csv` |

**Outputs are CSV-only.** No MATLAB, Excel, figure-rendering library or proprietary platform is necessary. The 8-variable analysis is *optional and separate*: `python run_all.py --include-exploratory8`. Do not substitute its 28-pair results for the six-variable manuscript Table S5.

## Citation and code availability

Cite the verified public GitHub repository URL, `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`. For exact code-version identification, also record the tagged release (`v1.0.0` after publication) and the full commit SHA, preferably with the verified GitHub Release URL `[VERIFIED_GITHUB_RELEASE_URL]`. A repository homepage is a stable entry point but its default branch can change; a recorded commit identifies the calculation snapshot. No DOI is used or requested. Code Availability and the detailed mathematical explanation are provided in separate reviewer-facing Word documents.

**Reuse license:** no LICENSE has been selected. The files are publicly inspectable, but no general reuse rights are granted beyond applicable law until an explicit license is chosen.
