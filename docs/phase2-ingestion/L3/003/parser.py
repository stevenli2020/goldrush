"""Select the L3-003 terminal-rate proxy from a validated L3-002 curve."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

VARIABLE_ID = "L3-003"
PARSER_VERSION = "0.1.0"
METHOD_VERSION = "1.0.0"
REQUIRED = {
    "variable_id", "observation_date", "contract", "implied_policy_rate_pct",
    "expiry_date", "curve_position", "source_url", "source_pdf_path",
    "source_manifest_path", "source_pdf_sha256", "retrieved_at",
    "validation_status", "availability_status",
}
FIELDS = [
    "variable_id", "observation_date", "expected_terminal_policy_rate_pct",
    "selected_contract", "selected_expiry_date", "curve_direction",
    "nearest_rate_pct", "farthest_rate_pct", "contracts_examined",
    "selection_method_version", "unit", "source_curve", "source_url",
    "source_pdf_path", "source_manifest_path", "source_pdf_sha256", "retrieved_at",
    "parser_version", "is_revised", "prior_terminal_rate_pct",
    "validation_status", "availability_status",
]


def prior_values(path: Path | None) -> dict[str, float]:
    if path is None or not path.exists(): return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {r["observation_date"]: float(r["expected_terminal_policy_rate_pct"])
                for r in csv.DictReader(handle) if r.get("validation_status") == "PASS"}


def parse_terminal(curve_path: Path, prior_path: Path | None = None) -> list[dict]:
    with curve_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"L3-002 curve missing columns: {sorted(REQUIRED - set(reader.fieldnames or []))}")
        input_rows = list(reader)
    grouped: dict[str, list[dict]] = {}
    for row in input_rows:
        if row["variable_id"] != "L3-002" or row["validation_status"] != "PASS":
            continue
        try:
            rate = float(row["implied_policy_rate_pct"]); position = int(row["curve_position"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"malformed L3-002 curve row: {row}") from exc
        if not -1 <= rate <= 20 or position < 1:
            raise ValueError(f"invalid L3-002 curve row: {row}")
        grouped.setdefault(row["observation_date"], []).append({**row, "rate": rate, "position": position})
    previous = prior_values(prior_path)
    output = []
    for obs, rows in sorted(grouped.items()):
        rows.sort(key=lambda row: row["position"])
        contracts = rows[:12]
        if len(contracts) < 2:
            raise ValueError(f"L3-002 curve has fewer than two contracts for {obs}")
        if len({row["position"] for row in contracts}) != len(contracts):
            raise ValueError(f"duplicate curve position for {obs}")
        provenance = {(r["source_pdf_sha256"], r["source_manifest_path"]) for r in contracts}
        if len(provenance) != 1:
            raise ValueError(f"mixed source provenance for {obs}")
        nearest, farthest = contracts[0], contracts[-1]
        if farthest["rate"] < nearest["rate"]:
            direction = "downward"; selected = min(contracts, key=lambda row: row["rate"])
        elif farthest["rate"] > nearest["rate"]:
            direction = "upward"; selected = max(contracts, key=lambda row: row["rate"])
        else:
            direction = "flat"; selected = farthest
        prior = previous.get(obs); value = selected["rate"]
        output.append({
            "variable_id": VARIABLE_ID, "observation_date": obs,
            "expected_terminal_policy_rate_pct": value,
            "selected_contract": selected["contract"], "selected_expiry_date": selected["expiry_date"],
            "curve_direction": direction, "nearest_rate_pct": nearest["rate"],
            "farthest_rate_pct": farthest["rate"], "contracts_examined": len(contracts),
            "selection_method_version": METHOD_VERSION, "unit": "percent_per_annum",
            "source_curve": "L3-002", "source_url": selected["source_url"],
            "source_pdf_path": selected["source_pdf_path"],
            "source_manifest_path": selected["source_manifest_path"],
            "source_pdf_sha256": selected["source_pdf_sha256"], "retrieved_at": selected["retrieved_at"],
            "parser_version": PARSER_VERSION, "is_revised": prior is not None and prior != value,
            "prior_terminal_rate_pct": prior if prior is not None and prior != value else None,
            "validation_status": "PASS",
            "availability_status": "STALE" if any(r["availability_status"] == "STALE" for r in contracts) else "AVAILABLE",
        })
    if not output: raise ValueError("no validated L3-002 curve observations")
    return output


def carry_forward(prior: Path) -> list[dict]:
    if not prior.exists(): raise FileNotFoundError("no prior L3-003 observation is available")
    with prior.open(newline="", encoding="utf-8") as handle:
        rows=[r for r in csv.DictReader(handle) if r.get("validation_status") == "PASS"]
    if not rows: raise ValueError("prior L3-003 output has no valid observation")
    latest=max(rows,key=lambda r:r["observation_date"]); latest["availability_status"]="STALE"; return [latest]


def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True); output.with_suffix(".status.json").unlink(missing_ok=True)
    with output.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)


def write_blocked(output: Path, reason: str) -> Path:
    path=output.with_suffix(".status.json"); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({"variable_id":VARIABLE_ID,"status":"BLOCKED","availability_status":"BLOCKED",
        "reason":reason,"checked_at":datetime.now(timezone.utc).isoformat(),"parser_version":PARSER_VERSION},indent=2)+"\n",encoding="utf-8"); return path


def main(argv: list[str] | None = None) -> int:
    cli=argparse.ArgumentParser(description="Build L3-003 Expected Terminal Policy Rate")
    cli.add_argument("--curve",type=Path); cli.add_argument("--prior",type=Path)
    cli.add_argument("--output",type=Path,default=Path("data/processed/L3_003_observations.csv")); args=cli.parse_args(argv)
    try:
        if args.curve: rows=parse_terminal(args.curve,args.prior)
        elif args.prior: rows=carry_forward(args.prior)
        else: raise ValueError("provide --curve or --prior")
    except (OSError,ValueError) as exc:
        if args.prior:
            try: rows=carry_forward(args.prior)
            except (OSError,ValueError) as fallback_exc:
                path=write_blocked(args.output,str(fallback_exc)); print(json.dumps({"status":"BLOCKED","status_path":str(path)})); return 0
        else:
            path=write_blocked(args.output,str(exc)); print(json.dumps({"status":"BLOCKED","status_path":str(path)})); return 0
    write_csv(rows,args.output); print(json.dumps({"rows":len(rows),"latest":rows[-1]})); return 0


if __name__ == "__main__": raise SystemExit(main())
