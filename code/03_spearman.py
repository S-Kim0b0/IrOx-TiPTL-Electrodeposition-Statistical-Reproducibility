#!/usr/bin/env python3
"""Compute ONLY deterministic Spearman rho and scipy approximate p values."""

# INPUT: validated 16-condition paired vectors.
# EQUATION: rho_s = PearsonCorr(average_rank(X), average_rank(Y)).
# OUTPUT: observed rho and SciPy approximate p; no RNG is used.

import argparse
from pathlib import Path
from analysis_core import stats_for_pairs,write_csv,RESULTS

def calculate(mode='manuscript6',registry=None,out=None):
 # Spearman rho depends only on input ranks; random seeds cannot change it.
 rec=stats_for_pairs(mode,registry)
 return write_csv(out or RESULTS/mode/'Spearman_Rank_Correlations.csv',rec)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--mode',choices=['manuscript6','exploratory8'],default='manuscript6')
 a.add_argument('--registry',type=Path);a.add_argument('--out',type=Path);args=a.parse_args()
 print(calculate(args.mode,args.registry,args.out))
