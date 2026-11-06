#!/usr/bin/env python3
"""Compare two outputs from review_backbone_parity.gd. No files are changed."""
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('baseline',type=Path);p.add_argument('candidate',type=Path);a=p.parse_args()
report={}
for filename in ['dense_samples.json','controls.json','frame_hashes.json']:
    old=json.loads((a.baseline/filename).read_text());new=json.loads((a.candidate/filename).read_text())
    mismatches=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y]
    report[filename]={'baseline_count':len(old),'candidate_count':len(new),'mismatch_count':len(mismatches),'first_mismatches':mismatches[:10],'pass':len(old)==len(new) and not mismatches}
report['pass']=all(item['pass'] for item in report.values())
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['pass'] else 1)
