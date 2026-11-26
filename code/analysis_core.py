"""Shared fixed-seed, author-anonymized primitives for manuscript-aligned statistics.

No network services, graphics, user identity, dynamic remote dependencies or
instrument-data fabrication. Input source is the supplied final manuscript/SI tables.
"""

# SHARED INPUT CONTRACT: exactly 16 condition-level observations, unique 4x4 design.
# SHARED RNG CONTRACT: XX0000YY integer entropy plus a separate spawn-key index.
# TEST STATISTIC: Pearson correlation of average ranks (two-sided absolute tail).
# P-VALUE: (number of |rho_perm| >= |rho_obs| - 1e-12 + 1) / (B+1).

from __future__ import annotations
import csv
from itertools import combinations
from pathlib import Path
import hashlib
import numpy as np
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
CONFIG = ROOT / 'config'
RESULTS = ROOT / 'results'

VARIABLES = [
 ('Q_CA_mC','QCA', 'Integrated anodic charge, mC'),
 ('L_Ir_mg_cm2','LIr','Ir loading, mg cm^-2'),
 ('j_1p75_mA_cm2','j1.75','OER current density, mA cm^-2'),
 ('eta_10_raw_mV','eta10','Uncorrected OER overpotential, mV'),
 ('C_app_mF_cm2','Capp','Apparent capacitance, mF cm^-2'),
 ('tafel_b_raw_mV_dec','b','Uncorrected Tafel slope, mV dec^-1'),
 ('deposition_potential_V_AgAgCl','Edep','Deposition potential, V vs Ag/AgCl'),
 ('deposition_time_min','tdep','Deposition time, min'),
]

def cols(mode):
 if mode not in ('manuscript6','exploratory8'): raise ValueError(f'Unsupported analysis mode: {mode}')
 return [v[0] for v in VARIABLES[:6 if mode=='manuscript6' else 8]]

def write_csv(path, rows, headers=None):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 rows=list(rows)
 if headers is None:
  if not rows: raise ValueError(f'Provide explicit headers for empty output: {path}')
  headers=list(rows[0])
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=headers,extrasaction='raise');w.writeheader();w.writerows(rows)
 return path

