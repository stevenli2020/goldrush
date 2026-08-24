import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from jsonschema import FormatChecker, validate

sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import carry_forward, parse_observations, write_csv

SCHEMA = json.loads((Path(__file__).parents[1] / "schema.json").read_text())


class L7005Tests(unittest.TestCase):
    def raw(self, root, name, observations):
        path = Path(root) / f"{name}.json"
        path.write_text(json.dumps({"observations": observations}))
        return path

    def manifest(self, root, name, raw, series):
        path = Path(root) / f"{name}.manifest.json"
        path.write_text(json.dumps({"series_id": series, "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(), "retrieved_at": "2026-08-24T00:00:00+00:00"}))
        return path

    def pair(self, root, so, ef):
        sr = self.raw(root, "sofr", so); er = self.raw(root, "effr", ef)
        return sr, self.manifest(root, "sofr", sr, "SOFR"), er, self.manifest(root, "effr", er, "EFFR")

    def test_calculation_intersection_negative_missing_and_schema(self):
        with tempfile.TemporaryDirectory() as d:
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-21","value":"5.25"},{"date":"2026-08-22","value":"."},{"date":"2026-08-20","value":"5.0"}], [{"date":"2026-08-21","value":"5.00"},{"date":"2026-08-20","value":"5.01"},{"date":"2026-08-19","value":"5.0"}])
            rows = parse_observations(sr, sm, er, em, today=date(2026,8,24))
            self.assertEqual([r["observation_date"] for r in rows], ["2026-08-20", "2026-08-21"])
            self.assertEqual(rows[-1]["repo_funding_stress_bps"], 25.0)
            self.assertAlmostEqual(rows[0]["repo_funding_stress_bps"], -1.0)
            for row in rows: validate(row, SCHEMA, format_checker=FormatChecker())

    def test_invalid_date_numeric_wrong_series_hash_and_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            for obs in ([{"date":"bad","value":"1"}], [{"date":"2026-08-21","value":"nan"}], [{"date":"2026-08-21","value":"1"},{"date":"2026-08-21","value":"2"}]):
                sr, sm, er, em = self.pair(d, obs, [{"date":"2026-08-21","value":"1"}])
                with self.assertRaises(ValueError): parse_observations(sr, sm, er, em)
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-21","value":"1"}], [{"date":"2026-08-21","value":"1"}])
            sm.write_text(json.dumps({"series_id":"WALCL","sha256":hashlib.sha256(sr.read_bytes()).hexdigest(),"retrieved_at":"2026-08-24T00:00:00+00:00"}))
            with self.assertRaises(ValueError): parse_observations(sr, sm, er, em)

    def test_flagged_finite_outlier_is_retained(self):
        with tempfile.TemporaryDirectory() as d:
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-21","value":"45"}], [{"date":"2026-08-21","value":"1"}])
            rows = parse_observations(sr, sm, er, em)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["validation_status"], "FLAG")
            self.assertEqual(rows[0]["sofr_percent"], 45.0)

    def test_effr_provenance_failures_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-21","value":"5"}], [{"date":"2026-08-21","value":"4"}])
            em.write_text(json.dumps({"series_id":"WALCL","sha256":hashlib.sha256(er.read_bytes()).hexdigest(),"retrieved_at":"2026-08-24T00:00:00+00:00"}))
            with self.assertRaises(ValueError): parse_observations(sr, sm, er, em)
            em.write_text(json.dumps({"series_id":"EFFR","sha256":"0"*64,"retrieved_at":"2026-08-24T00:00:00+00:00"}))
            with self.assertRaises(ValueError): parse_observations(sr, sm, er, em)
            sm.write_text(json.dumps({"series_id":"SOFR","sha256":"0"*64,"retrieved_at":"2026-08-24T00:00:00+00:00"}))
            with self.assertRaises(ValueError): parse_observations(sr, sm, er, em)

    def test_no_overlap_and_stale_flag(self):
        with tempfile.TemporaryDirectory() as d:
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-20","value":"1"}], [{"date":"2026-08-21","value":"1"}])
            with self.assertRaises(ValueError): parse_observations(sr, sm, er, em)
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-01","value":"1"}], [{"date":"2026-08-01","value":"1"}])
            self.assertEqual(parse_observations(sr, sm, er, em, today=date(2026,8,24))[0]["availability_status"], "STALE")

    def test_cli_fallback_blocked_and_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); out = root / "out.csv"; cmd = [sys.executable, str(Path(__file__).parents[1]/"parser.py"), "--output", str(out)]
            blocked = subprocess.run(cmd, capture_output=True, text=True)
            status = out.with_suffix(".status.json")
            self.assertEqual(blocked.returncode, 0); self.assertEqual(json.loads(status.read_text())["status"], "BLOCKED")
            sr, sm, er, em = self.pair(d, [{"date":"2026-08-20","value":"5.10"},{"date":"2026-08-21","value":"5.25"}], [{"date":"2026-08-20","value":"5.00"},{"date":"2026-08-21","value":"5.00"}])
            good = subprocess.run(cmd + ["--sofr-raw",str(sr),"--sofr-manifest",str(sm),"--effr-raw",str(er),"--effr-manifest",str(em)], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0); self.assertFalse(status.exists())
            prior_rows = list(csv.DictReader(out.open(encoding="utf-8")))
            prior = prior_rows[0].copy()
            bad = self.raw(d, "bad", [{"date":"bad","value":"1"}]); bm = self.manifest(d,"bad",bad,"SOFR")
            fallback = subprocess.run(cmd + ["--sofr-raw",str(bad),"--sofr-manifest",str(bm),"--effr-raw",str(er),"--effr-manifest",str(em),"--prior",str(out)], capture_output=True, text=True)
            self.assertEqual(fallback.returncode, 0)
            stale = next(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(stale["availability_status"], "STALE")
            validate({**stale, "sofr_percent": float(stale["sofr_percent"]), "effr_percent": float(stale["effr_percent"]), "repo_funding_stress_bps": float(stale["repo_funding_stress_bps"])}, SCHEMA, format_checker=FormatChecker())
            for field in ("sofr_retrieved_at", "effr_retrieved_at", "sofr_raw_sha256", "effr_raw_sha256", "sofr_raw_file_path", "effr_raw_file_path", "sofr_manifest_file_path", "effr_manifest_file_path"):
                self.assertEqual(stale[field], prior[field])
            self.assertEqual(stale["observation_date"], "2026-08-21")


if __name__ == "__main__": unittest.main()
