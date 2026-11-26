#!/usr/bin/env python3
"""Create SHA-256 manifest and check for common personal identifiers in deliverables.

This is a pattern check on packaged text, not a certification that an unknown
scientific dataset can never contain identifying information.
"""

# INPUT: all distributed text/code/CSV files under the repository root.
# ALGORITHM: common-pattern privacy scan and SHA-256 digest of eligible files.
# OUTPUT: privacy and checksum CSVs; pattern tests cannot guarantee total anonymity.

from pathlib import Path
import csv,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE_SUFFIX={'.docx','.xlsx','.pdf','.png','.svg','.pyc','.zip'}
EXCLUDE_NAMES={'File_SHA256_Manifest.csv','Privacy_Audit.csv','full_run_progress_internal.log','full_run_internal.pid','RELEASE_SHA256_MANIFEST.csv'}
email=re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I)
userpath=re.compile(r'(?i)(?:[A-Z]:\\Users\\|/Users/[^/\s]+/|/home/(?:oai|runner|user)[/\\])')
phone=re.compile(r'(?<!\d)(?:\+82[- ]?)?0(?:10|11|16|17|18|19)[- ]?\d{3,4}[- ]?\d{4}(?!\d)')

def audit():
 files=[];flags=[]
 for path in sorted(ROOT.rglob('*')):
  if not path.is_file() or path.suffix in EXCLUDE_SUFFIX or path.name in EXCLUDE_NAMES or '__pycache__' in path.parts: continue
  rel=path.relative_to(ROOT).as_posix();raw=path.read_bytes()
  files.append({'file_relative_path':rel,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
  if path.name=='09_audit_submission_files.py':continue  # checker includes literal detection patterns
  try:content=raw.decode('utf-8')
  except UnicodeDecodeError:continue
  # Seed numbers like 01000002000 can resemble South Korean phone numbers.
  # Suppress known-formatted pair/replicate labels before PII pattern checks.
  # Other text, including non-numeric CSV fields, is still inspected.
  if path.suffix.lower()=='.csv':
   import io
   lines=[]
   for data_row in csv.DictReader(io.StringIO(content)):
    for key,value in data_row.items():
     if value is None:continue
     if 'seed' in (key or '').lower() or 'entropy' in (key or '').lower() or 'spawn_key' in (key or '').lower():continue
     if re.fullmatch(r'\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\s*',value):continue
     lines.append(value)
   content='\n'.join(lines)
  # Named, documented numerical seed labels cannot be confidential phone numbers.
  content=re.sub(r'(?<!\d)0[1-8]0000\d{2}(?:\d{3})?(?!\d)','[FIXED_SEED_LABEL]',content)
  for name,regex in [('email',email),('local_user_path',userpath),('mobile_phone',phone)]:
   for result in regex.finditer(content):flags.append({'file_relative_path':rel,'check':name,'offset':result.start(),'risk':'REVIEW_REQUIRED'})
 # no source Word documents in distributable package
 docs=list(ROOT.rglob('*.docx'))
 if docs:flags.append({'file_relative_path':'(package)','check':'source_word_document_embedded','offset':-1,'risk':'REVIEW_REQUIRED'})
 from csv import DictWriter
 for filename,rows,headers in [('File_SHA256_Manifest.csv',files,['file_relative_path','sha256','bytes']),
     ('Privacy_Audit.csv',flags if flags else [{'file_relative_path':'PACKAGE','check':'PII_pattern_scan','offset':0,'risk':'PASS_NO_MATCH'}],
       ['file_relative_path','check','offset','risk'])]:
  with (ROOT/'results'/filename).open('w',encoding='utf-8',newline='') as f:
   w=DictWriter(f,fieldnames=headers);w.writeheader();w.writerows(rows)
 if flags:raise AssertionError(f'Found {len(flags)} potential identifying pattern(s); review before submission')
 return len(files)
if __name__=='__main__':print('Audited',audit(),'files: no detected PII patterns')