def read_csv(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def sha(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()

# The same 16 rows are used for every pair; no pseudoreplication of electrodes.
def read_input(mode='manuscript6'):
 data=read_csv(DATA/'Analysis_Input_16Conditions.csv')
 if len(data)!=16: raise ValueError('Expected exactly 16 condition rows')
 keys=cols(mode)
 observed={(float(r['deposition_potential_V_AgAgCl']),int(r['deposition_time_min'])) for r in data}
 expected={(p,t) for p in (0.60,0.65,0.70,0.75) for t in (3,5,10,15)}
 if observed!=expected: raise ValueError('Missing/duplicated potential-time combinations')
 if len({r['condition_id'] for r in data})!=16:raise ValueError('Duplicate condition identifiers')
 matrix=np.array([[float(r[k]) for k in keys] for r in data],dtype=np.float64)
 if not np.isfinite(matrix).all(): raise ValueError('Nonfinite or missing numeric values')
 if np.any(np.ptp(matrix,axis=0)==0): raise ValueError('Cannot correlate a constant variable')
 return data,keys,matrix

# Prevent post-hoc seed selection: reject any mapping other than frozen 01–08.
def read_ids(path=None):
 reg=read_csv(path or CONFIG/'Variable_ID_Registry.csv')
 mapping={r['variable_key']:int(r['variable_id']) for r in reg}
 if set(mapping)!={x[0] for x in VARIABLES}: raise ValueError('ID registry does not match all 8 variable keys')
 if len(set(mapping.values()))!=len(mapping): raise ValueError('IDs must be unique')
 if any(not 1<=v<=99 for v in mapping.values()): raise ValueError('Fixed variable IDs must be 1..99')
 if mapping != {x[0]:i for i,x in enumerate(VARIABLES,1)}: raise ValueError('Fixed ID allocation must be 01..08 in declared variable order')
 return mapping

def pairs(mode, ids_path=None):
 m=read_ids(ids_path); items=[]
 for i,j in combinations(cols(mode),2):
  a,b=sorted((m[i],m[j])); label=f'{a:02d}0000{b:02d}'
  items.append({'variable_x':i,'variable_y':j,'variable_id_x':f'{m[i]:02d}','variable_id_y':f'{m[j]:02d}',
                'pair_seed_label':label,'pair_seed_entropy':int(label)})
 if len({x['pair_seed_label'] for x in items})!=len(items):raise ValueError('Seed collision')
 return items

# The 11-digit seed_label is for humans; it is not one integer passed to PCG64.
def seed_info(pair_seed_label,replicate):
 """Human label XX0000YYRRR; *actual* RNG is SeedSequence(entropy=XX0000YY,spawn_key=(RRR,))."""
 r=int(replicate)
 if not 0<=r<=999:raise ValueError('replicate must be 0..999')
 label=f'{pair_seed_label}{r:03d}'
 return {'seed_label':label, 'pair_seed_entropy':int(pair_seed_label), 'spawn_key_index':r,'bit_generator':'PCG64'}

# Deterministically generate a substream: one entropy per pair, one spawn_key per run.
def rng_for(pair_seed_label,replicate):
 ss=np.random.SeedSequence(int(pair_seed_label),spawn_key=(int(replicate),))
 return np.random.Generator(np.random.PCG64(ss))

# Apply average ranks for ties and calculate Pearson correlations of ranked columns.
def ranks_and_rho(matrix):
 ranks=np.column_stack([rankdata(matrix[:,i],method='average') for i in range(matrix.shape[1])])
 rhos=np.corrcoef(ranks,rowvar=False)
 return ranks,rhos

# Re-pair ranked Y relative to X; do NOT resample rows as independent electrodes.
def test_one(x, y, observed_rho, rng, B, batch_size=50000):
 """Two-sided abs(rho) Monte Carlo; permutes *whole condition-level* Y ranks."""
 if B<1 or batch_size<1:raise ValueError('B and batch_size must be positive')
 rx=rankdata(np.asarray(x,dtype=float),method='average');ry=rankdata(np.asarray(y,dtype=float),method='average')
 xc=rx-rx.mean();yc=ry-ry.mean()
 scale=float(np.linalg.norm(xc)*np.linalg.norm(yc))
 if scale==0: raise ValueError('Undefined statistic due to constant ranks')
 target=abs(float(observed_rho));hits=0;used=0
 while used<B:
  n=min(batch_size,B-used)
  # Each row is one complete 16-condition shuffle of ranked Y.
  permuted=rng.permuted(np.broadcast_to(yc,(n,len(yc))),axis=1)
  # Dot products of centered ranks are algebraically equivalent to Pearson rho.
  rs=np.einsum('ij,j->i',permuted,xc,optimize=False)/scale
  # Include ties at observed |rho| within the declared numerical tolerance.
  hits+=int(np.count_nonzero(np.abs(rs)>=target-1e-12))
  used+=n
 # The +1 correction prevents zero Monte Carlo p-values.
 return hits,(hits+1)/(B+1)

def stats_for_pairs(mode,registry=None):
 data,keys,matrix=read_input(mode)
 ranks,rhos=ranks_and_rho(matrix)
 records=[]
 for row in pairs(mode,registry):
  i,j=keys.index(row['variable_x']),keys.index(row['variable_y'])
  ar=matrix[:,i];br=matrix[:,j]
  rho_approx,p_approx=spearmanr(ar,br)
  rho=float(rhos[i,j]); assert abs(rho-rho_approx)<1e-12
  records.append({**row,'N':len(data),'rho_spearman':rho,'p_approx_scipy':float(p_approx)})
 return records

# Adjust nominal p-values for the chosen test family; separate from SI Table S5.
def holm_bh(values):
 ps=np.array(values,dtype=float);m=len(ps)
 if not m:raise ValueError('No p-values')
 order=np.argsort(ps,kind='stable')
 holm=np.empty_like(ps);holm[order]=np.minimum(1,np.maximum.accumulate(ps[order]*(m-np.arange(m))))
 bh=np.empty_like(ps);bh[order]=np.minimum(1,np.minimum.accumulate((ps[order]*m/(np.arange(m)+1))[::-1])[::-1])
 return holm,bh
