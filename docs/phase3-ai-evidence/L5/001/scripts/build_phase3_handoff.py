from __future__ import annotations
import argparse, csv, json
from pathlib import Path
REQUIRED={'variable_id','observation_date','official_purchase_change_tonnes','unit','source_file','source_publication_date','download_date','validation_status','availability_status'}
def build(path: Path, source: str) -> list[dict]:
    with path.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    if not rows: raise ValueError('processed input is empty')
    out=[]
    for r in rows:
        if REQUIRED-r.keys() or r['variable_id']!='L5-001' or r['unit']!='metric_tonnes' or r['validation_status']!='PASS': raise ValueError('invalid L5-001 row')
        out.append({'variable_id':'L5-001','observation_timestamp':f"{r['observation_date']}T00:00:00Z",'value':float(r['official_purchase_change_tonnes']),'unit_or_scale':'metric_tonnes','availability_status':r['availability_status'],'source_reference':source,'quality_flag':r['validation_status']})
    return out
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('--input',type=Path,required=True); a.add_argument('--source-reference',required=True); a.add_argument('--output',type=Path,required=True); x=a.parse_args(); y=build(x.input,x.source_reference); x.output.parent.mkdir(parents=True,exist_ok=True); x.output.write_text(json.dumps(y,indent=2)+'\n',encoding='utf-8'); print(f'Wrote {len(y)} handoff rows to {x.output}')
