#!/usr/bin/env python3
"""Independent small-sample exhaustive statistic/p-value and RNG-seed checks.

These checks do NOT establish experiment-level inference or independent
replication of instrument measurements.
"""

# INPUT: independent small test vectors and predeclared seed registry.
# ALGORITHM: compare average ranks, exhaustive 4-point permutations, and RNG invariants.
# OUTPUT: verification CSV independent of the study's reported p-values.

from itertools import permutations
from math import isclose
import numpy as np
from scipy.stats import rankdata,spearmanr
from analysis_core import DATA,CONFIG,RESULTS,read_input,read_ids,pairs,rng_for,test_one,write_csv

def calculate():
    x=np.array([1.0,2.0,3.0,4.0])
    y=np.array([4.0,1.0,3.0,2.0])
    observed=float(spearmanr(x,y).statistic)
    perm_values=[float(spearmanr(x,np.array(z)).statistic) for z in permutations(y)]
    k=sum(abs(z)>=abs(observed)-1e-12 for z in perm_values)
    exact_p=k/len(perm_values)
    xx=rankdata(x,method='average')
    yy=rankdata(y,method='average')
    manual=float(np.dot(xx-xx.mean(),yy-yy.mean())/np.linalg.norm(xx-xx.mean())/np.linalg.norm(yy-yy.mean()))
    assert isclose(manual,observed,abs_tol=1e-14)
    assert len(perm_values)==24 and 0<=exact_p<=1
    idmap=read_ids()
    assert [idmap[k] for k in idmap]==list(range(1,9))
    assert pairs('manuscript6')[0]['pair_seed_label']=='01000002'
    a=rng_for('01000002',0).integers(0,2**31,size=50)
    b=rng_for('01000002',0).integers(0,2**31,size=50)
    c=rng_for('01000002',1).integers(0,2**31,size=50)
    assert np.array_equal(a,b) and not np.array_equal(a,c)
    _,keys,mat=read_input('manuscript6')
    rho=float(spearmanr(mat[:,0],mat[:,1]).statistic)
    k1,p1=test_one(mat[:,0],mat[:,1],rho,rng_for('01000002',0),2000,2000)
    k2,p2=test_one(mat[:,0],mat[:,1],rho,rng_for('01000002',0),2000,333)
    assert k1==k2 and p1==p2, 'Batch partition should not affect permutation stream'
    rows=[{'verification':'toy_rho_vs_scipy','status':'PASS','observed':observed,'expected':manual},
          {'verification':'toy_exact_all_24_permutations','status':'PASS','observed':exact_p,'expected':f'{k}/24'},
          {'verification':'fixed_id_mapping','status':'PASS','observed':'01..08','expected':'01..08'},
          {'verification':'PCG64_same_seed_repeats','status':'PASS','observed':'equal','expected':'equal'},
          {'verification':'PCG64_distinct_spawn_key','status':'PASS','observed':'different','expected':'different'},
          {'verification':'2000_draws_batch_partition_invariance','status':'PASS','observed':k1,'expected':k2}]
    return write_csv(RESULTS/'Verification_Independent_Formula_Checks.csv',rows)

if __name__=='__main__':print(calculate())
