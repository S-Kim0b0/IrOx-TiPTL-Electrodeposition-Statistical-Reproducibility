# GitHub publication and v1.0.0 release — verified procedure

## Publication status

As of 2026-11-26, this GitHub repository **exists and is public** at `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`. No `v1.0.0` tag or Release URL has yet been verified. **Do not submit the provisional Word documents as final journal files until all placeholders have been replaced with observed values.**

## 1. Create the repository (one account-owner action)

1. In the authenticated GitHub browser, open https://github.com/new.
2. Owner: `S-Kim0b0` (or select a suitable authorized organization, with the resulting owner reflected in the Code Availability URL).
3. Repository name: `IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`.
4. Set visibility to **Public** only after checking institutional rights, data release permissions, and anonymous peer-review policy. A Private repository will not be usable by anonymous reviewers.
5. **Do not initialize** with a README, `.gitignore`, or license because these are managed by the prepared package; select any license only after obtaining authorization.
6. Select **Create repository**. Copy the actual owner/repository URL from GitHub.

## 2. Upload the frozen files

Unzip the companion archive. The repository root must contain `README.md`, `run_all.py`, `requirements.txt`, `code/`, `config/`, `data/`, `results/`, `tests/`, and `tools/` directly (no duplicate enclosing folder).

A local Git client can publish the code to the **empty** newly created repository:

```bash
git init -b main
git add .
git status --short
git commit -m "Release statistical reproducibility package"
git remote add origin https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility.git
git push -u origin main
```

The remote is a template until GitHub confirms the actual repository. A working GitHub login/token or SSH key is required in the user's Git environment. Do not paste authentication credentials into manuscripts, README files or uploaded logs.

## 3. Verify independently before creating the tag

Use Python 3.13 (tested with 3.13.5) and pinned dependencies from `requirements.txt`. Run from the repository root:

```bash
python -m pip install -r requirements.txt
python tools/verify_release_snapshot.py --scope all
python -m unittest discover -s tests -v
python run_all.py
python tools/verify_release_snapshot.py --scope source
```

`--scope all` checks that the freshly cloned snapshot exactly matches the archived source and results CSVs. `--scope source` checks immutable code, configuration and input after re-running the calculations; dynamic output CSVs may encode environment-specific metadata and need not remain byte-identical. The numerical validation is performed by `run_all.py` and recorded in `results/manuscript6/Verification_Summary.csv` and `results/manuscript6/Verification_Deterministic_Reexecution.csv`. For the full manuscript case the reference configuration is 15 variable pairs, B = 200,000 permutations per pair, 100 sensitivity seeds per pair, and full deterministic replay of 1,515 streams.

The recommended git checkout **must be clean** before tagging. Outputs that are intended to be published should be verified against the committed versions before creating the tag.

## 4. Freeze and publish the v1.0.0 tag

Check the full SHA and working tree first:

```bash
git status --short
git rev-parse HEAD
git tag -a v1.0.0 -m "Fixed-seed manuscript statistical analysis v1.0.0"
git push origin v1.0.0
```

Then on GitHub select **Releases → Draft a new release**, choose existing tag `v1.0.0`, attach the version notes, and publish. If available, enable GitHub's **immutable releases** setting before publication. Verify the actual Release page shows the intended tag and commit; do not move the tag or force-push the referenced commit. These operations cannot be completed within this prepared archive and are **not claimed to have occurred**.

## 5. Reviewer verification after release

```bash
git clone https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility.git
cd IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility
git fetch --tags
git checkout --detach v1.0.0
python tools/verify_release_snapshot.py --scope all --tag v1.0.0
python -m unittest discover -s tests -v
python run_all.py
python tools/verify_release_snapshot.py --scope source --tag v1.0.0
```

`--tag v1.0.0` requires a Git clone with `.git`; when working from a GitHub ZIP, use `--scope all` without `--tag`, then separately verify GitHub's displayed commit.

## 6. Copy verified fields into manuscript and SI

- `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`: real public repository homepage
- `[VERIFIED_V1_0_0_RELEASE_URL]`: real v1.0.0 release page
- `[VERIFIED_FULL_COMMIT_SHA]`: `git rev-parse v1.0.0^{commit}`

Do not use a DOI in this workflow. The repository homepage is a stable access point only while its owner/name remain unchanged; a release tag and a full commit SHA identify the exact analyzed snapshot. Consult GitHub documentation on permanent links and immutable releases.

## Scientific scope

The analysis uses transcribed numerical summary tables from the final manuscript/SI. It reproduces the Spearman statistic and numerical Monte Carlo permutation tests, not the raw instrument-to-table electrochemical data reduction, and it does not remove potential/time confounding in the fixed 4×4 design. Reproducibility of a pseudorandom stream is not proof of independent biological or electrochemical experimental replication.
