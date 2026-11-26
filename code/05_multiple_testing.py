#!/usr/bin/env python3
"""Calculate Holm FWER and Benjamini-Hochberg FDR (EXPLORATORY; manuscript reports nominal p)."""

# INPUT: baseline nominal Monte Carlo p-values.
# ALGORITHM: Holm family-wise and Benjamini–Hochberg false-discovery-rate corrections.
# OUTPUT: a separate EXPLORATORY CSV; these values do not replace manuscript Table S5.

import argparse
from pathlib import Path
from analysis_core import RESULTS,read_csv,write_csv,holm_bh

def calculate(mode='manuscript6',p_path=None,out=None):
 records=read_csv(p_path or RESULTS/mode/'Permutation_Baseline.csv')
 # Corrections use the full family of 15 (main) or 28 (optional) tests.
 holm,bh=holm_bh([float(r['p_permutation']) for r in records])
 rows=[]
 for r,h,q in zip(records,holm,bh):
  rows.append({'variable_x':r['variable_x'],'variable_y':r['variable_y'],
    'p_permutation_nominal':r['p_permutation'],'p_holm_FWER':float(h),'q_BH_FDR':float(q),
    'significant_Holm_0p05':int(h<.05),'significant_BH_0p05':int(q<.05),
    'scope':f'{len(records)}_exploratory_tests'})
 return write_csv(out or RESULTS/mode/'Multiple_Testing_Exploratory.csv',rows)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--mode',choices=['manuscript6','exploratory8'],default='manuscript6')
 a.add_argument('--input',type=Path);a.add_argument('--out',type=Path);x=a.parse_args();print(calculate(x.mode,x.input,x.out))
