#!/usr/bin/env python3
"""Audit each derived-value formula against the submitted (rounded) SI tables.

Differences are expected from source display precision; tolerances explicitly
account for rounding and are NOT uncertainty estimates.
"""

# INPUT: calculated derived metrics and printed SI Tables S2–S3.
# ALGORITHM: numerical comparisons with stated display-rounding tolerances.
# OUTPUT: 80 metric checks; display tolerance is not experimental uncertainty.

from analysis_core import DATA,RESULTS,read_csv,write_csv

SCHEMES=[
 ('Q_Ir_2e_mC_calculated','Q_Ir_2e_mC_reported',0.003,'Table S2: QIr,2e; mg/cm2 displayed to 5 decimals'),
 ('phi_2e_pct_calculated','phi_2e_pct_reported',0.015,'Table S2: percentage displayed to 2 decimals'),
 ('current_density_per_charge_mA_cm2_C1','j1p75_per_Q_reported',0.10,'Table S2: current per charge displayed to 1 decimal'),
 ('charge_per_mass_mC_mg1','Q_per_Ir_reported',0.20,'Table S2: charge per mass displayed to 1 decimal'),
]
def calculate():
 derived={r['condition_id']:r for r in read_csv(RESULTS/'Derived_Charge_and_Activity.csv')}
 s2={r['condition_id']:r for r in read_csv(DATA/'Source_SI_TableS2.csv')}
 s3={r['condition_id']:r for r in read_csv(DATA/'Source_SI_TableS3.csv')}
 if not (set(derived)==set(s2)==set(s3)):raise AssertionError('Mismatch between derivation and SI tables')
 out=[]
 for c in sorted(derived):
  for key,reference,tol,note in SCHEMES:
   value=float(derived[c][key]);source=float(s2[c][reference]);delta=value-source
   out.append({'condition_id':c,'metric':key,'calculated':value,'SI_reported':source,
     'difference':delta,'display_rounding_tolerance':tol,'passes_rounding_audit':int(abs(delta)<=tol),
     'note':note})
  value=float(derived[c]['mass_activity_A_gIr_calculated']);source=float(s3[c]['mass_activity_reported_A_gIr'])
  out.append({'condition_id':c,'metric':'mass_activity_A_gIr_calculated','calculated':value,
    'SI_reported':source,'difference':value-source,'display_rounding_tolerance':0.25,
    'passes_rounding_audit':int(abs(value-source)<=0.25),'note':'Table S3: selected electrode mass activity; rounded displayed inputs'})
 if not all(int(x['passes_rounding_audit']) for x in out):
  write_csv(RESULTS/'Verification_Derived_Values_Against_SI.csv',out)
  raise AssertionError('Derived calculation fails reported SI rounding check')
 return write_csv(RESULTS/'Verification_Derived_Values_Against_SI.csv',out)
if __name__=='__main__':print(calculate())
