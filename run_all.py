#!/usr/bin/env python3
"""One-command, CSV-only reproducibility package; predefined fixed IDs and seeds.

Main: `python run_all.py`; optional: `python run_all.py --include-exploratory8`.
No randomly re-assigned variable IDs and no seed selection by significance.
"""

# PURPOSE: reproduce the manuscript statistics and audit all outputs in one command.
# EXECUTION: fixed ID -> table pairing -> derived quantities -> rho -> permutations -> checks.
# DEFAULT: six variables, B=200,000, 100 sensitivity streams per pair, full replay.
# NOTE: do not modify seeds to obtain favorable p-values; no instrument raw data are processed.

from __future__ import annotations
import argparse,importlib.util,sys,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from analysis_core import DATA,CONFIG,RESULTS,write_csv,pairs,cols,seed_info,sha
import numpy as np
import scipy

def load(filename):
    path=ROOT/'code'/filename
    spec=importlib.util.spec_from_file_location('step_'+filename.replace('.py','').replace('_','x'),path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

# Record every pair and every child stream before running Monte Carlo calculations.
def manifest(mode,repeats):
    base=[];robust=[]
    for pair in pairs(mode):
        base.append({**pair,**seed_info(pair['pair_seed_label'],0),'mode':mode})
        for rep in range(1,repeats+1):
            robust.append({**pair,**seed_info(pair['pair_seed_label'],rep),'mode':mode})
    write_csv(RESULTS/mode/'Seed_Registry_Baseline.csv',base)
    write_csv(RESULTS/mode/'Seed_Registry_Robustness.csv',robust)

# Archive exact input hashes, library versions, test definitions and seed scheme.
def metadata(mode,B,repeats,batch,verification):
    rows=[('analysis_mode',mode),('input_provenance','Anonymized manuscript/SI printed summary-table values, NOT instrument-level raw signals'),
    ('input_sha256',sha(DATA/'Analysis_Input_16Conditions.csv')),
    ('fixed_id_registry_sha256',sha(CONFIG/'Variable_ID_Registry.csv')),
    ('observations',16),('variables',len(cols(mode))),('pairs',len(pairs(mode))),
    ('B_per_stream',B),('sensitivity_repetitions_per_pair',repeats),
    ('average_rank_tie_method','average'),('rho_statistic','Pearson correlation of ranks'),
    ('tail','abs(rho_perm)>=abs(rho_obs)-1e-12'),
    ('null_permutation','Unrestricted reshuffle of one array of 16 condition-level ranks'),
    ('p_permutation_formula','(k+1)/(B+1)'),
    ('seed_format','XX0000YY: fixed variable IDs 01..08 sorted ascending'),
    ('seed_initialization','NumPy SeedSequence(entropy=int(XX0000YY), spawn_key=(replicate_index,)) -> PCG64'),
    ('baseline_spawn_key',0),('sensitivity_spawn_keys','1..100 (when repeats=100)'),
    ('11_digit_label','XX0000YYRRR is human-readable only; NOT supplied as one integer seed'),
    ('python',platform.python_version()),('numpy',np.__version__),('scipy',scipy.__version__),
    ('batch_size',batch),('verification_level',verification),
    ('methodological_scope','Exploratory pairwise association in fixed 4x4 design; does not adjust potential/time'),
    ('primary_overpotential','uncorrected eta10'),('multiple_testing','nominal in manuscript; Holm and BH in separate exploratory CSV')]
    write_csv(RESULTS/mode/'Analysis_Metadata.csv',[{'setting':k,'value':str(v)} for k,v in rows])

# A non-default B/repeats run is a functional test, not the frozen publication calculation.
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--include-exploratory8',action='store_true',help='Also run separate exploratory 8-variable / 28-pair analysis')
    ap.add_argument('--permutations',type=int,default=200000)
    ap.add_argument('--repeats',type=int,default=100)
    ap.add_argument('--batch',type=int,default=50000)
    ap.add_argument('--verification',choices=['sample','full'],default='full')
    opts=ap.parse_args()
    if min(opts.permutations,opts.repeats,opts.batch)<1 or opts.repeats>100:
        ap.error('B,batch positive; 1 <= repeats <= 100 required')
    load('01_define_fixed_ids.py').create()
    load('00_build_analysis_input.py').build()
    load('08_reference_statistical_checks.py').calculate()
    load('02_derived_metrics.py').calculate(RESULTS/'Derived_Charge_and_Activity.csv')
    load('10_audit_derived_against_SI.py').calculate()
    for mode in ['manuscript6']+(['exploratory8'] if opts.include_exploratory8 else []):
        print('Computing:',mode,flush=True)
        manifest(mode,opts.repeats)
        load('03_spearman.py').calculate(mode)
        # Begin the stochastic calculation only after the deterministic rho CSV exists.
        load('04_permutation.py').calculate(mode,opts.permutations,opts.batch)
        if mode=='manuscript6':
            load('11_export_replacement_TableS5.py').calculate()
            if opts.permutations==200000:load('12_validate_fixedseed_reporting.py').calculate()
        load('05_multiple_testing.py').calculate(mode)
        load('06_seed_sensitivity.py').calculate(mode,opts.permutations,opts.repeats,opts.batch)
        metadata(mode,opts.permutations,opts.repeats,opts.batch,opts.verification)
        print('Verifying:',mode,opts.verification,flush=True)
        # Replay stored RNG streams and independently compare k and calculated p.
        load('07_verify_reproducibility.py').verify(mode,opts.permutations,opts.batch,opts.verification=='full',opts.repeats)
        print('VERIFIED:',mode,flush=True)
    count=load('09_audit_submission_files.py').audit()
    print(f'PASS: all outputs CSV; {count} files hashed and screened for common identifying patterns.',flush=True)

if __name__=='__main__':main()
