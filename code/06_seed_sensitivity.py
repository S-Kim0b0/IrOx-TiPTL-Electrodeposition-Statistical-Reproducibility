#!/usr/bin/env python3
"""Compute independently seeded 001..100 Monte Carlo tests for each variable pair."""

# INPUT: observed rho, baseline classifications, fixed per-pair entropy.
# ALGORITHM: 100 independently initialized child streams via spawn_key=(1,) … (100,).
# OUTPUT: individual p-values and a per-pair numerical sensitivity summary.

import argparse
from pathlib import Path
from analysis_core import (RESULTS,read_input,pairs,read_csv,write_csv,rng_for,test_one,seed_info)
import numpy as np

def calculate(mode='manuscript6',B=200000,repeats=100,batch=50000,registry=None,out=None,summary=None,rho_csv=None):
 _,keys,matrix=read_input(mode)
 ref=read_csv(rho_csv or RESULTS/mode/'Spearman_Rank_Correlations.csv')
 base={(r['variable_x'],r['variable_y']):r for r in read_csv(RESULTS/mode/'Permutation_Baseline.csv')}
 lookup={(r['variable_x'],r['variable_y']):r for r in pairs(mode,registry)}
 runs=[];aggregated=[]
 for s in ref:
  x=s['variable_x'];y=s['variable_y'];p=lookup[(x,y)];i=keys.index(x);j=keys.index(y)
  pvals=[];hitlist=[]
  # These 100 repeats are Monte Carlo numerical replicates, NOT new electrodes.
  for rep in range(1,repeats+1):
   hits,pvalue=test_one(matrix[:,i],matrix[:,j],float(s['rho_spearman']),rng_for(p['pair_seed_label'],rep),B,batch)
   record=seed_info(p['pair_seed_label'],rep)
   runs.append({'variable_x':x,'variable_y':y,'pair_seed_label':p['pair_seed_label'],
     'replicate_index':rep,'display_seed_label':record['seed_label'],
     'pair_seed_entropy':record['pair_seed_entropy'],'spawn_key_index':rep,
     'B':B,'extreme_count_k':hits,'rho_observed':s['rho_spearman'],
     'p_permutation':pvalue,'nominal_p_below_0p05':int(pvalue<.05)})
   pvals.append(pvalue);hitlist.append(hits)
  z=np.array(pvals)
  # Distinguish the fraction significant from agreement with the baseline classification.
  baseline_significant = float(base[(x,y)]['p_permutation']) < 0.05
  aggregated.append({'variable_x':x,'variable_y':y,'pair_seed_label':p['pair_seed_label'],
    'replications':repeats,'B_per_replication':B,'p_min':float(z.min()),'p_median':float(np.median(z)),
    'p_mean':float(z.mean()),'p_max':float(z.max()),'p_sample_sd':float(np.std(z,ddof=1)) if repeats>1 else 0,
    'significant_count':int(np.count_nonzero(z<.05)),
    'nonsignificant_count':int(np.count_nonzero(z>=.05)),
    'significant_fraction':float(np.mean(z<.05)),
    'baseline_significant':int(baseline_significant),
    'classification_agreement_fraction':float(np.mean((z<.05)==baseline_significant))})
 out=out or RESULTS/mode/'Seed_Sensitivity_All_Runs.csv'
 summary=summary or RESULTS/mode/'Seed_Sensitivity_Summary.csv'
 write_csv(out,runs);write_csv(summary,aggregated)
 return out,summary
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--mode',choices=['manuscript6','exploratory8'],default='manuscript6')
 a.add_argument('--permutations',type=int,default=200000);a.add_argument('--repeats',type=int,default=100)
 a.add_argument('--batch',type=int,default=50000);a.add_argument('--registry',type=Path)
 a.add_argument('--out',type=Path);a.add_argument('--summary',type=Path);a.add_argument('--rho-csv',type=Path)
 x=a.parse_args();print(calculate(x.mode,x.permutations,x.repeats,x.batch,x.registry,x.out,x.summary,x.rho_csv))
