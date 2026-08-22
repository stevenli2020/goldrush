"""Parse WGC official gold reserve shares for L5-002."""
import argparse, hashlib
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def parse_file(path: Path, publication_date: str, download_date: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name="PDF", header=None)
    header = next((i for i in range(len(raw)) if "Tonnes" in raw.iloc[i].astype(str).tolist() and "% of reserves**" in raw.iloc[i].astype(str).tolist()), None)
    if header is None: raise ValueError("Official reserve-share header not found")
    tonnes_col = next(i for i,v in enumerate(raw.iloc[header].astype(str)) if v == "Tonnes")
    share_col = next(i for i,v in enumerate(raw.iloc[header].astype(str)) if "% of reserves**" in str(v))
    digest=hashlib.sha256(path.read_bytes()).hexdigest(); records=[]
    for _, row in raw.iloc[header+1:].iterrows():
        name=row.iloc[1] if len(row)>1 else None
        tonnes=pd.to_numeric(row.iloc[tonnes_col],errors="coerce")
        share=pd.to_numeric(row.iloc[share_col],errors="coerce")
        if not isinstance(name,str) or not name.strip() or pd.isna(share): continue
        if pd.notna(tonnes) and tonnes < 0: raise ValueError(f"Negative holdings for {name}")
        records.append({"variable_id":"L5-002","country":name.strip(),"gold_share_of_reserves":float(share),"holdings_tonnes":float(tonnes) if pd.notna(tonnes) else None,"unit":"fraction","source_file":path.name,"source_publication_date":publication_date,"download_date":download_date,"workbook_sha256":digest,"ingested_at":datetime.now(timezone.utc).isoformat(),"validation_status":"PASS","availability_status":"AVAILABLE","parser_version":"1.0.0"})
    if not records: raise ValueError("No reserve-share records found")
    return pd.DataFrame(records).drop_duplicates("country")

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True,type=Path); ap.add_argument("--output",required=True,type=Path); ap.add_argument("--publication-date",required=True); ap.add_argument("--download-date",required=True); a=ap.parse_args(argv)
    df=parse_file(a.input,a.publication_date,a.download_date); a.output.parent.mkdir(parents=True,exist_ok=True); df.to_csv(a.output,index=False); print(f"Reserve-share records parsed: {len(df)}")

if __name__ == "__main__": main()
