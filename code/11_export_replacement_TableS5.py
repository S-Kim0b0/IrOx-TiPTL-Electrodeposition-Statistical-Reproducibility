#!/usr/bin/env python3
"""Export a seed-consistent CSV replacement for final SI Table S5, without editing Word files."""

# INPUT: final baseline permutation CSV and historical SI reference labels.
# ALGORITHM: map reported variable names to frozen column IDs; format p to 6 decimals.
# OUTPUT: candidate SI Table S5 values and an edit-consistency checklist.

from analysis_core import ROOT,DATA,RESULTS,read_csv,write_csv
NAME_MAP={'QCA':'Q_CA_mC','LIr':'L_Ir_mg_cm2','j1.75':'j_1p75_mA_cm2',
          'η10':'eta_10_raw_mV','η₁₀':'eta_10_raw_mV','Capp':'C_app_mF_cm2','b':'tafel_b_raw_mV_dec'}
def calculate():
 originals=read_csv(DATA/'Reference_SI_TableS5_PublishedValues.csv')
 current={(r['variable_x'],r['variable_y']):r for r in read_csv(RESULTS/'manuscript6'/'Permutation_Baseline.csv')}
 converted=[];changes=[]
 for ref in originals:
  x=NAME_MAP[ref['variable_x_label']];y=NAME_MAP[ref['variable_y_label']]
  r=current[(x,y)]
  rho=float(r['rho_spearman']);p=float(r['p_permutation']);p_approx=float(r['p_approx_scipy'])
  converted.append({'Variable X':ref['variable_x_label'],'Variable Y':ref['variable_y_label'],
    'rho_s':f'{rho:+.3f}','p_perm_B200000':f'{p:.6f}', 'p_approx':f'{p_approx:.6f}',
    'fixed_pair_seed_label':r['pair_seed_label'],'baseline_spawn_key':r['spawn_key_index']})
  changes.append({'variable_x':x,'variable_y':y,'SI_old_p_perm':ref['p_perm_reported'],
    'recomputed_p_perm':f'{p:.6f}','old_SI_rho':ref['rho_reported'],'recomputed_rho':f'{rho:+.3f}',
    'manuscript_edit_needed_for_exact_p_consistency':int(f'{p:.6f}'!=f'{float(ref["p_perm_reported"]):.6f}'),
    'nominal_significance_changed':int((float(ref['p_perm_reported'])<.05)!=(p<.05))})
 a=write_csv(RESULTS/'manuscript6'/'SI_TableS5_Seed_Consistent_Replacement.csv',converted)
 b=write_csv(RESULTS/'manuscript6'/'Manuscript_pValue_Consistency_Checklist.csv',changes)
 return a,b
if __name__=='__main__':print(calculate())
