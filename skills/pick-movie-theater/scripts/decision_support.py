#!/usr/bin/env python3
"""Deterministic audits for the pick-movie-theater skill.

The script intentionally does not search the web or persist cinema data. It only
calculates seat geometry and audits evidence, screening bindings, and coverage
packets assembled by the agent.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


VALID_GRADES = {"A", "B", "C", "D", "E"}
FINAL_CANDIDATE_STATUSES = {"verified", "unresolved"}
REQUIRED_COVERAGE_PASSES = {
    "format_official",
    "city_format",
    "reputation",
    "upgrade",
    "snowball",
}
REQUIRED_FORMAT_FAMILIES = {
    "imax",
    "dolby",
    "cinity",
    "cgs",
    "cinema_led",
    "screenx",
    "motion_effects",
    "premium_sound",
    "other_plf",
}
REQUIRED_SCREENING_FIELDS = {
    "film",
    "date",
    "time",
    "cinema",
    "hall",
    "ticket_label",
}
DIRECT_SCREENING_SOURCE_KINDS = {"direct_ticket_page", "official_schedule"}


def _positive_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be a positive finite number")
    return number


def _finite(name: str, value: float | None) -> float | None:
    if value is None:
        return None
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number")
    return number


def calculate_seat_geometry(
    *,
    screen_width_m: float,
    seat_distance_m: float,
    lateral_offset_m: float,
    screen_top_delta_m: float | None = None,
    screen_center_delta_m: float | None = None,
) -> dict[str, float | None]:
    """Calculate viewing geometry from known auditorium dimensions.

    Deltas are vertical distances from the viewer's eye level. Positive values
    point upward. The lateral angle preserves left/right sign.
    """

    width = _positive_finite("screen_width_m", screen_width_m)
    distance = _positive_finite("seat_distance_m", seat_distance_m)
    lateral = _finite("lateral_offset_m", lateral_offset_m)
    top_delta = _finite("screen_top_delta_m", screen_top_delta_m)
    center_delta = _finite("screen_center_delta_m", screen_center_delta_m)
    assert lateral is not None

    horizontal_fov = math.degrees(2 * math.atan(width / (2 * distance)))
    lateral_angle = math.degrees(math.atan(lateral / distance))
    top_elevation = (
        math.degrees(math.atan(top_delta / distance))
        if top_delta is not None
        else None
    )
    center_elevation = (
        math.degrees(math.atan(center_delta / distance))
        if center_delta is not None
        else None
    )

    return {
        "horizontal_fov_deg": round(horizontal_fov, 6),
        "lateral_offset_deg": round(lateral_angle, 6),
        "screen_top_elevation_deg": (
            round(top_elevation, 6) if top_elevation is not None else None
        ),
        "screen_center_elevation_deg": (
            round(center_elevation, 6) if center_elevation is not None else None
        ),
    }


def _usable_evidence(item: dict[str, Any]) -> bool:
    return (
        item.get("supports", True) is not False
        and item.get("current", True) is not False
        and item.get("superseded", False) is not True
    )


def audit_evidence(facts: list[dict[str, Any]]) -> dict[str, Any]:
    """Audit whether every decisive fact has adequate independent support.

    A/B evidence is sufficient by itself. Grade C requires two independent
    source identifiers. D/E may be retained as leads but never make a decisive
    fact ready.
    """

    results: list[dict[str, Any]] = []
    unsupported: list[str] = []

    for index, fact in enumerate(facts):
        fact_id = str(fact.get("id") or f"fact-{index + 1}")
        decisive = bool(fact.get("decisive", False))
        evidence = fact.get("evidence", [])
        if not isinstance(evidence, list):
            raise ValueError(f"{fact_id}.evidence must be a list")

        usable: list[dict[str, Any]] = []
        for item in evidence:
            if not isinstance(item, dict):
                raise ValueError(f"{fact_id}.evidence items must be objects")
            grade = str(item.get("grade", "")).upper()
            if grade not in VALID_GRADES:
                raise ValueError(f"{fact_id} has invalid evidence grade: {grade!r}")
            if _usable_evidence(item):
                usable.append({**item, "grade": grade})

        primary = [item for item in usable if item["grade"] in {"A", "B"}]
        community_ids = {
            str(item.get("source_family") or item.get("source_id"))
            for item in usable
            if item["grade"] == "C"
            and (item.get("source_family") or item.get("source_id"))
        }
        conflict_unresolved = bool(fact.get("conflict_unresolved", False))
        supported = bool(primary) or len(community_ids) >= 2
        if conflict_unresolved:
            supported = False

        if not decisive:
            status = "non_decisive"
            reason = "非决定性事实不阻塞推荐"
        elif conflict_unresolved:
            status = "blocked"
            reason = "存在尚未解决的证据冲突"
        elif primary:
            status = "supported"
            reason = "至少有一条当前有效的 A/B 级证据"
        elif len(community_ids) >= 2:
            status = "supported"
            reason = "至少两条独立且当前有效的 C 级证据相互印证"
        else:
            status = "unsupported"
            reason = "决定性事实缺少 A/B 或两条独立 C 级证据"

        if decisive and not supported:
            unsupported.append(fact_id)

        results.append(
            {
                "id": fact_id,
                "decisive": decisive,
                "status": status,
                "reason": reason,
                "usable_grades": [item["grade"] for item in usable],
                "independent_c_sources": sorted(community_ids),
            }
        )

    return {
        "ready": not unsupported,
        "unsupported_decisive_facts": unsupported,
        "facts": results,
    }


def audit_screening_bindings(packet: dict[str, Any]) -> dict[str, Any]:
    """Reject screening facts assembled across film blocks.

    Agents must retain one source block identifier per field. A valid binding
    proves that film, date, time, cinema, hall, and ticket label came from the
    same film section. Search-index snapshots may establish a lead, but they
    cannot establish current availability when the original page was not
    reopened.
    """

    expected_film = str(packet.get("expected_film") or "").strip()
    if not expected_film:
        raise ValueError("expected_film is required")

    screenings = packet.get("screenings", [])
    if not isinstance(screenings, list):
        raise ValueError("screenings must be a list")

    results: list[dict[str, Any]] = []
    invalid_ids: list[str] = []
    conditional_ids: list[str] = []

    for index, screening in enumerate(screenings):
        screening_id = f"screening-{index + 1}"
        reasons: list[str] = []
        if not isinstance(screening, dict):
            invalid_ids.append(screening_id)
            results.append(
                {
                    "id": screening_id,
                    "binding_valid": False,
                    "current_confirmable": False,
                    "recommended_status": "invalid",
                    "reasons": ["场次必须是对象"],
                }
            )
            continue

        screening_id = str(screening.get("id") or screening_id)
        missing_values = sorted(
            field
            for field in REQUIRED_SCREENING_FIELDS
            if not str(screening.get(field) or "").strip()
        )
        if missing_values:
            reasons.append("缺少场次字段：" + "、".join(missing_values))

        observed_film = str(screening.get("film") or "").strip()
        if observed_film != expected_film:
            reasons.append(
                f"影片不匹配：期望 {expected_film!r}，实际 {observed_film!r}"
            )

        field_block_ids = screening.get("field_block_ids", {})
        if not isinstance(field_block_ids, dict):
            reasons.append("field_block_ids 必须是对象")
            field_block_ids = {}
        missing_block_ids = sorted(
            field
            for field in REQUIRED_SCREENING_FIELDS
            if not str(field_block_ids.get(field) or "").strip()
        )
        if missing_block_ids:
            reasons.append(
                "缺少字段区块绑定：" + "、".join(missing_block_ids)
            )
        block_ids = {
            str(field_block_ids.get(field))
            for field in REQUIRED_SCREENING_FIELDS
            if str(field_block_ids.get(field) or "").strip()
        }
        if len(block_ids) > 1:
            reasons.append("影片、日期、时间、影院、影厅或版本来自不同页面区块")

        declared_block_id = str(screening.get("source_block_id") or "").strip()
        if not declared_block_id:
            reasons.append("缺少 source_block_id")
        elif block_ids and block_ids != {declared_block_id}:
            reasons.append("字段区块与 source_block_id 不一致")

        binding_valid = not reasons
        source_kind = str(screening.get("source_kind") or "").strip()
        page_reopened = screening.get("page_reopened") is True
        current_confirmable = (
            binding_valid
            and source_kind in DIRECT_SCREENING_SOURCE_KINDS
            and page_reopened
        )

        if not binding_valid:
            recommended_status = "invalid"
            invalid_ids.append(screening_id)
        elif current_confirmable:
            recommended_status = "current_confirmed"
        else:
            recommended_status = "conditional"
            conditional_ids.append(screening_id)
            if source_kind == "search_index_snapshot" and not page_reopened:
                reasons.append("只有搜索索引快照，原始票务页未复核")
            else:
                reasons.append("来源不足以证明当前仍可购")

        results.append(
            {
                "id": screening_id,
                "binding_valid": binding_valid,
                "current_confirmable": current_confirmable,
                "recommended_status": recommended_status,
                "reasons": reasons,
            }
        )

    return {
        "ready": not invalid_ids,
        "invalid_screening_ids": invalid_ids,
        "conditional_screening_ids": conditional_ids,
        "screenings": results,
    }


def audit_coverage(packet: dict[str, Any]) -> dict[str, Any]:
    """Audit whether a search run reached the skill's bounded saturation rule."""

    reasons: list[str] = []
    official_checked = bool(packet.get("official_relevant_checked", False))
    if not official_checked:
        reasons.append("与本片相关的官方格式入口尚未检查")

    required_passes = packet.get("required_passes", {})
    if not isinstance(required_passes, dict):
        raise ValueError("required_passes must be an object")
    missing_passes = sorted(
        name
        for name in REQUIRED_COVERAGE_PASSES
        if required_passes.get(name) is not True
    )
    if missing_passes:
        reasons.append("规定入口尚未完成：" + "、".join(missing_passes))

    format_families = packet.get("format_families", {})
    if not isinstance(format_families, dict):
        raise ValueError("format_families must be an object")
    missing_format_families = sorted(
        family
        for family in REQUIRED_FORMAT_FAMILIES
        if not isinstance(format_families.get(family), dict)
        or format_families[family].get("searched") is not True
    )
    if missing_format_families:
        reasons.append(
            "效果优先格式家族尚未逐项覆盖："
            + "、".join(missing_format_families)
        )

    discovery_passes = packet.get("discovery_passes", [])
    if not isinstance(discovery_passes, list):
        raise ValueError("discovery_passes must be a list")
    independent = [
        item
        for item in discovery_passes
        if isinstance(item, dict) and item.get("independent", False)
    ]
    last_two = independent[-2:]
    two_zero_yield = len(last_two) == 2 and all(
        int(item.get("new_candidates", -1)) == 0 for item in last_two
    )
    if not two_zero_yield:
        reasons.append("尚未取得连续两个独立补漏入口零新增")

    candidates = packet.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    pending = [
        str(item.get("id") or "unknown")
        for item in candidates
        if not isinstance(item, dict)
        or str(item.get("status", "")) not in FINAL_CANDIDATE_STATUSES
    ]
    if pending:
        reasons.append("存在尚未处理的候选")

    screening_binding_audit = packet.get("screening_binding_audit")
    invalid_screening_bindings: list[str] = []
    screening_audit_ready = False
    if screening_binding_audit is None:
        reasons.append("场次绑定审计尚未完成")
    elif not isinstance(screening_binding_audit, dict):
        raise ValueError("screening_binding_audit must be an object")
    elif screening_binding_audit.get("ready") is not True:
        raw_invalid = screening_binding_audit.get("invalid_screening_ids", [])
        if isinstance(raw_invalid, list):
            invalid_screening_bindings = [str(item) for item in raw_invalid]
        reasons.append("存在跨影片或跨区块拼接的场次")
    else:
        screening_audit_ready = True

    saturated = (
        official_checked
        and not missing_passes
        and not missing_format_families
        and two_zero_yield
        and not pending
        and screening_audit_ready
    )
    blocked_sources = packet.get("blocked_sources", [])
    if not isinstance(blocked_sources, list):
        raise ValueError("blocked_sources must be a list")

    return {
        "saturated": saturated,
        "claim": (
            "本轮优质候选搜索达到饱和"
            if saturated
            else "本轮优质候选搜索尚未达到饱和"
        ),
        "reasons": reasons,
        "blocked_sources": blocked_sources,
        "missing_format_families": missing_format_families,
        "pending_candidate_ids": pending,
        "invalid_screening_ids": invalid_screening_bindings,
        "last_two_independent_passes": [
            {
                "name": item.get("name"),
                "new_candidates": item.get("new_candidates"),
            }
            for item in last_two
        ],
    }


