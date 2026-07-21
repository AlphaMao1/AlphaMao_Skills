from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "render_manifest.py"
SPEC = importlib.util.spec_from_file_location("render_manifest", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Cannot load renderer: {SCRIPT_PATH}")
RENDERER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RENDERER
SPEC.loader.exec_module(RENDERER)


def sha(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def make_material(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "status": "fully_read",
                "declared_scope": "全文",
                "materials": [
                    {
                        "material_id": "source-1",
                        "title": "材料一",
                        "source_ref": "fixture://source-1",
                        "declared_scope": "全文",
                        "role": "core",
                        "read_status": "fully_read",
                        "read_ranges": ["全文"],
                        "source_fingerprint": sha("material-source-1"),
                        "mapped_node_ids": ["N1"],
                    }
                ],
                "node_source_map": [
                    {
                        "node_id": "N1",
                        "material_ids": ["source-1"],
                        "source_ranges": ["source-1：全文"],
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def make_course_design(path: Path, *, course_id: str) -> None:
    path.write_text(
        json.dumps(
            {
                "schema_version": "notion-course-pack-init.course-design.v1",
                "course_id": course_id,
                "status": "calibrated",
                "captured_at": "2026-07-11T00:00:00+00:00",
                "learning_goal": "理解并迁移课程核心机制",
                "intended_use": "互动学习",
                "baseline_summary": "用户能说明基础概念，迁移能力待验证",
                "preferred_depth": "机制优先",
                "first_lesson_entry_point": "N1",
                "evidence_boundary": "route-calibration-only-not-mastery",
                "calibration_items": [
                    {
                        "item_id": "CAL-01",
                        "question": "请用自己的例子解释核心机制。",
                        "answer": "用户给出例子并选择从 N1 开始。",
                        "evidence_source": "user_response",
                        "diagnostic_signal": "从 N1 开始，不构成掌握证据。",
                    }
                ],
                "personalized_route": {
                    "status": "calibrated",
                    "start_node_id": "N1",
                    "skip_candidates": [],
                    "bridge_candidates": [],
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


class CourseDesignValidationTests(unittest.TestCase):
    def test_unrendered_course_design_placeholder_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "course_design_receipt.json"
            make_course_design(path, course_id="course-1")
            receipt = json.loads(path.read_text(encoding="utf-8"))
            receipt["learning_goal"] = "{{learning_goal}}"

            with self.assertRaisesRegex(ValueError, "template placeholder"):
                RENDERER.validate_course_design(receipt, course_id="course-1")


def make_receipt(
    *,
    course_id: str,
    pages: dict[str, str],
    titles: dict[str, str],
    fingerprints: dict[str, str],
) -> dict:
    page_verified_at = "2026-07-11T00:09:00+00:00"
    smoke_verified_at = "2026-07-11T00:19:00+00:00"
    return {
        "schema_version": "notion-course-pack-init.evidence-receipt.v1",
        "evidence_source": "codex-notion-readback",
        "course_id": course_id,
        "captured_at": "2026-07-11T00:20:00+00:00",
        "notion_readback": {
            "status": "verified",
            "verified_at": "2026-07-11T00:10:00+00:00",
            "pages": {
                key: {
                    "page_role": key,
                    "url": pages[key],
                    "title": titles[key],
                    "region_id": f"{course_id}:{key}:v1",
                    "region_occurrences": 1,
                    "prewrite_fingerprint": fingerprints[key],
                    "readback_fingerprint": fingerprints[key],
                    "write_mode": "updated",
                    "outside_managed_region_before_fingerprint": sha(f"outside-{key}"),
                    "outside_managed_region_after_fingerprint": sha(f"outside-{key}"),
                    "verified_at": page_verified_at,
                }
                for key in RENDERER.REQUIRED_PAGE_KEYS
            },
            "idempotency": {
                "status": "verified",
                "verified_at": "2026-07-11T00:10:00+00:00",
                "course_home_matches": 1,
                "duplicate_page_roles": [],
            },
        },
        "runtime_smoke": {
            "status": "verified",
            "verified_at": smoke_verified_at,
            "authorization": {
                "status": "authorized",
                "recorded_at": "2026-07-11T00:11:00+00:00",
            },
            "isolation_mode": "isolated-system-check-course",
            "test_id": "runtime_smoke_1",
            "test_course_id": "system-check-1",
            "test_course_title": "SYSTEM CHECK | 课程一",
            "test_course_home_url": "https://app.notion.com/system-check/home",
            "isolated_parent_url": "https://app.notion.com/system-check/parent",
            "write_pages": {
                key: {
                    "page_role": key,
                    "url": f"https://app.notion.com/system-check/{key}",
                    "managed_region_test_id_occurrences": 1,
                    "verified_at": "2026-07-11T00:18:00+00:00",
                }
                for key in RENDERER.SMOKE_WRITE_KEYS
            },
            "protected_pages": {
                key: {
                    "page_role": key,
                    "url": f"https://app.notion.com/system-check/{key}",
                    "before_fingerprint": sha(f"protected-{key}"),
                    "after_fingerprint": sha(f"protected-{key}"),
                    "managed_region_test_id_occurrences": 0,
                    "verified_at": "2026-07-11T00:18:00+00:00",
                }
                for key in RENDERER.SMOKE_NO_WRITE_KEYS
            },
            "cleanup": {
                "status": "deleted-verified",
                "verified_at": smoke_verified_at,
            },
        },
    }


def make_args(temp: Path) -> tuple[argparse.Namespace, Path, dict]:
    material_path = temp / "material.json"
    course_design_path = temp / "course_design_receipt.json"
    receipt_path = temp / "evidence-receipt.json"
    make_material(material_path)
    make_course_design(course_design_path, course_id="course-1")
    pages = {
        key: f"https://app.notion.com/course/{index}"
        for index, key in enumerate(RENDERER.REQUIRED_PAGE_KEYS, start=1)
    }
    titles = {key: f"Title {key}" for key in RENDERER.REQUIRED_PAGE_KEYS}
    fingerprints = {key: sha(f"page-{key}") for key in RENDERER.REQUIRED_PAGE_KEYS}
    receipt = make_receipt(
        course_id="course-1",
        pages=pages,
        titles=titles,
        fingerprints=fingerprints,
    )
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    args = argparse.Namespace(
        course_id="course-1",
        course_title="课程一",
        created_at="2026-07-11T00:00:00+00:00",
        parent_url="https://app.notion.com/parent",
        template_version="v3",
        course_design_json=str(course_design_path),
        material_coverage_json=str(material_path),
        evidence_receipt_json=str(receipt_path),
        page=list(pages.items()),
        page_title=list(titles.items()),
        page_fingerprint=list(fingerprints.items()),
    )
    return args, receipt_path, receipt


def make_cli_command(args: argparse.Namespace, *, output: Path | None = None) -> list[str]:
    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--course-id",
        args.course_id,
        "--course-title",
        args.course_title,
        "--created-at",
        args.created_at,
        "--parent-url",
        args.parent_url,
        "--course-design-json",
        args.course_design_json,
        "--material-coverage-json",
        args.material_coverage_json,
        "--evidence-receipt-json",
        args.evidence_receipt_json,
    ]
    for key, value in args.page:
        command.extend(("--page", f"{key}={value}"))
    for key, value in args.page_title:
        command.extend(("--page-title", f"{key}={value}"))
    for key, value in args.page_fingerprint:
        command.extend(("--page-fingerprint", f"{key}={value}"))
    if output is not None:
        command.extend(("--output", str(output)))
    return command


class RenderManifestTests(unittest.TestCase):
    def test_final_manifest_is_derived_from_independent_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, _, _ = make_args(Path(temp))

            manifest = RENDERER.build_manifest(args)

            self.assertEqual(RENDERER.SCHEMA_VERSION, manifest["schema_version"])
            self.assertEqual("calibrated", manifest["course_design"]["status"])
            self.assertEqual(
                "course-1:course_home:v1",
                manifest["notion"]["managed_regions"]["course_home"]["region_id"],
            )
            readback = manifest["notion"]["readback"]["pages"]["course_home"]
            self.assertEqual(readback["prewrite_fingerprint"], readback["readback_fingerprint"])
            self.assertEqual(
                readback["outside_managed_region_before_fingerprint"],
                readback["outside_managed_region_after_fingerprint"],
            )
            self.assertEqual(1, readback["region_occurrences"])
            self.assertEqual("verified", manifest["notion"]["idempotency"]["status"])
            self.assertEqual(
                1,
                manifest["runtime_smoke"]["write_page_receipts"]["runtime_snapshot"]
                ["managed_region_test_id_occurrences"],
            )
            self.assertEqual(
                manifest["runtime_smoke"]["protected_page_receipts"]["course_map"]
                ["before_fingerprint"],
                manifest["runtime_smoke"]["protected_page_receipts"]["course_map"]
                ["after_fingerprint"],
            )
            self.assertRegex(manifest["evidence_receipt"]["sha256"], r"^[0-9a-f]{64}$")

    def test_missing_evidence_receipt_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, receipt_path, _ = make_args(Path(temp))
            receipt_path.unlink()

            with self.assertRaisesRegex(ValueError, "evidence receipt file not found"):
                RENDERER.build_manifest(args)

    def test_unanswered_course_design_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, _, _ = make_args(Path(temp))
            path = Path(args.course_design_json)
            design = json.loads(path.read_text(encoding="utf-8"))
            design["calibration_items"][0]["answer"] = ""
            path.write_text(json.dumps(design), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "calibration_items\\[0\\].answer"):
                RENDERER.build_manifest(args)

    def test_cli_writes_manifest_only_after_receipt_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args, _, _ = make_args(root)
            output = root / "manifest.json"

            result = subprocess.run(
                make_cli_command(args, output=output), capture_output=True, text=True, check=False
            )

            self.assertEqual(0, result.returncode, result.stderr)
            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("verified", manifest["notion"]["readback"]["status"])
            self.assertEqual("verified", manifest["runtime_smoke"]["status"])

    def test_fake_invalid_urls_and_zero_fingerprints_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, receipt_path, receipt = make_args(Path(temp))
            fake_pages = {key: f"https://fake.invalid/{key}" for key in RENDERER.REQUIRED_PAGE_KEYS}
            zero_fingerprints = {key: "0" * 64 for key in RENDERER.REQUIRED_PAGE_KEYS}
            args.page = list(fake_pages.items())
            args.page_fingerprint = list(zero_fingerprints.items())
            for key in RENDERER.REQUIRED_PAGE_KEYS:
                receipt["notion_readback"]["pages"][key]["url"] = fake_pages[key]
                receipt["notion_readback"]["pages"][key]["prewrite_fingerprint"] = "0" * 64
                receipt["notion_readback"]["pages"][key]["readback_fingerprint"] = "0" * 64
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            result = subprocess.run(
                make_cli_command(args), capture_output=True, text=True, check=False
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("non-placeholder", result.stderr)

    def test_all_zero_fingerprint_is_rejected_even_with_valid_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, receipt_path, receipt = make_args(Path(temp))
            args.page_fingerprint = [(key, "0" * 64) for key in RENDERER.REQUIRED_PAGE_KEYS]
            for key in RENDERER.REQUIRED_PAGE_KEYS:
                receipt["notion_readback"]["pages"][key]["prewrite_fingerprint"] = "0" * 64
                receipt["notion_readback"]["pages"][key]["readback_fingerprint"] = "0" * 64
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "all-zero placeholder"):
                RENDERER.build_manifest(args)

    def test_readback_fingerprint_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, receipt_path, receipt = make_args(Path(temp))
            receipt["notion_readback"]["pages"]["course_map"]["readback_fingerprint"] = sha(
                "unexpected-readback"
            )
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "readback_fingerprint must match"):
                RENDERER.build_manifest(args)

    def test_updated_page_outside_managed_region_change_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, receipt_path, receipt = make_args(Path(temp))
            receipt["notion_readback"]["pages"]["course_map"][
                "outside_managed_region_after_fingerprint"
            ] = sha("outside-course-map-changed")
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "outside_managed_region_after_fingerprint must match"):
                RENDERER.build_manifest(args)

    def test_runtime_smoke_requires_test_id_and_unchanged_protected_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args, receipt_path, receipt = make_args(Path(temp))
            receipt["runtime_smoke"]["write_pages"]["sessions"][
                "managed_region_test_id_occurrences"
            ] = 0
            receipt["runtime_smoke"]["protected_pages"]["course_map"]["after_fingerprint"] = sha(
                "changed-course-map"
            )
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaises(ValueError):
                RENDERER.build_manifest(args)

    def test_exact_page_inputs_reject_missing_and_duplicate_roles(self) -> None:
        values = [(key, key) for key in RENDERER.REQUIRED_PAGE_KEYS[:-1]]
        with self.assertRaises(ValueError):
            RENDERER.collect_exact(values, label="pages")

        values = [(key, key) for key in RENDERER.REQUIRED_PAGE_KEYS]
        values.append((RENDERER.REQUIRED_PAGE_KEYS[0], "duplicate"))
        with self.assertRaises(ValueError):
            RENDERER.collect_exact(values, label="pages")


if __name__ == "__main__":
    unittest.main()
