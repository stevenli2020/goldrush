import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("l4_009_parser", ROOT / "parser.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
ENDPOINT = MODULE.ENDPOINT
carry_forward = MODULE.carry_forward
parse_manifest = MODULE.parse_manifest
write_csv = MODULE.write_csv

SCHEMA = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
FIELDS = "record_date,security_type_desc,security_class1_desc,maturity_date,outstanding_amt,src_line_nbr"


def source_row(record_date, line, maturity, amount, class_desc="Notes", type_desc="Marketable"):
    return {
        "record_date": record_date,
        "security_type_desc": type_desc,
        "security_class1_desc": class_desc,
        "maturity_date": maturity,
        "outstanding_amt": amount,
        "src_line_nbr": str(line),
    }


def typed(row):
    result = dict(row)
    for field in (
        "maturing_within_1y_mil_usd", "total_marketable_outstanding_mil_usd",
        "dated_detail_outstanding_mil_usd", "classification_coverage_pct",
        "marketable_debt_maturing_within_1y_pct",
    ):
        result[field] = float(result[field])
    result["page_count"] = int(result["page_count"])
    return result


class L4009ParserTests(unittest.TestCase):
    def fixture(self, directory, pages, **manifest_changes):
        root = Path(directory)
        raw_paths, hashes, contents = [], [], []
        for number, rows in enumerate(pages, 1):
            raw = root / f"raw-{number}.json"
            raw.write_text(json.dumps({"data": rows, "meta": {"total-pages": len(pages)}}), encoding="utf-8")
            content = raw.read_bytes()
            raw_paths.append(str(raw))
            hashes.append(hashlib.sha256(content).hexdigest())
            contents.append(content)
        manifest = {
            "endpoint": ENDPOINT,
            "query": {"fields": FIELDS, "filter": "record_date:gte:1900-01-01", "page[size]": 1000},
            "retrieved_at": "2026-08-24T00:00:00+00:00",
            "raw_paths": raw_paths,
            "page_sha256": hashes,
            "source_sha256": hashlib.sha256(b"".join(contents)).hexdigest(),
            "page_count": len(pages),
        }
        manifest.update(manifest_changes)
        path = root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def valid_rows(self, record_date="2024-02-29"):
        return [
            source_row(record_date, 1, record_date, "50"),
            source_row(record_date, 2, "2024-03-01", "100"),
            source_row(record_date, 3, "2025-02-28", "200"),
            source_row(record_date, 4, "2025-03-01", "620"),
            source_row(record_date, 5, "null", "970", "Notes Total"),
            source_row(record_date, 6, "null", "30", "Federal Financing Bank"),
            source_row(record_date, 7, "null", "1000", "Total Marketable"),
            source_row(record_date, 8, "2024-03-01", "null"),
            source_row(record_date, 9, " * ", "*  "),
        ]

    def test_boundary_calculation_class_exclusion_and_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            result = parse_manifest(self.fixture(directory, [self.valid_rows()]), stale_after_days=10000)[0]
            self.assertEqual(result["maturing_within_1y_mil_usd"], 300.0)
            self.assertEqual(result["dated_detail_outstanding_mil_usd"], 970.0)
            self.assertEqual(result["total_marketable_outstanding_mil_usd"], 1000.0)
            self.assertEqual(result["classification_coverage_pct"], 97.0)
            self.assertEqual(result["marketable_debt_maturing_within_1y_pct"], 30.0)
            self.assertEqual(result["validation_status"], "PASS")
            validate(result, SCHEMA)

    def test_bill_maturity_value_can_make_coverage_exceed_100(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = [
                source_row("2024-01-31", 1, "2024-06-30", "30", "Bills Maturity Value"),
                source_row("2024-01-31", 2, "2026-01-31", "75", "Notes"),
                source_row("2024-01-31", 3, "null", "100", "Total Marketable"),
            ]
            result = parse_manifest(self.fixture(directory, [rows]), stale_after_days=10000)[0]
            self.assertEqual(result["dated_detail_outstanding_mil_usd"], 105.0)
            self.assertEqual(result["classification_coverage_pct"], 105.0)
            self.assertEqual(result["marketable_debt_maturing_within_1y_pct"], 30.0)
            validate(result, SCHEMA)

    def test_multi_page_provenance_and_determinism(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = self.valid_rows()
            manifest = self.fixture(directory, [rows[:4], rows[4:]])
            first = parse_manifest(manifest, stale_after_days=10000)
            second = parse_manifest(manifest, stale_after_days=10000)
            self.assertEqual(first, second)
            self.assertEqual(first[0]["page_count"], 2)
            self.assertEqual(len(first[0]["source_sha256"]), 64)
            self.assertIn("raw-1.json", first[0]["raw_file_paths"])
            self.assertIn("raw-2.json", first[0]["raw_file_paths"])

    def test_missing_and_duplicate_total_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, [self.valid_rows()[:-3]]))
        with tempfile.TemporaryDirectory() as directory:
            rows = self.valid_rows() + [source_row("2024-02-29", 10, "null", "1000", "Total Marketable")]
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, [rows]))

    def test_conflicting_source_line_duplicate_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = self.valid_rows() + [source_row("2024-02-29", 2, "2024-03-01", "101")]
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, [rows]))

    def test_invalid_dates_amounts_and_bounds_fail(self):
        cases = []
        bad_date = self.valid_rows(); bad_date[1] = source_row("2024-02-29", 2, "bad", "100"); cases.append(bad_date)
        bad_record = self.valid_rows(); bad_record[1] = source_row("bad", 2, "2024-03-01", "100"); cases.append(bad_record)
        negative = self.valid_rows(); negative[1] = source_row("2024-02-29", 2, "2024-03-01", "-1"); cases.append(negative)
        nan = self.valid_rows(); nan[1] = source_row("2024-02-29", 2, "2024-03-01", "NaN"); cases.append(nan)
        too_large = self.valid_rows(); too_large[1] = source_row("2024-02-29", 2, "2024-03-01", "1001"); cases.append(too_large)
        for rows in cases:
            with self.subTest(rows=rows), tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(ValueError):
                    parse_manifest(self.fixture(directory, [rows]))

    def test_hash_and_manifest_fields_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.fixture(directory, [self.valid_rows()], source_sha256="0" * 64)
            with self.assertRaises(ValueError):
                parse_manifest(manifest)
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.fixture(directory, [self.valid_rows()])
            payload = json.loads(manifest.read_text())
            payload["query"]["fields"] = "record_date,outstanding_amt"
            manifest.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                parse_manifest(manifest)

    def test_flag_available_and_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = self.valid_rows()
            rows[4]["outstanding_amt"] = "800"
            rows[3]["outstanding_amt"] = "500"
            manifest = self.fixture(directory, [rows])
            available = parse_manifest(manifest, stale_after_days=10000)[0]
            self.assertEqual(available["validation_status"], "FLAG")
            self.assertEqual(available["availability_status"], "AVAILABLE")
            self.assertEqual(parse_manifest(manifest, stale_after_days=1)[0]["availability_status"], "STALE")

    def test_fallback_is_one_schema_valid_stale_row(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = parse_manifest(self.fixture(directory, [self.valid_rows()]), stale_after_days=10000)
            prior = root / "prior.csv"
            write_csv(rows, prior)
            fallback = carry_forward(prior, retrieved_at="2026-08-24T01:00:00+00:00")
            self.assertEqual(len(fallback), 1)
            self.assertEqual(fallback[0]["availability_status"], "STALE")
            validate(typed(fallback[0]), SCHEMA)

    def test_cli_blocked_stale_and_recovery_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "out.csv"
            missing = root / "missing.json"
            command = [sys.executable, str(ROOT / "parser.py"), "--manifest", str(missing), "--output", str(output)]
            blocked = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(blocked.returncode, 0)
            status = output.with_suffix(".status.json")
            self.assertEqual(json.loads(status.read_text())["status"], "BLOCKED")

            manifest = self.fixture(directory, [self.valid_rows()])
            recovered = subprocess.run([sys.executable, str(ROOT / "parser.py"), "--manifest", str(manifest), "--output", str(output), "--stale-after-days", "10000"], capture_output=True, text=True, check=False)
            self.assertEqual(recovered.returncode, 0)
            self.assertTrue(output.exists())
            self.assertFalse(status.exists())

            stale = root / "stale.csv"
            fallback = subprocess.run([sys.executable, str(ROOT / "parser.py"), "--manifest", str(missing), "--prior", str(output), "--output", str(stale)], capture_output=True, text=True, check=False)
            self.assertEqual(fallback.returncode, 0)
            with stale.open(newline="", encoding="utf-8") as handle:
                result = list(csv.DictReader(handle))
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["availability_status"], "STALE")
            validate(typed(result[0]), SCHEMA)


if __name__ == "__main__":
    unittest.main()
