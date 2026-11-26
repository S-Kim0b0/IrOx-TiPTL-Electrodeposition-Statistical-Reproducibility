#!/usr/bin/env python3
"""Compute ONLY baseline Monte Carlo permutation p-values for all pairs."""

# INPUT: frozen 16-condition data, rho CSV, and fixed pair-seed registry.
# NULL: unrestricted condition-level re-pairing of one ranked variable.
# OUTPUT: k and p=(k+1)/(B+1) for 200,000 two-sided draws per pair.

import argparse
from pathlib import Path
from analysis_core import (RESULTS,read_input,pairs,read_csv,write_csv,rng_for,test_one,seed_info)

def calculate(mode='manuscript6',B=200000,batch=50000,registry=None,out=None,rho_csv=None):
 _,keys,matrix=read_input(mode)
 src=read_csv(rho_csv or RESULTS/mode/'Spearman_Rank_Correlations.csv')
 seed_rows=pairs(mode,registry);mapping={(x['variable_x'],x['variable_y']):x for x in seed_rows}
 rows=[]
 for r in src:
  k=(r['variable_x'],r['variable_y']);p=mapping[k];i=keys.index(k[0]);j=keys.index(k[1])
  # Reinitialize each pair with its registered entropy and baseline spawn_key=(0,).
  hits,pvalue=test_one(matrix[:,i],matrix[:,j],float(r['rho_spearman']),rng_for(p['pair_seed_label'],0),B,batch)
  rows.append({**r,**seed_info(p['pair_seed_label'],0),'B':B,'extreme_count_k':hits,
   'p_permutation':pvalue,'nominal_p_below_0p05':int(pvalue<0.05),
   'permutation_definition':'abs(rho_perm)>=abs(rho_obs)-1e-12','p_definition':'(k+1)/(B+1)'})
 return write_csv(out or RESULTS/mode/'Permutation_Baseline.csv',rows)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--mode',choices=['manuscript6','exploratory8'],default='manuscript6')
 a.add_argument('--permutations',type=int,default=200000);a.add_argument('--batch',type=int,default=50000)
 a.add_argument('--registry',type=Path);a.add_argument('--out',type=Path);a.add_argument('--rho-csv',type=Path);x=a.parse_args()
 print(calculate(x.mode,x.permutations,x.batch,x.registry,x.out,x.rho_csv))
