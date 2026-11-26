#!/usr/bin/env python3
"""Build 16-condition analysis input from anonymized final manuscript/SI table CSVs.

The original Word documents are intentionally NOT required or redistributed.
Input-data conflicts fail loudly; no missing record is ever synthesized.
"""

# SOURCE INPUT: final manuscript Table 1 and SI Tables S1–S3 transcribed to CSV.
# ALGORITHM: match all sixteen deposition conditions by condition_id, never by row position.
# OUTPUT: data/Analysis_Input_16Conditions.csv; mismatches raise an exception.

from pathlib import Path
import argparse,csv
from analysis_core import DATA,read_csv,write_csv

SOURCE_FILES=['Source_Manuscript_Table1.csv','Source_SI_TableS1.csv','Source_SI_TableS2.csv','Source_SI_TableS3.csv']
OUTPUT_COLS=['condition_id','deposition_potential_V_AgAgCl','deposition_time_min',
 'Q_CA_mC','L_Ir_mg_cm2','j_1p75_mA_cm2','eta_10_raw_mV','C_app_mF_cm2','tafel_b_raw_mV_dec',
 'eta_10_iR_mV','tafel_b_iR_mV_dec']

def build(output=None,verify_existing=True):
 # Read the four source tables independently to preserve provenance.
 sources=[read_csv(DATA/f) for f in SOURCE_FILES]
 indexes=[]
 for source in sources:
  mapping={r['condition_id']:r for r in source}
  if len(mapping)!=16:raise ValueError('Exactly 16 unique conditions required in each source table')
  indexes.append(mapping)
 if not all(set(indexes[0])==set(m) for m in indexes):raise ValueError('Missing/mismatched condition IDs between source tables')
 items=[]
 # Join by a unique condition identifier; sort for deterministic CSV order.
 for cond in sorted(indexes[0],key=lambda c:(int(c.split('_T')[-1]),float(c[1:5]))):
  value={}
  for source in indexes:
   for k,v in source[cond].items():
    if k=='electrode':continue
    if k in value and value[k]!=v:
     raise ValueError(f'Conflicting source column for {cond}/{k}')
    value[k]=v
  row={k:value[k] for k in OUTPUT_COLS}
  items.append(row)
 path=Path(output or DATA/'Analysis_Input_16Conditions.csv')
 if path.exists() and verify_existing:
  stored=read_csv(path)
  if stored!=items:raise ValueError('Existing analysis input differs from source table values; refusing silent overwrite')
 else: write_csv(path,items,OUTPUT_COLS)
 return path
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path);ap.add_argument('--replace-input',action='store_true')
 a=ap.parse_args();print(build(a.out,not a.replace_input))
