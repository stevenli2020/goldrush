"""Transform normalized CFTC gold positioning into L10-001 observations."""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime, timezone
from pathlib import Path

PARSER_VERSION = "0.1.0"
STALE_DAYS = 10


def _as_of(value: str | None) -> date:
    return datetime.fromisoformat(value).date() if value else datetime.now(timezone.utc).date()


def parse(source: Path, *, as_of: str | None = None, prior: Path | None = None) -> list[dict]:
    today = _as_of(as_of)
    prior_values: dict[str, dict] = {}
    if prior and prior.exists():
        with prior.open(newline="", encoding="utf-8") as handle:
            prior_values = {row["report_date"]: row for row in csv.DictReader(handle)}
    output: list[dict] = []
    with source.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            report_date = date.fromisoformat(row["report_date"])
            long = int(row["managed_money_long"])
            short = int(row["managed_money_short"])
            spreading = int(row["managed_money_spreading"])
            open_interest = int(row["open_interest"])
            net = long - short
            validation = "PASS"
            if min(long, short, spreading, open_interest) < 0 or abs(net) > open_interest:
                validation = "FLAG"
            prior_row = prior_values.get(row["report_date"])
            is_revision = bool(prior_row and any(
                prior_row.get(processed_name, prior_row.get(source_name, "")) != row[source_name]
                for source_name, processed_name in (
                    ("managed_money_long", "managed_money_long_contracts"),
                    ("managed_money_short", "managed_money_short_contracts"),
                    ("managed_money_spreading", "managed_money_spreading_contracts"),
                    ("open_interest", "open_interest_contracts"),
                )
            ))
            age = (today - report_date).days
            availability = "AVAILABLE" if age <= STALE_DAYS else "STALE"
            output.append({
                "variable_id": "L10-001",
                "observation_date": row["report_date"],
                "report_date": row["report_date"],
                "value": net,
                "managed_money_net_contracts": net,
                "managed_money_long_contracts": long,
                "managed_money_short_contracts": short,
                "managed_money_spreading_contracts": spreading,
                "open_interest_contracts": open_interest,
                "unit": "contracts",
                "source_name": "CFTC Disaggregated Futures-Only COT",
                "source_series_id": "CFTC_088691_FutOnly",
                "market_name": row["market_name"],
                "cftc_contract_market_code": row["cftc_contract_market_code"],
                "fut_only_or_combined": row["fut_only_or_combined"],
                "raw_path": row["raw_path"],
                "raw_sha256": row["raw_sha256"],
                "retrieved_at": row["retrieved_at"],
                "validation_status": validation,
                "availability_status": availability,
                "is_revision": is_revision,
                "prior_source_sha256": prior_row.get("raw_sha256") if is_revision and prior_row else "",
                "parser_version": PARSER_VERSION,
            })
    return sorted(output, key=lambda row: row["observation_date"])


def write_csv(rows: list[dict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    root = Path(__file__).resolve().parent
    cli = argparse.ArgumentParser(description="Parse L10-001 CFTC gold positioning")
    cli.add_argument("--source", type=Path, default=root / "data/extracted/L10_001_source.csv")
    cli.add_argument("--output", type=Path, default=root / "data/processed/L10_001_observations.csv")
    cli.add_argument("--as-of")
    cli.add_argument("--prior", type=Path)
    args = cli.parse_args()
    rows = parse(args.source, as_of=args.as_of, prior=args.prior)
    write_csv(rows, args.output)
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
