from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "validate_course_pack.py"
SPEC = importlib.util.spec_from_file_location("validate_course_pack", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Cannot load validator: {SCRIPT_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "valid_course_pack"


class ValidateCoursePackReceiptTests(unittest.TestCase):
    def copy_fixture(self, temp: str) -> tuple[Path, Path, dict]:
        target = Path(temp) / "course-pack"
        shutil.copytree(FIXTURE, target)
        manifest_path = target / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        return target, manifest_path, manifest

    def test_manifest_without_independent_evidence_receipt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, manifest_path, manifest = self.copy_fixture(temp)
            manifest.pop("evidence_receipt", None)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)
            self.assertTrue(any("evidence_receipt" in error for error in result.errors))

    def test_missing_or_unanswered_course_design_receipt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, manifest_path, manifest = self.copy_fixture(temp)
            (target / "course_design_receipt.json").unlink()
            manifest["course_design"]["calibration_items"][0]["answer"] = ""
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)
            self.assertTrue(any("course design receipt" in error for error in result.errors))
            self.assertTrue(any("calibration_items[0].answer" in error for error in result.errors))

    def test_course_design_receipt_must_match_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, _, _ = self.copy_fixture(temp)
            receipt_path = target / "course_design_receipt.json"
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["personalized_route"]["start_node_id"] = "N2"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)
            self.assertTrue(any("exactly match" in error for error in result.errors))

    def test_course_design_template_placeholder_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, manifest_path, manifest = self.copy_fixture(temp)
            receipt_path = target / "course_design_receipt.json"
            manifest["course_design"]["calibration_items"][0]["answer"] = "{{user_answer}}"
            receipt_path.write_text(
                json.dumps(manifest["course_design"]), encoding="utf-8"
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)
            self.assertTrue(any("template placeholders" in error for error in result.errors))

    def test_placeholder_url_and_zero_fingerprint_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, manifest_path, manifest = self.copy_fixture(temp)
            page = "course_home"
            manifest["notion"]["pages"][page] = "https://fake.invalid/course-home"
            manifest["notion"]["course_home_url"] = "https://fake.invalid/course-home"
            manifest["notion"]["managed_regions"][page]["source_fingerprint"] = "0" * 64
            manifest["notion"]["readback"]["pages"][page]["url"] = (
                "https://fake.invalid/course-home"
            )
            manifest["notion"]["readback"]["pages"][page]["source_fingerprint"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)

    def test_runtime_receipts_must_prove_test_id_and_unchanged_protected_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, manifest_path, manifest = self.copy_fixture(temp)
            smoke = manifest["runtime_smoke"]
            smoke.setdefault("write_page_receipts", {})["sessions"] = {
                "page_role": "sessions",
                "url": "https://app.notion.com/system-check/sessions",
                "managed_region_test_id_occurrences": 0,
                "verified_at": "2026-07-09T00:20:00+00:00",
            }
            smoke.setdefault("protected_page_receipts", {})["course_map"] = {
                "page_role": "course_map",
                "url": "https://app.notion.com/system-check/course-map",
                "before_fingerprint": "a" * 64,
                "after_fingerprint": "b" * 64,
                "managed_region_test_id_occurrences": 1,
                "verified_at": "2026-07-09T00:20:00+00:00",
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)

    def test_updated_page_must_preserve_outside_managed_region(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target, manifest_path, manifest = self.copy_fixture(temp)
            receipt = manifest["notion"]["readback"]["pages"]["course_map"]
            receipt["outside_managed_region_after_fingerprint"] = "b" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = VALIDATOR.validate(target)

            self.assertFalse(result.ok)
            self.assertTrue(
                any("outside_managed_region_after_fingerprint must match" in error for error in result.errors)
            )


if __name__ == "__main__":
    unittest.main()
