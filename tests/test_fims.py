import json
import tempfile
import unittest
from pathlib import Path

import fims


class FIMSTest(unittest.TestCase):
    def test_save_baseline_and_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "data"
            root.mkdir()
            (root / "a.txt").write_text("hello", encoding="utf-8")
            baseline = Path(tmp_dir) / "baseline.json"

            fims.save_baseline(root, baseline)

            loaded = json.loads(baseline.read_text(encoding="utf-8"))
            self.assertIn("a.txt", loaded)

    def test_compare_snapshot_detects_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "data"
            root.mkdir()
            file_path = root / "a.txt"
            file_path.write_text("hello", encoding="utf-8")
            baseline = Path(tmp_dir) / "baseline.json"
            fims.save_baseline(root, baseline)

            file_path.write_text("changed", encoding="utf-8")
            (root / "b.txt").write_text("new", encoding="utf-8")
            file_path.unlink()

            changes = fims.compare_snapshot(root, baseline)
            self.assertEqual(changes["added"], ["b.txt"])
            self.assertEqual(changes["removed"], ["a.txt"])
            self.assertEqual(changes["modified"], [])


if __name__ == "__main__":
    unittest.main()
