#!/usr/bin/env python3
"""Render a final Notion Course Pack manifest from independent evidence.

The CLI declarations describe the intended production write. A separate receipt
must describe the later Notion readback and isolated runtime smoke. The renderer
cross-checks both sources and fails closed; it never turns declarations alone
into a ``verified`` result and never reads or writes Notion itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


SCHEMA_VERSION = "notion-course-pack-init.manifest.v3"
COURSE_DESIGN_SCHEMA_VERSION = "notion-course-pack-init.course-design.v1"
EVIDENCE_SCHEMA_VERSION = "notion-course-pack-init.evidence-receipt.v1"
EVIDENCE_SOURCE = "codex-notion-readback"
MANAGED_BY = "notion-course-pack-init"
MANAGED_UPDATE_POLICY = "replace-managed-region-only"
IDEMPOTENCY_STRATEGY = "upsert-by-course-id-and-page-role"
SMOKE_ISOLATION_MODE = "isolated-system-check-course"
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


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_evidence_url(value: object) -> bool:
    if not isinstance(value, str) or not is_url(value):
        return False
    hostname = (urlparse(value).hostname or "").lower().rstrip(".")
    return bool(hostname) and hostname != "invalid" and not hostname.endswith(".invalid")


def _timestamp(value: object, *, label: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must use ISO-8601 format") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone")
    return parsed


def parse_iso_timestamp(value: str) -> str:
    try:
        _timestamp(value, label="timestamp")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return value


def _require_dict(value: object, *, label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _require_exact_keys(value: dict, required: tuple[str, ...], *, label: str) -> None:
    missing = [key for key in required if key not in value]
    extra = [key for key in value if key not in required]
    if missing or extra:
        parts: list[str] = []
        if missing:
            parts.append("missing=" + ",".join(missing))
        if extra:
            parts.append("unexpected=" + ",".join(sorted(extra)))
        raise ValueError(f"{label} must contain the exact required roles ({'; '.join(parts)})")


def _require_real_fingerprint(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not FINGERPRINT_RE.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase sha256")
    if value == ZERO_FINGERPRINT:
        raise ValueError(f"{label} must not be the all-zero placeholder")
    return value


def _require_status(value: dict, expected: str, *, label: str) -> None:
    if value.get("status") != expected:
        raise ValueError(f"{label}.status must be {expected}")


def _require_resolved_string(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty")
    if "{{" in value or "}}" in value:
        raise ValueError(f"{label} must not contain an unrendered template placeholder")
    return value


def parse_key_value(value: str, *, label: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"{label} must use key=value format")
    key, item = value.split("=", 1)
    key = key.strip()
    item = item.strip()
    if key not in REQUIRED_PAGE_KEYS:
        allowed = ", ".join(REQUIRED_PAGE_KEYS)
        raise argparse.ArgumentTypeError(f"unknown page key '{key}'. Allowed: {allowed}")
    if not item:
        raise argparse.ArgumentTypeError(f"{label} value for '{key}' must not be empty")
    return key, item


def parse_page(value: str) -> tuple[str, str]:
    key, url = parse_key_value(value, label="page")
    if not is_url(url):
        raise argparse.ArgumentTypeError(f"page URL for '{key}' is not a valid http(s) URL")
    return key, url


def parse_page_title(value: str) -> tuple[str, str]:
    return parse_key_value(value, label="page title")


def parse_page_fingerprint(value: str) -> tuple[str, str]:
    key, fingerprint = parse_key_value(value, label="page fingerprint")
    if not FINGERPRINT_RE.fullmatch(fingerprint):
        raise argparse.ArgumentTypeError(f"page fingerprint for '{key}' must be a lowercase sha256")
    return key, fingerprint


def collect_exact(items: list[tuple[str, str]], *, label: str) -> dict[str, str]:
    values: dict[str, str] = {}
    duplicates: list[str] = []
    for key, value in items:
        if key in values:
            duplicates.append(key)
        values[key] = value
    missing = [key for key in REQUIRED_PAGE_KEYS if key not in values]
    if duplicates or missing:
        parts: list[str] = []
        if missing:
            parts.append("missing=" + ",".join(missing))
        if duplicates:
            parts.append("duplicates=" + ",".join(sorted(set(duplicates))))
        raise ValueError(f"{label} must contain each required page exactly once ({'; '.join(parts)})")
    return values


def load_material_coverage(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"material coverage file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"material coverage file is invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("material coverage file root must be an object")
    if "material_coverage" in value:
        value = value["material_coverage"]
    return _require_dict(value, label="material_coverage")


def load_course_design(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"course design receipt not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError("course design receipt must be UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"course design receipt is invalid JSON: {exc}") from exc
    return _require_dict(value, label="course_design")


def validate_course_design(receipt: dict, *, course_id: str) -> None:
    if receipt.get("schema_version") != COURSE_DESIGN_SCHEMA_VERSION:
        raise ValueError(
            f"course_design.schema_version must be {COURSE_DESIGN_SCHEMA_VERSION}"
        )
    if receipt.get("course_id") != course_id:
        raise ValueError("course_design.course_id must match --course-id")
    _require_status(receipt, "calibrated", label="course_design")
    _timestamp(receipt.get("captured_at"), label="course_design.captured_at")
    for key in (
        "learning_goal",
        "intended_use",
        "baseline_summary",
        "preferred_depth",
        "first_lesson_entry_point",
    ):
        _require_resolved_string(receipt.get(key), label=f"course_design.{key}")
    if receipt.get("evidence_boundary") != "route-calibration-only-not-mastery":
        raise ValueError(
            "course_design.evidence_boundary must be route-calibration-only-not-mastery"
        )
    items = receipt.get("calibration_items")
    if not isinstance(items, list) or not 1 <= len(items) <= 3:
        raise ValueError("course_design.calibration_items must contain one to three items")
    seen_ids: set[str] = set()
    for index, item in enumerate(items):
        label = f"course_design.calibration_items[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{label} must be an object")
        for key in ("item_id", "question", "answer", "diagnostic_signal"):
            _require_resolved_string(item.get(key), label=f"{label}.{key}")
        if item["item_id"] in seen_ids:
            raise ValueError(f"duplicate course design calibration item: {item['item_id']}")
        seen_ids.add(item["item_id"])
        if item.get("evidence_source") not in {"user_response", "existing_course_state"}:
            raise ValueError(
                f"{label}.evidence_source must be user_response or existing_course_state"
            )
    route = _require_dict(receipt.get("personalized_route"), label="personalized_route")
    _require_status(route, "calibrated", label="personalized_route")
    _require_resolved_string(
        route.get("start_node_id"), label="personalized_route.start_node_id"
    )
    for key in ("skip_candidates", "bridge_candidates"):
        value = route.get(key)
        if not isinstance(value, list):
            raise ValueError(f"personalized_route.{key} must be a list of node IDs")
        for index, node_id in enumerate(value):
            _require_resolved_string(
                node_id, label=f"personalized_route.{key}[{index}]"
            )


def load_evidence_receipt(path: Path) -> tuple[dict, str]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise ValueError(f"evidence receipt file not found: {path}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ValueError("evidence receipt must be UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"evidence receipt is invalid JSON: {exc}") from exc
    return _require_dict(value, label="evidence receipt root"), hashlib.sha256(raw).hexdigest()


def validate_evidence_receipt(
    receipt: dict,
    *,
    course_id: str,
    pages: dict[str, str],
    titles: dict[str, str],
    fingerprints: dict[str, str],
) -> None:
    if receipt.get("schema_version") != EVIDENCE_SCHEMA_VERSION:
        raise ValueError(f"evidence receipt schema_version must be {EVIDENCE_SCHEMA_VERSION}")
    if receipt.get("evidence_source") != EVIDENCE_SOURCE:
        raise ValueError(f"evidence receipt evidence_source must be {EVIDENCE_SOURCE}")
    if receipt.get("course_id") != course_id:
        raise ValueError("evidence receipt course_id must match --course-id")
    captured_at = _timestamp(receipt.get("captured_at"), label="evidence receipt captured_at")

    readback = _require_dict(receipt.get("notion_readback"), label="notion_readback")
    _require_status(readback, "verified", label="notion_readback")
    readback_verified_at = _timestamp(
        readback.get("verified_at"), label="notion_readback.verified_at"
    )
    if readback_verified_at > captured_at:
        raise ValueError("notion_readback.verified_at must not be later than captured_at")

    readback_pages = _require_dict(readback.get("pages"), label="notion_readback.pages")
    _require_exact_keys(readback_pages, REQUIRED_PAGE_KEYS, label="notion_readback.pages")
    for key in REQUIRED_PAGE_KEYS:
        page = _require_dict(readback_pages[key], label=f"notion_readback.pages.{key}")
        label = f"notion_readback.pages.{key}"
        if page.get("page_role") != key:
            raise ValueError(f"{label}.page_role must be {key}")
        if not is_evidence_url(page.get("url")):
            raise ValueError(f"{label}.url must be a non-placeholder http(s) URL")
        if page.get("url") != pages[key]:
            raise ValueError(f"{label}.url must match the declared page URL")
        if not isinstance(page.get("title"), str) or not page["title"].strip():
            raise ValueError(f"{label}.title must be non-empty")
        if page.get("title") != titles[key]:
            raise ValueError(f"{label}.title must match the declared page title")
        expected_region_id = f"{course_id}:{key}:v1"
        if page.get("region_id") != expected_region_id:
            raise ValueError(f"{label}.region_id must be {expected_region_id}")
        if page.get("region_occurrences") != 1:
            raise ValueError(f"{label}.region_occurrences must be exactly 1")
        prewrite = _require_real_fingerprint(
            page.get("prewrite_fingerprint"), label=f"{label}.prewrite_fingerprint"
        )
        readback_fingerprint = _require_real_fingerprint(
            page.get("readback_fingerprint"), label=f"{label}.readback_fingerprint"
        )
        if prewrite != fingerprints[key]:
            raise ValueError(f"{label}.prewrite_fingerprint must match the declared fingerprint")
        if readback_fingerprint != prewrite:
            raise ValueError(f"{label}.readback_fingerprint must match prewrite_fingerprint")
        write_mode = page.get("write_mode")
        if write_mode not in {"created", "updated"}:
            raise ValueError(f"{label}.write_mode must be created or updated")
        outside_before = page.get("outside_managed_region_before_fingerprint")
        outside_after = page.get("outside_managed_region_after_fingerprint")
        if write_mode == "updated":
            outside_before = _require_real_fingerprint(
                outside_before,
                label=f"{label}.outside_managed_region_before_fingerprint",
            )
            outside_after = _require_real_fingerprint(
                outside_after,
                label=f"{label}.outside_managed_region_after_fingerprint",
            )
            if outside_before != outside_after:
                raise ValueError(
                    f"{label}.outside_managed_region_after_fingerprint must match "
                    "outside_managed_region_before_fingerprint"
                )
        elif outside_before != "not_applicable_created" or outside_after != "not_applicable_created":
            raise ValueError(
                f"{label} created pages must mark both outside-managed-region fingerprints "
                "as not_applicable_created"
            )
        page_verified_at = _timestamp(page.get("verified_at"), label=f"{label}.verified_at")
        if page_verified_at > readback_verified_at:
            raise ValueError(f"{label}.verified_at must not be later than notion_readback.verified_at")

    if len(set(pages.values())) != len(REQUIRED_PAGE_KEYS):
        raise ValueError("declared production page URLs must be unique")

    idempotency = _require_dict(readback.get("idempotency"), label="notion_readback.idempotency")
    _require_status(idempotency, "verified", label="notion_readback.idempotency")
    idempotency_verified_at = _timestamp(
        idempotency.get("verified_at"), label="notion_readback.idempotency.verified_at"
    )
    if idempotency_verified_at > readback_verified_at:
        raise ValueError(
            "notion_readback.idempotency.verified_at must not be later than notion_readback.verified_at"
        )
    if idempotency.get("course_home_matches") != 1:
        raise ValueError("notion_readback.idempotency.course_home_matches must be exactly 1")
    if idempotency.get("duplicate_page_roles") != []:
        raise ValueError("notion_readback.idempotency.duplicate_page_roles must be an empty list")

    smoke = _require_dict(receipt.get("runtime_smoke"), label="runtime_smoke")
    _require_status(smoke, "verified", label="runtime_smoke")
    smoke_verified_at = _timestamp(smoke.get("verified_at"), label="runtime_smoke.verified_at")
    if smoke_verified_at > captured_at:
        raise ValueError("runtime_smoke.verified_at must not be later than captured_at")
    if smoke_verified_at < readback_verified_at:
        raise ValueError("runtime_smoke.verified_at must not precede Notion readback verification")

    authorization = _require_dict(smoke.get("authorization"), label="runtime_smoke.authorization")
    _require_status(authorization, "authorized", label="runtime_smoke.authorization")
    authorization_at = _timestamp(
        authorization.get("recorded_at"), label="runtime_smoke.authorization.recorded_at"
    )
    if authorization_at < readback_verified_at or authorization_at > smoke_verified_at:
        raise ValueError(
            "runtime_smoke.authorization.recorded_at must fall between readback and smoke verification"
        )
    if smoke.get("isolation_mode") != SMOKE_ISOLATION_MODE:
        raise ValueError(f"runtime_smoke.isolation_mode must be {SMOKE_ISOLATION_MODE}")
    test_id = smoke.get("test_id")
    if not isinstance(test_id, str) or not SMOKE_TEST_ID_RE.fullmatch(test_id):
        raise ValueError("runtime_smoke.test_id must use the runtime_smoke_<stable-id> format")
    test_course_id = smoke.get("test_course_id")
    if (
        not isinstance(test_course_id, str)
        or not test_course_id.strip()
        or test_course_id == course_id
    ):
        raise ValueError("runtime_smoke.test_course_id must differ from the production course_id")
    test_title = smoke.get("test_course_title")
    if not isinstance(test_title, str) or "SYSTEM CHECK" not in test_title.upper():
        raise ValueError("runtime_smoke.test_course_title must identify a SYSTEM CHECK course")
    for key in ("test_course_home_url", "isolated_parent_url"):
        if not is_evidence_url(smoke.get(key)):
            raise ValueError(f"runtime_smoke.{key} must be a non-placeholder http(s) URL")
    if smoke["test_course_home_url"] == smoke["isolated_parent_url"]:
        raise ValueError("runtime_smoke test Course Home URL must differ from its parent URL")
    production_urls = set(pages.values())
    if smoke["test_course_home_url"] in production_urls:
        raise ValueError("runtime_smoke.test_course_home_url must differ from production pages")

    write_pages = _require_dict(smoke.get("write_pages"), label="runtime_smoke.write_pages")
    _require_exact_keys(write_pages, SMOKE_WRITE_KEYS, label="runtime_smoke.write_pages")
    smoke_page_urls: list[str] = []
    for key in SMOKE_WRITE_KEYS:
        page = _require_dict(write_pages[key], label=f"runtime_smoke.write_pages.{key}")
        label = f"runtime_smoke.write_pages.{key}"
        if page.get("page_role") != key:
            raise ValueError(f"{label}.page_role must be {key}")
        if not is_evidence_url(page.get("url")):
            raise ValueError(f"{label}.url must be a non-placeholder http(s) URL")
        smoke_page_urls.append(page["url"])
        if page.get("managed_region_test_id_occurrences") != 1:
            raise ValueError(f"{label}.managed_region_test_id_occurrences must be exactly 1")
        verified_at = _timestamp(page.get("verified_at"), label=f"{label}.verified_at")
        if verified_at > smoke_verified_at:
            raise ValueError(f"{label}.verified_at must not be later than runtime_smoke.verified_at")

    protected_pages = _require_dict(
        smoke.get("protected_pages"), label="runtime_smoke.protected_pages"
    )
    _require_exact_keys(protected_pages, SMOKE_NO_WRITE_KEYS, label="runtime_smoke.protected_pages")
    for key in SMOKE_NO_WRITE_KEYS:
        page = _require_dict(protected_pages[key], label=f"runtime_smoke.protected_pages.{key}")
        label = f"runtime_smoke.protected_pages.{key}"
        if page.get("page_role") != key:
            raise ValueError(f"{label}.page_role must be {key}")
        if not is_evidence_url(page.get("url")):
            raise ValueError(f"{label}.url must be a non-placeholder http(s) URL")
        smoke_page_urls.append(page["url"])
        before = _require_real_fingerprint(
            page.get("before_fingerprint"), label=f"{label}.before_fingerprint"
        )
        after = _require_real_fingerprint(
            page.get("after_fingerprint"), label=f"{label}.after_fingerprint"
        )
        if before != after:
            raise ValueError(f"{label}.after_fingerprint must match before_fingerprint")
        if page.get("managed_region_test_id_occurrences") != 0:
            raise ValueError(f"{label}.managed_region_test_id_occurrences must be 0")
        verified_at = _timestamp(page.get("verified_at"), label=f"{label}.verified_at")
        if verified_at > smoke_verified_at:
            raise ValueError(f"{label}.verified_at must not be later than runtime_smoke.verified_at")

    if len(set(smoke_page_urls)) != len(smoke_page_urls):
        raise ValueError("runtime_smoke page receipt URLs must be unique")
    if production_urls.intersection(smoke_page_urls):
        raise ValueError("runtime_smoke page receipt URLs must differ from production pages")
    if smoke["test_course_home_url"] in smoke_page_urls:
        raise ValueError("runtime_smoke test Course Home URL must differ from child page URLs")

    cleanup = _require_dict(smoke.get("cleanup"), label="runtime_smoke.cleanup")
    if cleanup.get("status") not in {"deleted-verified", "retained-explicitly"}:
        raise ValueError("runtime_smoke.cleanup.status must be deleted-verified or retained-explicitly")
    cleanup_verified_at = _timestamp(
        cleanup.get("verified_at"), label="runtime_smoke.cleanup.verified_at"
    )
    if cleanup_verified_at > smoke_verified_at:
        raise ValueError("runtime_smoke.cleanup.verified_at must not be later than smoke verification")


def build_manifest(args: argparse.Namespace) -> dict:
    if not isinstance(args.course_id, str) or not args.course_id.strip():
        raise ValueError("--course-id must be non-empty")
    if not isinstance(args.course_title, str) or not args.course_title.strip():
        raise ValueError("--course-title must be non-empty")
    _timestamp(args.created_at, label="--created-at") if args.created_at else None
    if not is_evidence_url(args.parent_url):
        raise ValueError("--parent-url must be a non-placeholder http(s) URL")

    pages = collect_exact(args.page, label="--page")
    titles = collect_exact(args.page_title, label="--page-title")
    fingerprints = collect_exact(args.page_fingerprint, label="--page-fingerprint")
    for key in REQUIRED_PAGE_KEYS:
        if not is_evidence_url(pages[key]):
            raise ValueError(f"--page URL for '{key}' must be a non-placeholder http(s) URL")
        if not titles[key].strip():
            raise ValueError(f"--page-title for '{key}' must be non-empty")
        _require_real_fingerprint(fingerprints[key], label=f"--page-fingerprint for '{key}'")

    material_coverage = load_material_coverage(Path(args.material_coverage_json))
    course_design = load_course_design(Path(args.course_design_json))
    validate_course_design(course_design, course_id=args.course_id)
    receipt, receipt_sha256 = load_evidence_receipt(Path(args.evidence_receipt_json))
    validate_evidence_receipt(
        receipt,
        course_id=args.course_id,
        pages=pages,
        titles=titles,
        fingerprints=fingerprints,
    )

    parent_by_page = {"course_home": "parent_url"}
    parent_by_page.update({key: "course_home" for key in COURSE_HOME_CHILD_KEYS})
    managed_regions = {
        key: {
            "managed_by": MANAGED_BY,
            "course_id": args.course_id,
            "region_id": f"{args.course_id}:{key}:v1",
            "update_policy": MANAGED_UPDATE_POLICY,
            "source_fingerprint": fingerprints[key],
        }
        for key in REQUIRED_PAGE_KEYS
    }
    receipt_readback = receipt["notion_readback"]
    readback_pages = {
        key: {
            "page_role": key,
            "url": receipt_readback["pages"][key]["url"],
            "title": receipt_readback["pages"][key]["title"],
            "region_id": receipt_readback["pages"][key]["region_id"],
            "region_occurrences": receipt_readback["pages"][key]["region_occurrences"],
            "prewrite_fingerprint": receipt_readback["pages"][key]["prewrite_fingerprint"],
            "readback_fingerprint": receipt_readback["pages"][key]["readback_fingerprint"],
            "write_mode": receipt_readback["pages"][key]["write_mode"],
            "outside_managed_region_before_fingerprint": receipt_readback["pages"][key][
                "outside_managed_region_before_fingerprint"
            ],
            "outside_managed_region_after_fingerprint": receipt_readback["pages"][key][
                "outside_managed_region_after_fingerprint"
            ],
            "source_fingerprint": receipt_readback["pages"][key]["readback_fingerprint"],
            "verified_at": receipt_readback["pages"][key]["verified_at"],
        }
        for key in REQUIRED_PAGE_KEYS
    }
    idempotency_receipt = receipt_readback["idempotency"]
    smoke_receipt = receipt["runtime_smoke"]

    return {
        "schema_version": SCHEMA_VERSION,
        "course_id": args.course_id,
        "course_title": args.course_title,
        "created_at": args.created_at or datetime.now(timezone.utc).isoformat(),
        "template_version": args.template_version,
        "course_design": course_design,
        "material_coverage_status": material_coverage.get("status"),
        "material_coverage": material_coverage,
        "evidence_receipt": {
            "schema_version": receipt["schema_version"],
            "evidence_source": receipt["evidence_source"],
            "captured_at": receipt["captured_at"],
            "sha256": receipt_sha256,
        },
        "notion": {
            "parent_url": args.parent_url,
            "course_home_url": pages["course_home"],
            "pages": pages,
            "parent_child": {
                "course_home_parent_url": args.parent_url,
                "children_of_course_home": list(COURSE_HOME_CHILD_KEYS),
                "parent_by_page": parent_by_page,
            },
            "managed_regions": managed_regions,
            "readback": {
                "status": receipt_readback["status"],
                "verified_at": receipt_readback["verified_at"],
                "pages": readback_pages,
            },
            "idempotency": {
                "strategy": IDEMPOTENCY_STRATEGY,
                "status": idempotency_receipt["status"],
                "verified_at": idempotency_receipt["verified_at"],
                "course_home_matches": idempotency_receipt["course_home_matches"],
                "duplicate_page_roles": idempotency_receipt["duplicate_page_roles"],
            },
        },
        "runtime_smoke": {
            "status": smoke_receipt["status"],
            "verified_at": smoke_receipt["verified_at"],
            "authorization": smoke_receipt["authorization"],
            "isolation_mode": smoke_receipt["isolation_mode"],
            "test_id": smoke_receipt["test_id"],
            "test_course_id": smoke_receipt["test_course_id"],
            "test_course_title": smoke_receipt["test_course_title"],
            "test_course_home_url": smoke_receipt["test_course_home_url"],
            "isolated_parent_url": smoke_receipt["isolated_parent_url"],
            "allowed_write_pages": list(SMOKE_WRITE_KEYS),
            "forbidden_write_pages": list(SMOKE_NO_WRITE_KEYS),
            "verified_write_pages": list(SMOKE_WRITE_KEYS),
            "verified_unchanged_pages": list(SMOKE_NO_WRITE_KEYS),
            "write_page_receipts": smoke_receipt["write_pages"],
            "protected_page_receipts": smoke_receipt["protected_pages"],
            "cleanup_status": smoke_receipt["cleanup"]["status"],
            "cleanup_verified_at": smoke_receipt["cleanup"]["verified_at"],
        },
        "validation": {
            "status": "ready_for_local_validation",
            "notes": [],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a Course Pack manifest from declared writes and an independent receipt."
    )
    parser.add_argument("--course-id", required=True)
    parser.add_argument("--course-title", required=True)
    parser.add_argument("--created-at", default="", type=parse_iso_timestamp)
    parser.add_argument("--parent-url", required=True)
    parser.add_argument("--template-version", default="v3")
    parser.add_argument("--course-design-json", required=True)
    parser.add_argument("--material-coverage-json", required=True)
    parser.add_argument("--evidence-receipt-json", required=True)
    parser.add_argument("--page", action="append", default=[], type=parse_page, required=True)
    parser.add_argument("--page-title", action="append", default=[], type=parse_page_title, required=True)
    parser.add_argument(
        "--page-fingerprint", action="append", default=[], type=parse_page_fingerprint, required=True
    )
    parser.add_argument("--output", help="Write manifest JSON to this path. Defaults to stdout.")
    args = parser.parse_args()

    if args.output:
        if Path(args.output).resolve() == Path(args.evidence_receipt_json).resolve():
            parser.error("--output must differ from --evidence-receipt-json")
        if Path(args.output).resolve() == Path(args.course_design_json).resolve():
            parser.error("--output must differ from --course-design-json")
    try:
        manifest = build_manifest(args)
    except ValueError as exc:
        parser.error(str(exc))
    output = json.dumps(manifest, ensure_ascii=False, indent=2)

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
