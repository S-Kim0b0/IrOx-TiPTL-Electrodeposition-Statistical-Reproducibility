#!/usr/bin/env python3
"""Validate or create the PREDECLARED fixed variable IDs 01..08 (never randomized).

Main manuscript: 01..06. Additional exploratory variables: 07..08.
Existing inconsistent registries are rejected rather than silently overwritten.
"""

# INPUT: config/Variable_ID_Registry.csv (reviewer-visible fixed IDs).
# ALGORITHM: compare the complete registry against the predeclared 01–08 sequence.
# OUTPUT: validated registry; a modified mapping is a hard error.

from pathlib import Path
from analysis_core import CONFIG, VARIABLES, read_csv, write_csv,read_ids

def expected_rows():
    return [{'variable_key':key,'variable_symbol':symbol,'variable_id':f'{idx:02d}',
             'assignment_source':'fixed_order_01_to_08'}
            for idx,(key,symbol,_) in enumerate(VARIABLES,1)]

def create(path=None):
    path=Path(path or CONFIG/'Variable_ID_Registry.csv')
    # The seed mapping is frozen before observing permutation outcomes.
    expected=expected_rows()
    if path.exists():
        actual=read_csv(path)
        if actual != expected:
            raise ValueError('Fixed seed registry was changed; restore the submitted CSV')
    else:
        write_csv(path,expected)
    assert read_ids(path)=={r['variable_key']:int(r['variable_id']) for r in expected}
    return path

if __name__=='__main__':
    print(create())
