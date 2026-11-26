"""Standalone standard-library checks; never mutate the publication snapshot."""
from __future__ import annotations
import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from analysis_core import read_ids, pairs, rng_for, holm_bh  # noqa: E402


class ReviewerChecks(unittest.TestCase):
    def test_frozen_variable_numbering(self):
        # Reject changed IDs: no researcher can optimize seeds after seeing p-values.
        mapping = read_ids()
        self.assertEqual(list(mapping.values()), list(range(1, 9)))
        self.assertEqual(pairs("manuscript6")[0]["pair_seed_label"], "01000002")

    def test_same_stream_replays(self):
        # The same pair entropy and spawn key must reproduce the same integer stream.
        a = rng_for("01000002", 0).integers(0, 2**31, size=100)
        b = rng_for("01000002", 0).integers(0, 2**31, size=100)
        self.assertTrue((a == b).all())

    def test_holm_and_bh_bounded(self):
        # Statistical adjustments should remain in [0, 1].
        a, b = holm_bh([0.001, 0.02, 0.5])
        self.assertTrue(((a >= 0) & (a <= 1)).all())
        self.assertTrue(((b >= 0) & (b <= 1)).all())

    def test_end_to_end_in_temporary_copy(self):
        # Functional smoke test on a temporary copy; it cannot overwrite 200k results.
        with tempfile.TemporaryDirectory(prefix="irox_reviewer_test_") as tmp:
            target = Path(tmp) / "repo"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("results", "__pycache__", ".venv", "*.pyc"))
            result = subprocess.run(
                [sys.executable, "run_all.py", "--permutations", "1000", "--repeats", "2", "--verification", "sample"],
                cwd=target, capture_output=True, text=True, timeout=180,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + "\n" + result.stderr)
            path = target / "results" / "manuscript6" / "Permutation_Baseline.csv"
            with path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 15)
            self.assertTrue(all(int(r["B"]) == 1000 for r in rows))
            self.assertTrue((target / "results" / "manuscript6" / "Verification_Summary.csv").exists())


if __name__ == "__main__":
    unittest.main()
