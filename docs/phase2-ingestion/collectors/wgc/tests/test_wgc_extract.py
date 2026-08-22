import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from wgc_extract import latest_manifests, run_parser


class ExtractTests(unittest.TestCase):
    def test_latest_manifest_selects_newest_per_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for stamp, sha in (("20260820T000000Z", "old"), ("20260821T000000Z", "new")):
                (root / f"gdt-{stamp}.json").write_text(json.dumps({"target": "gdt", "sha256": sha, "downloaded_at": stamp}))
            self.assertEqual(latest_manifests(root)[0]["sha256"], "new")

    @patch("wgc_extract.subprocess.run")
    def test_parser_command_replaces_input(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = "ok"
        run.return_value.stderr = ""
        result = run_parser({"script": "parser.py", "args": ["--input", "{input}"]}, Path("sample.xlsx"), Path("/project"), {"downloaded_at": "2026-08-21T00:00:00+00:00"})
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(run.call_args.args[0][3], "sample.xlsx")


if __name__ == "__main__":
    unittest.main()
