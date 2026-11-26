# v1.0.0 — Manuscript fixed-seed statistical reproducibility

**Publication status: DRAFT. Not a published GitHub Release.**

This code release reproduces the 6-variable, 16-condition Spearman correlation analysis and the 15 two-sided Monte Carlo permutation tests reported in manuscript Supporting Information Table S5. Numerical settings: B=200,000; fixed variable IDs 01–06; deterministic SeedSequence/PCG64 per-pair streams; 100-seed sensitivity and 1,515-stream exact replay.

Contents: documented Python code, anonymized summary-table CSV input, fixed seed registry, archived numerical results, independent functional tests and SHA-256 release manifest.

Reviewers may run `python tools/verify_release_snapshot.py --scope all` and `python -m unittest discover -s tests -v`, followed by `python run_all.py` for full numerical reproduction.

Scope limit: original instrument CA/LSV/CV/ICP-MS raw records are not included. These scripts do not adjust pairwise correlations for the common deposition potential/time.
