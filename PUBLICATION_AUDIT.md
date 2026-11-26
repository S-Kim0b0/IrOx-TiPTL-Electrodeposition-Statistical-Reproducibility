# Prepublication static and numerical audit

Repository: `S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility`  
Verified repository URL: https://github.com/S-Kim0b0/IrOx-TiPTL-Electrodeposition-Statistical-Reproducibility

## Distribution boundaries
- Only UTF-8 source text, Python modules, CSV numeric data and reproducibility documentation are included.
- No source DOCX/PDF/PPTX/figures, local user path, password, access token, e-mail or telephone number is distributed.
- Numerically shaped, 11-digit seed labels can resemble telephone numbers and are *not* personal identifiers.
- Included data are transcriptions of manuscript/SI summary tables, not raw CA, CV, LSV, EIS or ICP-MS instrument files.
- The optional 8-variable/28-pair analysis is separate from the six-variable/15-pair manuscript results.

## Reproducibility scope
- Fixed IDs: 01–06 (optional 07–08). Fixed pair label `XX0000YY`.
- `SeedSequence(entropy=int(pair_label), spawn_key=(r,))`, `PCG64`; `r=0` baseline, `r=1..100` sensitivity.
- B=200000; two-sided `abs(rho_perm)>=abs(rho_obs)-1e-12`; p=`(k+1)/(B+1)`.
- Independent, same-environment prior full replay recorded 1,515/1,515 primary streams and 2,828/2,828 exploratory streams.
- These checks establish deterministic numerical replay, not inferential validity of unrestricted permutations under common deposition potential/time effects.

## Privacy and dependency limitations
- Automated pattern checks are not a guarantee that research datasets are completely anonymous.
- No LICENSE has been selected. The owner should explicitly select a reuse license if third-party redistribution is intended.
- SHA-256 verification attests exact file bytes but not correctness of the scientific model; original experimental replicate measurements are not included.
- The v1.0.0 tag and GitHub Release remain unissued until explicitly published and verified.