def _read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    evidence = subparsers.add_parser("evidence", help="audit decisive evidence")
    evidence.add_argument("--input", required=True, help="UTF-8 JSON packet")

    coverage = subparsers.add_parser("coverage", help="audit search saturation")
    coverage.add_argument("--input", required=True, help="UTF-8 JSON packet")

    screenings = subparsers.add_parser(
        "screenings", help="audit same-film screening bindings"
    )
    screenings.add_argument("--input", required=True, help="UTF-8 JSON packet")

    seat = subparsers.add_parser("seat", help="calculate seat geometry")
    seat.add_argument("--screen-width-m", required=True, type=float)
    seat.add_argument("--seat-distance-m", required=True, type=float)
    seat.add_argument("--lateral-offset-m", required=True, type=float)
    seat.add_argument("--screen-top-delta-m", type=float)
    seat.add_argument("--screen-center-delta-m", type=float)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "evidence":
            payload = _read_json(args.input)
            facts = payload.get("facts") if isinstance(payload, dict) else payload
            if not isinstance(facts, list):
                raise ValueError("evidence input must be a list or contain a facts list")
            result = audit_evidence(facts)
        elif args.command == "coverage":
            payload = _read_json(args.input)
            if not isinstance(payload, dict):
                raise ValueError("coverage input must be an object")
            result = audit_coverage(payload)
        elif args.command == "screenings":
            payload = _read_json(args.input)
            if not isinstance(payload, dict):
                raise ValueError("screenings input must be an object")
            result = audit_screening_bindings(payload)
        else:
            result = calculate_seat_geometry(
                screen_width_m=args.screen_width_m,
                seat_distance_m=args.seat_distance_m,
                lateral_offset_m=args.lateral_offset_m,
                screen_top_delta_m=args.screen_top_delta_m,
                screen_center_delta_m=args.screen_center_delta_m,
            )
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
