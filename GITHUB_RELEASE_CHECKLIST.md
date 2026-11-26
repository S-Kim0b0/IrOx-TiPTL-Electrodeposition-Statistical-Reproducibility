# GitHub repository publication and fixed URL checklist

**Requested repository:** `IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`.

The verified public repository URL is `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`.

1. **Rights and anonymity:** review institutional permissions to share manuscript-derived numerical tables. Check journal blind-review requirements; do not publish private names, emails, local file paths, instrument raw files not included in this analysis or original manuscript DOCX files.
2. **Licensing:** select a suitable `LICENSE` file after obtaining rights clearance. Do not imply an open-source license before approval.
3. **Create/identify repository:** create the exact public repository name under the correct account. Record its browser URL directly from GitHub. Avoid moving or renaming the repository after article submission to minimize link redirection risks.
4. **Publish files:** upload the *contents* of this prepared repository, preserving its relative paths and unchanged fixed seed registry. Review Git changes and ensure no personal information or unintended files were added.
5. **Independent verification:** run `python -m pip install -r requirements.txt`, `python -m unittest discover -s tests -v`, then `python run_all.py`. Inspect verification CSVs, reported Table S5 agreement and SHA-256 manifest.
6. **Freeze the computational snapshot:** tag the validated exact commit (suggested `v1.0.0`) and publish a GitHub Release. Record the actual release URL and full commit SHA. Do not change a published tag or force-push the manuscript-referenced commit.
7. **Code Availability:** replace `https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`, `[VERIFIED_GITHUB_RELEASE_URL]` and `[VERIFIED_COMMIT_SHA]` in the separate Word wording document with observed GitHub values. Verify the URL works when not signed into the owner's account.
8. **After publication:** for changes affecting numbers or methods, publish a new release (`v1.0.1` etc.) and document changes. Keep the originally cited release and commit available.

## Why both repository URL and commit SHA?

The repository homepage is a useful, memorable fixed location while the repository owner/name remain unchanged. It does **not**, by itself, freeze the files on the default branch. A full commit SHA (and a release referencing it) specifies the numerical code snapshot reviewed for the paper. No DOI is required in this workflow.

## Official GitHub guidance

- Repository releases: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
- Permanent links to GitHub content: https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files

**Current status:** public repository verified; commit SHA and v1.0.0 Release URL must be read back after upload and release. No release has been issued.


**Additional frozen-v1.0.0 verification:** See `GITHUB_V1_0_0_RELEASE_VERIFICATION.md` and use `python tools/verify_release_snapshot.py --scope all` on a fresh clone before running computations.
