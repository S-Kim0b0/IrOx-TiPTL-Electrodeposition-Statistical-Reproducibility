#!/usr/bin/env python3
"""Independently calculate phi2e and activity-normalization descriptors."""

# INPUT: condition-level Q_CA, Ir loading, and selected-electrode j_1.75.
# EQUATIONS: Q_Ir,2e = (2F/M_Ir) m_Ir; phi_2e = 100 Q_Ir,2e/Q_CA.
# OUTPUT: results/Derived_Charge_and_Activity.csv; not an instrument trace reconstruction.

import argparse
from pathlib import Path
from analysis_core import read_csv,write_csv,ROOT,DATA,RESULTS
F=96485.0 # C mol^-1, manuscript rounded constant
M_IR=192.217 # g mol^-1
A_DEP=1.00 # cm2, geometric deposition area, both sides

def calculate(destination):
 src=read_csv(DATA/'Analysis_Input_16Conditions.csv')
 rows=[]
 for r in src:
  Q=float(r['Q_CA_mC']);L=float(r['L_Ir_mg_cm2']);j=float(r['j_1p75_mA_cm2'])
  # With L in mg cm^-2 and A_DEP in cm^2, g-to-mg and C-to-mC factors cancel.
  Q2=2*F*L*A_DEP/M_IR
  # The mass activity is j_1.75/L_Ir in A gIr^-1 numerically.
  rows.append({'condition_id':r['condition_id'],'Q_CA_mC':Q,'L_Ir_mg_cm2':L,
   'Q_Ir_2e_mC_calculated':Q2,'phi_2e_pct_calculated':100*Q2/Q,
   'mass_activity_A_gIr_calculated':j/L,
   'current_density_per_charge_mA_cm2_C1':j*1000/Q,
   'charge_per_mass_mC_mg1':Q/(L*A_DEP),
   'F_C_mol':F,'M_Ir_g_mol':M_IR,'deposition_area_cm2':A_DEP})
 return write_csv(destination,rows)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=RESULTS/'Derived_Charge_and_Activity.csv');args=a.parse_args()
 print(calculate(args.out))
