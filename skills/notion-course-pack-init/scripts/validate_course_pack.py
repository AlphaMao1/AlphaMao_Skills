#!/usr/bin/env python3
"""Validate local audit files for a Notion Course Pack.

This validator is intentionally local-only. It checks manifest shape and audit
file presence, but it never reads or writes Notion.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


SCHEMA_VERSION = "notion-course-pack-init.manifest.v3"
COURSE_DESIGN_SCHEMA_VERSION = "notion-course-pack-init.course-design.v1"
EVIDENCE_SCHEMA_VERSION = "notion-course-pack-init.evidence-receipt.v1"
EVIDENCE_SOURCE = "codex-notion-readback"
REQUIRED_PAGE_KEYS = (
    "course_home",
    "runtime_snapshot",
    "course_map",
    "course_state_profile",
    "sources_coverage",
    "sessions",
    "notes_inbox",
    "codex_handoff_queue",
)
COURSE_HOME_CHILD_KEYS = tuple(key for key in REQUIRED_PAGE_KEYS if key != "course_home")
REQUIRED_AUDIT_FILES = ("material_read_report.md", "sync_report.md")
COURSE_DESIGN_RECEIPT_FILE = "course_design_receipt.json"
AUDIT_REQUIRED_PHRASES = {
    "material_read_report.md": ("材料读取报告", "正式范围", "来源指纹", "Course_Map"),
    "sync_report.md": ("同步报告", "托管区域", "回读", "幂等", "隔离烟测"),
}
REQUIRED_RUNTIME_FILES = (
    "chatgpt_runtime_smoke_prompt.md",
    "runtime_smoke_test_guide.md",
)
OPTIONAL_RENDERED_FILES = (
    "chatgpt_runtime_smoke_prompt.md",
    "runtime_smoke_test_guide.md",
    "course_init_report.md",
)
RUNTIME_GUARD_PHRASES = (
    "课程首页 URL",
    "不要自行选择最近课程",
    "相似课程",
    "烟测 prompt 未渲染",
    "隔离",
)
MANAGED_BY = "notion-course-pack-init"
MANAGED_UPDATE_POLICY = "replace-managed-region-only"
IDEMPOTENCY_STRATEGY = "upsert-by-course-id-and-page-role"
SMOKE_ISOLATION_MODE = "isolated-system-check-course"
SMOKE_WRITE_KEYS = (
    "runtime_snapshot",
    "course_state_profile",
    "sessions",
    "notes_inbox",
)
SMOKE_NO_WRITE_KEYS = ("course_map", "sources_coverage")
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")
SMOKE_TEST_ID_RE = re.compile(r"^runtime_smoke_[A-Za-z0-9][A-Za-z0-9._-]*$")
ZERO_FINGERPRINT = "0" * 64


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]
    warnings: list[str]


def is_url(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_evidence_url(value: object) -> bool:
    if not is_url(value):
        return False
    hostname = (urlparse(str(value)).hostname or "").lower().rstrip(".")
    return bool(hostname) and hostname != "invalid" and not hostname.endswith(".invalid")


def load_manifest(path: Path) -> tuple[dict | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"manifest not found: {path}"]
    except UnicodeDecodeError as exc:
        return None, [f"manifest is not valid UTF-8: {exc}"]
    except OSError as exc:
        return None, [f"manifest could not be read: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"manifest is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, ["manifest root must be an object"]
    return data, []


def resolve_manifest_path(target: Path) -> tuple[Path, Path]:
    if target.is_dir():
        return target / "manifest.json", target
    return target, target.parent


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _resolved_string(value: object) -> bool:
    return _non_empty_string(value) and "{{" not in str(value) and "}}" not in str(value)


def _read_utf8(path: Path, errors: list[str], *, label: str) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{label} is not valid UTF-8: {path}: {exc}")
    except OSError as exc:
        errors.append(f"{label} could not be read: {path}: {exc}")
    return None


def _is_iso_datetime(value: object) -> bool:
    if not _non_empty_string(value):
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _is_real_fingerprint(value: object) -> bool:
    return isinstance(value, str) and bool(FINGERPRINT_RE.fullmatch(value)) and value != ZERO_FINGERPRINT


def _validate_evidence_receipt_metadata(manifest: dict, errors: list[str]) -> None:
    evidence = manifest.get("evidence_receipt")
    if not isinstance(evidence, dict):
        errors.append("missing evidence_receipt object")
        return
    if evidence.get("schema_version") != EVIDENCE_SCHEMA_VERSION:
        errors.append(f"evidence_receipt.schema_version must be {EVIDENCE_SCHEMA_VERSION}")
    if evidence.get("evidence_source") != EVIDENCE_SOURCE:
        errors.append(f"evidence_receipt.evidence_source must be {EVIDENCE_SOURCE}")
    if not _is_iso_datetime(evidence.get("captured_at")):
        errors.append("evidence_receipt.captured_at must be an ISO-8601 timestamp")
    if not _is_real_fingerprint(evidence.get("sha256")):
        errors.append("evidence_receipt.sha256 must be a non-placeholder lowercase sha256")


def _validate_material_coverage(manifest: dict, errors: list[str]) -> None:
    coverage = manifest.get("material_coverage")
    if not isinstance(coverage, dict):
        errors.append("missing material_coverage object")
        return
    if coverage.get("status") != "fully_read":
        errors.append("material_coverage.status must be fully_read")
    if not _non_empty_string(coverage.get("declared_scope")):
        errors.append("material_coverage.declared_scope must be non-empty")
    materials = coverage.get("materials")
    if not isinstance(materials, list) or not materials:
        errors.append("material_coverage.materials must be a non-empty list")
        return

    material_ids: set[str] = set()
    material_nodes: dict[str, set[str]] = {}
    for index, material in enumerate(materials):
        prefix = f"material_coverage.materials[{index}]"
        if not isinstance(material, dict):
            errors.append(f"{prefix} must be an object")
            continue
        material_id = material.get("material_id")
        if not _non_empty_string(material_id):
            errors.append(f"{prefix}.material_id must be non-empty")
            continue
        if material_id in material_ids:
            errors.append(f"duplicate material_id: {material_id}")
        material_ids.add(material_id)
        for key in ("title", "source_ref", "declared_scope"):
            if not _non_empty_string(material.get(key)):
                errors.append(f"{prefix}.{key} must be non-empty")
        role = material.get("role")
        if role not in {"core", "supplemental", "metadata-only"}:
            errors.append(f"{prefix}.role is invalid")
        read_status = material.get("read_status")
        if read_status not in {"fully_read", "out_of_scope", "blocked", "metadata_only"}:
            errors.append(f"{prefix}.read_status is invalid")
        if role == "core" and read_status != "fully_read":
            errors.append(f"core material is not fully_read: {material_id}")
        ranges = material.get("read_ranges")
        if read_status == "fully_read" and (not isinstance(ranges, list) or not ranges or not all(_non_empty_string(x) for x in ranges)):
            errors.append(f"{prefix}.read_ranges must document the fully read scope")
        fingerprint = material.get("source_fingerprint")
        if not isinstance(fingerprint, str) or not FINGERPRINT_RE.fullmatch(fingerprint):
            errors.append(f"{prefix}.source_fingerprint must be a lowercase sha256")
        mapped_nodes = material.get("mapped_node_ids")
        if role == "core" and (not isinstance(mapped_nodes, list) or not mapped_nodes or not all(_non_empty_string(x) for x in mapped_nodes)):
            errors.append(f"{prefix}.mapped_node_ids must map core material to Course_Map nodes")
        material_nodes[str(material_id)] = set(mapped_nodes) if isinstance(mapped_nodes, list) else set()

    node_map = coverage.get("node_source_map")
    if not isinstance(node_map, list) or not node_map:
        errors.append("material_coverage.node_source_map must be a non-empty list")
        return
    mapped_pairs: set[tuple[str, str]] = set()
    seen_nodes: set[str] = set()
    for index, mapping in enumerate(node_map):
        prefix = f"material_coverage.node_source_map[{index}]"
        if not isinstance(mapping, dict):
            errors.append(f"{prefix} must be an object")
            continue
        node_id = mapping.get("node_id")
        if not _non_empty_string(node_id):
            errors.append(f"{prefix}.node_id must be non-empty")
            continue
        if node_id in seen_nodes:
            errors.append(f"duplicate node_source_map node_id: {node_id}")
        seen_nodes.add(node_id)
        ids = mapping.get("material_ids")
        ranges = mapping.get("source_ranges")
        if not isinstance(ids, list) or not ids:
            errors.append(f"{prefix}.material_ids must be non-empty")
            continue
        if not isinstance(ranges, list) or not ranges or not all(_non_empty_string(x) for x in ranges):
            errors.append(f"{prefix}.source_ranges must be non-empty")
        for material_id in ids:
            if material_id not in material_ids:
                errors.append(f"{prefix} references unknown material_id: {material_id}")
            else:
                mapped_pairs.add((str(material_id), str(node_id)))
    for material_id, nodes in material_nodes.items():
        for node_id in nodes:
            if (material_id, node_id) not in mapped_pairs:
                errors.append(f"material/node mapping is not reciprocal: {material_id} -> {node_id}")
    for material_id, node_id in mapped_pairs:
        if node_id not in material_nodes.get(material_id, set()):
            errors.append(f"node/material mapping is not reciprocal: {node_id} -> {material_id}")


def _validate_course_design_value(
    design: object, errors: list[str], *, label: str = "course_design"
) -> None:
    if not isinstance(design, dict):
        errors.append(f"missing {label} object")
        return
    if design.get("schema_version") != COURSE_DESIGN_SCHEMA_VERSION:
        errors.append(f"{label}.schema_version must be {COURSE_DESIGN_SCHEMA_VERSION}")
    if design.get("status") != "calibrated":
        errors.append(f"{label}.status must be calibrated")
    if not _is_iso_datetime(design.get("captured_at")):
        errors.append(f"{label}.captured_at must be an ISO-8601 timestamp")
    for key in (
        "course_id",
        "learning_goal",
        "intended_use",
        "baseline_summary",
        "preferred_depth",
        "first_lesson_entry_point",
    ):
        if not _resolved_string(design.get(key)):
            errors.append(f"{label}.{key} must be non-empty and free of template placeholders")
    if design.get("evidence_boundary") != "route-calibration-only-not-mastery":
        errors.append(
            f"{label}.evidence_boundary must be route-calibration-only-not-mastery"
        )
    items = design.get("calibration_items")
    if not isinstance(items, list) or not 1 <= len(items) <= 3:
        errors.append(f"{label}.calibration_items must contain one to three items")
    else:
        seen_ids: set[str] = set()
        for index, item in enumerate(items):
            prefix = f"{label}.calibration_items[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("item_id", "question", "answer", "diagnostic_signal"):
                if not _resolved_string(item.get(key)):
                    errors.append(
                        f"{prefix}.{key} must be non-empty and free of template placeholders"
                    )
            item_id = item.get("item_id")
            if _non_empty_string(item_id):
                if str(item_id) in seen_ids:
                    errors.append(f"duplicate calibration item ID: {item_id}")
                seen_ids.add(str(item_id))
            if item.get("evidence_source") not in {"user_response", "existing_course_state"}:
                errors.append(
                    f"{prefix}.evidence_source must be user_response or existing_course_state"
                )
    route = design.get("personalized_route")
    if not isinstance(route, dict):
        errors.append(f"missing {label}.personalized_route object")
    else:
        if route.get("status") != "calibrated":
            errors.append(f"{label}.personalized_route.status must be calibrated")
        if not _resolved_string(route.get("start_node_id")):
            errors.append(
                f"{label}.personalized_route.start_node_id must be non-empty and free of template placeholders"
            )
        for key in ("skip_candidates", "bridge_candidates"):
            value = route.get(key)
            if not isinstance(value, list) or any(not _resolved_string(item) for item in value):
                errors.append(f"{label}.personalized_route.{key} must be a list of node IDs")


def _validate_notion_receipts(manifest: dict, notion: dict, pages: dict, errors: list[str]) -> None:
    course_id = manifest.get("course_id")
    managed = notion.get("managed_regions")
    if not isinstance(managed, dict):
        errors.append("missing notion.managed_regions object")
        managed = {}
    region_ids: set[str] = set()
    for page_key in REQUIRED_PAGE_KEYS:
        region = managed.get(page_key)
        prefix = f"notion.managed_regions.{page_key}"
        if not isinstance(region, dict):
            errors.append(f"missing managed region: {prefix}")
            continue
        expected_region_id = f"{course_id}:{page_key}:v1"
        if region.get("managed_by") != MANAGED_BY:
            errors.append(f"{prefix}.managed_by must be {MANAGED_BY}")
        if region.get("course_id") != course_id:
            errors.append(f"{prefix}.course_id must match manifest course_id")
        if region.get("region_id") != expected_region_id:
            errors.append(f"{prefix}.region_id must be {expected_region_id}")
        if region.get("region_id") in region_ids:
            errors.append(f"duplicate managed region id: {region.get('region_id')}")
        region_ids.add(str(region.get("region_id")))
        if region.get("update_policy") != MANAGED_UPDATE_POLICY:
            errors.append(f"{prefix}.update_policy must be {MANAGED_UPDATE_POLICY}")
        fingerprint = region.get("source_fingerprint")
        if not _is_real_fingerprint(fingerprint):
            errors.append(f"{prefix}.source_fingerprint must be a non-placeholder lowercase sha256")

    readback = notion.get("readback")
    if not isinstance(readback, dict):
        errors.append("missing notion.readback object")
        readback = {}
    if readback.get("status") != "verified":
        errors.append("notion.readback.status must be verified")
    if not _is_iso_datetime(readback.get("verified_at")):
        errors.append("notion.readback.verified_at must be an ISO-8601 timestamp")
    readback_pages = readback.get("pages")
    if not isinstance(readback_pages, dict):
        errors.append("missing notion.readback.pages object")
        readback_pages = {}
    for page_key in REQUIRED_PAGE_KEYS:
        receipt = readback_pages.get(page_key)
        prefix = f"notion.readback.pages.{page_key}"
        if not isinstance(receipt, dict):
            errors.append(f"missing readback receipt: {prefix}")
            continue
        if receipt.get("page_role") != page_key:
            errors.append(f"{prefix}.page_role must be {page_key}")
        if not is_evidence_url(receipt.get("url")):
            errors.append(f"{prefix}.url must be a non-placeholder http(s) URL")
        if receipt.get("url") != pages.get(page_key):
            errors.append(f"{prefix}.url must match notion.pages.{page_key}")
        if not _non_empty_string(receipt.get("title")):
            errors.append(f"{prefix}.title must be non-empty")
        expected_region = managed.get(page_key, {}).get("region_id") if isinstance(managed.get(page_key), dict) else None
        if receipt.get("region_id") != expected_region:
            errors.append(f"{prefix}.region_id must match the managed region")
        if receipt.get("region_occurrences") != 1:
            errors.append(f"{prefix}.region_occurrences must be exactly 1")
        expected_fingerprint = managed.get(page_key, {}).get("source_fingerprint") if isinstance(managed.get(page_key), dict) else None
        prewrite_fingerprint = receipt.get("prewrite_fingerprint")
        readback_fingerprint = receipt.get("readback_fingerprint")
        if not _is_real_fingerprint(prewrite_fingerprint):
            errors.append(f"{prefix}.prewrite_fingerprint must be a non-placeholder lowercase sha256")
        if not _is_real_fingerprint(readback_fingerprint):
            errors.append(f"{prefix}.readback_fingerprint must be a non-placeholder lowercase sha256")
        if prewrite_fingerprint != expected_fingerprint:
            errors.append(f"{prefix}.prewrite_fingerprint must match the managed region")
        if readback_fingerprint != prewrite_fingerprint:
            errors.append(f"{prefix}.readback_fingerprint must match prewrite_fingerprint")
        if receipt.get("source_fingerprint") != readback_fingerprint:
            errors.append(f"{prefix}.source_fingerprint must match readback_fingerprint")
        write_mode = receipt.get("write_mode")
        if write_mode not in {"created", "updated"}:
            errors.append(f"{prefix}.write_mode must be created or updated")
        outside_before = receipt.get("outside_managed_region_before_fingerprint")
        outside_after = receipt.get("outside_managed_region_after_fingerprint")
        if write_mode == "updated":
            if not _is_real_fingerprint(outside_before):
                errors.append(
                    f"{prefix}.outside_managed_region_before_fingerprint must be a non-placeholder lowercase sha256"
                )
            if not _is_real_fingerprint(outside_after):
                errors.append(
                    f"{prefix}.outside_managed_region_after_fingerprint must be a non-placeholder lowercase sha256"
                )
            if outside_before != outside_after:
                errors.append(
                    f"{prefix}.outside_managed_region_after_fingerprint must match "
                    "outside_managed_region_before_fingerprint"
                )
        elif write_mode == "created" and (
            outside_before != "not_applicable_created"
            or outside_after != "not_applicable_created"
        ):
            errors.append(
                f"{prefix} created pages must mark outside-managed-region fingerprints as not_applicable_created"
            )
        if not _is_iso_datetime(receipt.get("verified_at")):
            errors.append(f"{prefix}.verified_at must be an ISO-8601 timestamp")

    idempotency = notion.get("idempotency")
    if not isinstance(idempotency, dict):
        errors.append("missing notion.idempotency object")
    else:
        if idempotency.get("strategy") != IDEMPOTENCY_STRATEGY:
            errors.append(f"notion.idempotency.strategy must be {IDEMPOTENCY_STRATEGY}")
        if idempotency.get("status") != "verified":
            errors.append("notion.idempotency.status must be verified")
        if not _is_iso_datetime(idempotency.get("verified_at")):
            errors.append("notion.idempotency.verified_at must be an ISO-8601 timestamp")
        if idempotency.get("course_home_matches") != 1:
            errors.append("notion.idempotency.course_home_matches must be exactly 1")
        duplicates = idempotency.get("duplicate_page_roles")
        if duplicates != []:
            errors.append("notion.idempotency.duplicate_page_roles must be an empty list")


def _validate_smoke_isolation(manifest: dict, errors: list[str]) -> None:
    smoke = manifest.get("runtime_smoke")
    notion = manifest.get("notion") if isinstance(manifest.get("notion"), dict) else {}
    if not isinstance(smoke, dict):
        errors.append("missing runtime_smoke object")
        return
    if smoke.get("status") != "verified":
        errors.append("runtime_smoke.status must be verified")
    if not _is_iso_datetime(smoke.get("verified_at")):
        errors.append("runtime_smoke.verified_at must be an ISO-8601 timestamp")
    authorization = smoke.get("authorization")
    if not isinstance(authorization, dict):
        errors.append("missing runtime_smoke.authorization object")
    else:
        if authorization.get("status") != "authorized":
            errors.append("runtime_smoke.authorization.status must be authorized")
        if not _is_iso_datetime(authorization.get("recorded_at")):
            errors.append("runtime_smoke.authorization.recorded_at must be an ISO-8601 timestamp")
    if smoke.get("isolation_mode") != SMOKE_ISOLATION_MODE:
        errors.append(f"runtime_smoke.isolation_mode must be {SMOKE_ISOLATION_MODE}")
    for key in ("test_id", "test_course_id", "test_course_title"):
        if not _non_empty_string(smoke.get(key)):
            errors.append(f"runtime_smoke.{key} must be non-empty")
    if _non_empty_string(smoke.get("test_id")) and not SMOKE_TEST_ID_RE.fullmatch(str(smoke.get("test_id"))):
        errors.append("runtime_smoke.test_id must use the runtime_smoke_<stable-id> format")
    if smoke.get("test_course_id") == manifest.get("course_id"):
        errors.append("runtime_smoke.test_course_id must differ from the production course_id")
    if "SYSTEM CHECK" not in str(smoke.get("test_course_title", "")).upper():
        errors.append("runtime_smoke.test_course_title must identify a SYSTEM CHECK course")
    if not is_evidence_url(smoke.get("test_course_home_url")):
        errors.append("runtime_smoke.test_course_home_url must be a non-placeholder URL")
    else:
        production_pages = notion.get("pages") if isinstance(notion.get("pages"), dict) else {}
        if smoke.get("test_course_home_url") in production_pages.values():
            errors.append("runtime_smoke.test_course_home_url must differ from every production page URL")
    if not is_evidence_url(smoke.get("isolated_parent_url")):
        errors.append("runtime_smoke.isolated_parent_url must be a non-placeholder URL")
    if smoke.get("test_course_home_url") == smoke.get("isolated_parent_url"):
        errors.append("runtime_smoke test Course Home URL must differ from its parent URL")
    if smoke.get("allowed_write_pages") != list(SMOKE_WRITE_KEYS):
        errors.append("runtime_smoke.allowed_write_pages must match the four runtime surfaces")
    if smoke.get("forbidden_write_pages") != list(SMOKE_NO_WRITE_KEYS):
        errors.append("runtime_smoke.forbidden_write_pages must protect Course_Map and Sources & Coverage")
    if smoke.get("verified_write_pages") != list(SMOKE_WRITE_KEYS):
        errors.append("runtime_smoke.verified_write_pages must confirm all allowed smoke writes")
    if smoke.get("verified_unchanged_pages") != list(SMOKE_NO_WRITE_KEYS):
        errors.append("runtime_smoke.verified_unchanged_pages must confirm protected pages stayed unchanged")
    if smoke.get("cleanup_status") not in {"deleted-verified", "retained-explicitly"}:
        errors.append("runtime_smoke.cleanup_status must be deleted-verified or retained-explicitly")
    if not _is_iso_datetime(smoke.get("cleanup_verified_at")):
        errors.append("runtime_smoke.cleanup_verified_at must be an ISO-8601 timestamp")

    write_receipts = smoke.get("write_page_receipts")
    if not isinstance(write_receipts, dict):
        errors.append("missing runtime_smoke.write_page_receipts object")
        write_receipts = {}
    missing_write = sorted(set(SMOKE_WRITE_KEYS) - set(write_receipts))
    extra_write = sorted(set(write_receipts) - set(SMOKE_WRITE_KEYS))
    for page_key in missing_write:
        errors.append(f"missing runtime smoke write receipt: {page_key}")
    for page_key in extra_write:
        errors.append(f"unexpected runtime smoke write receipt: {page_key}")
    smoke_urls: list[str] = []
    for page_key in SMOKE_WRITE_KEYS:
        receipt = write_receipts.get(page_key)
        prefix = f"runtime_smoke.write_page_receipts.{page_key}"
        if not isinstance(receipt, dict):
            continue
        if receipt.get("page_role") != page_key:
            errors.append(f"{prefix}.page_role must be {page_key}")
        if not is_evidence_url(receipt.get("url")):
            errors.append(f"{prefix}.url must be a non-placeholder URL")
        else:
            smoke_urls.append(receipt["url"])
        if receipt.get("managed_region_test_id_occurrences") != 1:
            errors.append(f"{prefix}.managed_region_test_id_occurrences must be exactly 1")
        if not _is_iso_datetime(receipt.get("verified_at")):
            errors.append(f"{prefix}.verified_at must be an ISO-8601 timestamp")

    protected_receipts = smoke.get("protected_page_receipts")
    if not isinstance(protected_receipts, dict):
        errors.append("missing runtime_smoke.protected_page_receipts object")
        protected_receipts = {}
    missing_protected = sorted(set(SMOKE_NO_WRITE_KEYS) - set(protected_receipts))
    extra_protected = sorted(set(protected_receipts) - set(SMOKE_NO_WRITE_KEYS))
    for page_key in missing_protected:
        errors.append(f"missing runtime smoke protected-page receipt: {page_key}")
    for page_key in extra_protected:
        errors.append(f"unexpected runtime smoke protected-page receipt: {page_key}")
    for page_key in SMOKE_NO_WRITE_KEYS:
        receipt = protected_receipts.get(page_key)
        prefix = f"runtime_smoke.protected_page_receipts.{page_key}"
        if not isinstance(receipt, dict):
            continue
        if receipt.get("page_role") != page_key:
            errors.append(f"{prefix}.page_role must be {page_key}")
        if not is_evidence_url(receipt.get("url")):
            errors.append(f"{prefix}.url must be a non-placeholder URL")
        else:
            smoke_urls.append(receipt["url"])
        before = receipt.get("before_fingerprint")
        after = receipt.get("after_fingerprint")
        if not _is_real_fingerprint(before):
            errors.append(f"{prefix}.before_fingerprint must be a non-placeholder lowercase sha256")
        if not _is_real_fingerprint(after):
            errors.append(f"{prefix}.after_fingerprint must be a non-placeholder lowercase sha256")
        if before != after:
            errors.append(f"{prefix}.after_fingerprint must match before_fingerprint")
        if receipt.get("managed_region_test_id_occurrences") != 0:
            errors.append(f"{prefix}.managed_region_test_id_occurrences must be 0")
        if not _is_iso_datetime(receipt.get("verified_at")):
            errors.append(f"{prefix}.verified_at must be an ISO-8601 timestamp")

    if len(smoke_urls) != len(set(smoke_urls)):
        errors.append("runtime_smoke page receipt URLs must be unique")
    production_pages = notion.get("pages") if isinstance(notion.get("pages"), dict) else {}
    production_urls = set(production_pages.values())
    if production_urls.intersection(smoke_urls):
        errors.append("runtime_smoke page receipt URLs must differ from production pages")
    if smoke.get("test_course_home_url") in smoke_urls:
        errors.append("runtime_smoke test Course Home URL must differ from child page receipt URLs")


def validate(target: Path) -> ValidationResult:
    manifest_path, course_dir = resolve_manifest_path(target)
    errors: list[str] = []
    warnings: list[str] = []

    manifest, load_errors = load_manifest(manifest_path)
    errors.extend(load_errors)
    if manifest is None:
        return ValidationResult(False, errors, warnings)

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    for key in ("course_id", "course_title", "created_at", "template_version"):
        if not isinstance(manifest.get(key), str) or not manifest.get(key, "").strip():
            errors.append(f"missing or empty manifest field: {key}")
    if _non_empty_string(manifest.get("created_at")) and not _is_iso_datetime(manifest.get("created_at")):
        errors.append("created_at must be an ISO-8601 timestamp")

    _validate_evidence_receipt_metadata(manifest, errors)

    course_design = manifest.get("course_design")
    _validate_course_design_value(course_design, errors)
    if isinstance(course_design, dict) and course_design.get("course_id") != manifest.get("course_id"):
        errors.append("course_design.course_id must match manifest course_id")

    material_status = manifest.get("material_coverage_status")
    if material_status != "fully_read":
        errors.append("material_coverage_status must be fully_read for a valid Course Pack")
    _validate_material_coverage(manifest, errors)

    notion = manifest.get("notion")
    if not isinstance(notion, dict):
        errors.append("missing notion object")
        notion = {}

    pages = notion.get("pages")
    if not isinstance(pages, dict):
        errors.append("missing notion.pages object")
        pages = {}

    for page_key in REQUIRED_PAGE_KEYS:
        if page_key not in pages:
            errors.append(f"missing required page key: notion.pages.{page_key}")
            continue
        if not is_evidence_url(pages.get(page_key)):
            errors.append(f"missing, invalid, or placeholder URL: notion.pages.{page_key}")

    valid_page_urls = [pages.get(key) for key in REQUIRED_PAGE_KEYS if is_evidence_url(pages.get(key))]
    if len(valid_page_urls) != len(set(valid_page_urls)):
        errors.append("notion.pages URLs must be unique across the eight page roles")

    _validate_notion_receipts(manifest, notion, pages, errors)
    _validate_smoke_isolation(manifest, errors)

    course_home_url = notion.get("course_home_url")
    if not is_evidence_url(course_home_url):
        errors.append("missing, invalid, or placeholder URL: notion.course_home_url")
    elif pages.get("course_home") and pages.get("course_home") != course_home_url:
        errors.append("notion.course_home_url must match notion.pages.course_home")

    parent_child = notion.get("parent_child")
    if not isinstance(parent_child, dict):
        errors.append("missing notion.parent_child object")
        parent_child = {}

    parent_by_page = parent_child.get("parent_by_page")
    if not isinstance(parent_by_page, dict):
        errors.append("missing notion.parent_child.parent_by_page object")
        parent_by_page = {}

    if parent_by_page.get("course_home") != "parent_url":
        errors.append("notion.parent_child.parent_by_page.course_home must be parent_url")

    for page_key in COURSE_HOME_CHILD_KEYS:
        if parent_by_page.get(page_key) != "course_home":
            errors.append(f"notion.parent_child.parent_by_page.{page_key} must be course_home")

    children = parent_child.get("children_of_course_home")
    if not isinstance(children, list):
        errors.append("notion.parent_child.children_of_course_home must be a list")
    else:
        missing_children = sorted(set(COURSE_HOME_CHILD_KEYS) - set(children))
        extra_children = sorted(set(children) - set(COURSE_HOME_CHILD_KEYS))
        for child in missing_children:
            errors.append(f"missing course_home child relationship: {child}")
        for child in extra_children:
            errors.append(f"unexpected course_home child relationship: {child}")

    course_home_parent_url = parent_child.get("course_home_parent_url")
    parent_url = notion.get("parent_url")
    if isinstance(parent_url, str) and parent_url:
        if not is_evidence_url(parent_url):
            errors.append("notion.parent_url must be a non-placeholder URL when provided")
        elif course_home_parent_url != parent_url:
            errors.append("notion.parent_child.course_home_parent_url must match notion.parent_url")
    elif course_home_parent_url:
        errors.append("notion.parent_child.course_home_parent_url is set but notion.parent_url is empty")

    for filename in REQUIRED_AUDIT_FILES:
        required_path = course_dir / filename
        if not required_path.exists():
            errors.append(f"missing required audit file: {required_path}")
        elif required_path.is_dir():
            errors.append(f"required audit file is a directory: {required_path}")
        elif required_path.stat().st_size == 0:
            errors.append(f"required audit file is empty: {required_path}")
        else:
            audit_text = _read_utf8(required_path, errors, label="audit file")
            if audit_text is None:
                continue
            if "{{" in audit_text or "}}" in audit_text:
                errors.append(f"unrendered template placeholder found in audit file: {required_path}")
            for phrase in AUDIT_REQUIRED_PHRASES[filename]:
                if phrase not in audit_text:
                    errors.append(f"missing audit receipt phrase in {required_path}: {phrase}")

    design_path = course_dir / COURSE_DESIGN_RECEIPT_FILE
    if not design_path.exists():
        errors.append(f"missing required course design receipt: {design_path}")
    elif design_path.is_dir():
        errors.append(f"course design receipt is a directory: {design_path}")
    else:
        try:
            design_receipt = json.loads(design_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"course design receipt is unreadable or invalid JSON: {exc}")
        else:
            _validate_course_design_value(
                design_receipt, errors, label="course_design_receipt"
            )
            if design_receipt != course_design:
                errors.append("course_design_receipt.json must exactly match manifest.course_design")

    course_title = manifest.get("course_title") if isinstance(manifest.get("course_title"), str) else ""
    course_home_url_text = course_home_url if isinstance(course_home_url, str) else ""
    smoke = manifest.get("runtime_smoke") if isinstance(manifest.get("runtime_smoke"), dict) else {}
    smoke_title = smoke.get("test_course_title") if isinstance(smoke.get("test_course_title"), str) else ""
    smoke_url = smoke.get("test_course_home_url") if isinstance(smoke.get("test_course_home_url"), str) else ""
    smoke_test_id = smoke.get("test_id") if isinstance(smoke.get("test_id"), str) else ""

    for filename in REQUIRED_RUNTIME_FILES:
        runtime_path = course_dir / filename
        if not runtime_path.exists():
            errors.append(f"missing required rendered runtime file: {runtime_path}")
        elif runtime_path.is_dir():
            errors.append(f"required rendered runtime file is a directory: {runtime_path}")
        elif runtime_path.stat().st_size == 0:
            errors.append(f"required rendered runtime file is empty: {runtime_path}")

    for filename in OPTIONAL_RENDERED_FILES:
        rendered_path = course_dir / filename
        if not rendered_path.exists() or rendered_path.is_dir():
            continue
        rendered_text = _read_utf8(rendered_path, errors, label="rendered file")
        if rendered_text is None:
            continue
        if "{{" in rendered_text or "}}" in rendered_text:
            errors.append(f"unrendered template placeholder found in delivered file: {rendered_path}")
        if filename in REQUIRED_RUNTIME_FILES:
            if smoke_title and smoke_title not in rendered_text:
                errors.append(f"isolated smoke course title not found in rendered runtime file: {rendered_path}")
            if smoke_url and smoke_url not in rendered_text:
                errors.append(f"isolated smoke course URL not found in rendered runtime file: {rendered_path}")
            if smoke_test_id and smoke_test_id not in rendered_text:
                errors.append(f"smoke Test ID not found in rendered runtime file: {rendered_path}")
            for phrase in RUNTIME_GUARD_PHRASES:
                if phrase not in rendered_text:
                    errors.append(f"missing runtime safety phrase in {rendered_path}: {phrase}")
        elif filename == "course_init_report.md" and course_title and course_title not in rendered_text:
            errors.append(f"course title not found in delivered file: {rendered_path}")

    return ValidationResult(not errors, errors, warnings)


def print_result(result: ValidationResult) -> None:
    if result.ok:
        print("PASS: Course Pack local audit files are valid.")
    else:
        print("FAIL: Course Pack local audit files are invalid.")
    for warning in result.warnings:
        print(f"WARN: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")


def self_test() -> int:
    fixture = Path(__file__).resolve().parent / "fixtures" / "valid_course_pack"
    result = validate(fixture)
    if not result.ok:
        print("SELF-TEST FAIL: valid fixture did not pass")
        print_result(result)
        return 1

    with tempfile.TemporaryDirectory(prefix="course-pack-validator-") as tmp:
        tmpdir = Path(tmp)

        missing_url = tmpdir / "missing_url"
        shutil.copytree(fixture, missing_url)
        manifest_path = missing_url / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["notion"]["pages"]["runtime_snapshot"] = ""
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(missing_url)
        if result.ok:
            print("SELF-TEST FAIL: missing URL fixture unexpectedly passed")
            return 1

        missing_report = tmpdir / "missing_report"
        shutil.copytree(fixture, missing_report)
        (missing_report / "material_read_report.md").unlink()
        result = validate(missing_report)
        if result.ok:
            print("SELF-TEST FAIL: missing material_read_report fixture unexpectedly passed")
            return 1

        empty_report = tmpdir / "empty_report"
        shutil.copytree(fixture, empty_report)
        (empty_report / "sync_report.md").write_text("", encoding="utf-8")
        result = validate(empty_report)
        if result.ok:
            print("SELF-TEST FAIL: empty sync_report fixture unexpectedly passed")
            return 1

        missing_relationships = tmpdir / "missing_relationships"
        shutil.copytree(fixture, missing_relationships)
        manifest_path = missing_relationships / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        del data["notion"]["parent_child"]
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(missing_relationships)
        if result.ok:
            print("SELF-TEST FAIL: missing parent_child fixture unexpectedly passed")
            return 1

        missing_runtime_prompt = tmpdir / "missing_runtime_prompt"
        shutil.copytree(fixture, missing_runtime_prompt)
        (missing_runtime_prompt / "chatgpt_runtime_smoke_prompt.md").unlink()
        result = validate(missing_runtime_prompt)
        if result.ok:
            print("SELF-TEST FAIL: missing runtime prompt fixture unexpectedly passed")
            return 1

        missing_page = tmpdir / "missing_page"
        shutil.copytree(fixture, missing_page)
        manifest_path = missing_page / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        del data["notion"]["pages"]["notes_inbox"]
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(missing_page)
        if result.ok:
            print("SELF-TEST FAIL: missing page fixture unexpectedly passed")
            return 1

        unread_material = tmpdir / "unread_material"
        shutil.copytree(fixture, unread_material)
        manifest_path = unread_material / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["material_coverage_status"] = "blocked"
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(unread_material)
        if result.ok:
            print("SELF-TEST FAIL: unread material fixture unexpectedly passed")
            return 1

        partial_core_material = tmpdir / "partial_core_material"
        shutil.copytree(fixture, partial_core_material)
        manifest_path = partial_core_material / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["material_coverage"]["materials"][0]["read_status"] = "blocked"
        data["material_coverage"]["materials"][0]["read_ranges"] = []
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(partial_core_material)
        if result.ok:
            print("SELF-TEST FAIL: partial core material fixture unexpectedly passed")
            return 1

        duplicate_region = tmpdir / "duplicate_region"
        shutil.copytree(fixture, duplicate_region)
        manifest_path = duplicate_region / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["notion"]["readback"]["pages"]["course_map"]["region_occurrences"] = 2
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(duplicate_region)
        if result.ok:
            print("SELF-TEST FAIL: duplicate managed region fixture unexpectedly passed")
            return 1

        duplicate_page_role = tmpdir / "duplicate_page_role"
        shutil.copytree(fixture, duplicate_page_role)
        manifest_path = duplicate_page_role / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["notion"]["idempotency"]["course_home_matches"] = 2
        data["notion"]["idempotency"]["duplicate_page_roles"] = ["course_home"]
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(duplicate_page_role)
        if result.ok:
            print("SELF-TEST FAIL: duplicate page-role fixture unexpectedly passed")
            return 1

        production_smoke = tmpdir / "production_smoke"
        shutil.copytree(fixture, production_smoke)
        manifest_path = production_smoke / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["runtime_smoke"]["test_course_id"] = data["course_id"]
        data["runtime_smoke"]["test_course_title"] = data["course_title"]
        data["runtime_smoke"]["test_course_home_url"] = data["notion"]["course_home_url"]
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = validate(production_smoke)
        if result.ok:
            print("SELF-TEST FAIL: production-course smoke fixture unexpectedly passed")
            return 1

        placeholder_prompt = tmpdir / "placeholder_prompt"
        shutil.copytree(fixture, placeholder_prompt)
        (placeholder_prompt / "chatgpt_runtime_smoke_prompt.md").write_text(
            "用 Notion 对《{{course_title}}》做一次运行端功能烟测。\n",
            encoding="utf-8",
        )
        result = validate(placeholder_prompt)
        if result.ok:
            print("SELF-TEST FAIL: placeholder smoke prompt fixture unexpectedly passed")
            return 1

        missing_runtime_url = tmpdir / "missing_runtime_url"
        shutil.copytree(fixture, missing_runtime_url)
        (missing_runtime_url / "runtime_smoke_test_guide.md").write_text(
            "用 Notion 对《Fixture Course》做一次运行端功能烟测。\n"
            "占位符检查：不要自行选择最近课程。烟测 prompt 未渲染。\n",
            encoding="utf-8",
        )
        result = validate(missing_runtime_url)
        if result.ok:
            print("SELF-TEST FAIL: missing runtime URL fixture unexpectedly passed")
            return 1

    print("SELF-TEST PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local Course Pack audit directory.")
    parser.add_argument("target", nargs="?", help="Course directory or manifest.json path.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in validator self-tests.")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.target:
        parser.error("target is required unless --self-test is used")

    result = validate(Path(args.target))
    print_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
