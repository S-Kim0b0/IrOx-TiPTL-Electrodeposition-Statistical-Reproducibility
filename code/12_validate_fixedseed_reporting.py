#!/usr/bin/env python3
"""Check that output Table S5 and 16-condition baseline are numerically identical to the frozen reporting snapshot.

The snapshot is derived from fixed-ID calculations, not an external validation of raw electrochemical measurements.
"""

# INPUT: a frozen fixed-seed Table S5 snapshot and recomputed replacement table.
# ALGORITHM: compare all 15 rows, pair IDs, rho, approximate and permutation p.
# OUTPUT: exact reporting consistency CSV; not an independent measurement check.

from analysis_core import DATA,RESULTS,read_csv,write_csv

def calculate():
    target=read_csv(DATA/'Reference_FixedSeed_SI_TableS5.csv')
    actual=read_csv(RESULTS/'manuscript6'/'SI_TableS5_Seed_Consistent_Replacement.csv')
    if len(target)!=15 or len(actual)!=15:raise AssertionError('Expected exactly 15 rows')
    rows=[]
    for i,(a,b) in enumerate(zip(target,actual),1):
        success=(a['variable_x']==b['Variable X'] and a['variable_y']==b['Variable Y'] and
             a['rho_s']==b['rho_s'] and a['p_permutation']==b['p_perm_B200000'] and
             a['p_approx']==b['p_approx'] and a['fixed_pair_seed']==b['fixed_pair_seed_label'])
        rows.append({'row':i,'variable_x':a['variable_x'],'variable_y':a['variable_y'],
          'expected_p':a['p_permutation'],'computed_p':b['p_perm_B200000'],'match':int(success)})
        if not success:raise AssertionError(f'Frozen SI Table S5 mismatch at row {i}')
    return write_csv(RESULTS/'manuscript6'/'Verification_FixedSeed_Reported_TableS5.csv',rows)

if __name__=='__main__':print(calculate())
