"""Run the live L6-001 source-to-Phase-4 handoff."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
PHASE2 = ROOT / "docs" / "phase2-ingestion" / "L6" / "001"
SCORE = PHASE2 / "score.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


collector = load_module("l6_001_collector", PHASE2 / "collector.py")
phase2_parser = load_module("l6_001_parser", PHASE2 / "parser.py")
scorer = load_module("l6_001_score", SCORE)


def load_state(path: Path) -> dict[str, float | int | None]:
    if not path.exists():
        return {"prev_score": None, "missing_days": 0}
    state = json.loads(path.read_text(encoding="utf-8"))
    if set(state) != {"prev_score", "missing_days"}:
        raise ValueError("invalid L6-001 state")
    if state["prev_score"] is not None:
        state["prev_score"] = float(state["prev_score"])
    state["missing_days"] = int(state["missing_days"])
    if state["missing_days"] < 0:
        raise ValueError("missing_days cannot be negative")
    return state


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def latest_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 60:
        raise ValueError("L6-001 needs at least 60 source observations")
    return sorted(rows, key=lambda row: row["observation_date"])[-60:]


def build_handoff(rows: list[dict[str, str]], state: dict[str, float | int | None], run_at: str) -> tuple[dict, dict]:
    latest = rows[-1]
    is_missing = latest["availability_status"] == "STALE"
    history = [float(row["gpr_act_index"]) for row in rows]
    score, missing_days, trend_note = scorer.compute_l6_001(
        history, is_missing, state["prev_score"], state["missing_days"]
    )
    handoff = {
        "variable_id": "L6-001",
        "observation_timestamp": f"{latest['observation_date']}T00:00:00Z",
        "value": score,
        "unit_or_scale": "standard_deviation_units_clamped_-1_to_1",
        "availability_status": "STALE" if is_missing else "AVAILABLE",
        "source_reference": latest["manifest_path"],
        "quality_flag": "MISSING_RESET" if is_missing and missing_days >= 3 else "MISSING_DECAY" if is_missing else latest["validation_status"],
    }
    if trend_note is not None:
        handoff["trend_note"] = trend_note
    return handoff, {"prev_score": score, "missing_days": missing_days, "updated_at": run_at}


def run(data_dir: Path) -> dict:
    raw_dir = data_dir / "raw"
    manifest_dir = data_dir / "manifests"
    phase2_output = data_dir / "phase2.csv"
    state_path = data_dir / "state.json"
    handoff_path = data_dir / "l6_001_phase3_handoff.json"
    run_at = datetime.now(timezone.utc).isoformat()
    state = load_state(state_path)
    try:
        manifest = collector.collect(raw_dir, manifest_dir)
        rows = phase2_parser.parse(Path(manifest["raw_path"]), Path(manifest["manifest_path"]))
        phase2_parser.write(rows, phase2_output)
    except Exception:
        if not phase2_output.exists():
            raise
    rows = latest_rows(phase2_output)
    handoff, new_state = build_handoff(rows, state, run_at)
    write_json(state_path, {"prev_score": new_state["prev_score"], "missing_days": new_state["missing_days"]})
    write_json(handoff_path, [handoff])
    return {"handoff": handoff, "state": new_state, "output": str(handoff_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    args = parser.parse_args()
    print(json.dumps(run(args.data_dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
