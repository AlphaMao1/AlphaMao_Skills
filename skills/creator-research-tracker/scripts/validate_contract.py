#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd or ROOT), text=True, encoding="utf-8", errors="replace", capture_output=True)


def assert_ok(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise AssertionError(f"{label} failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def load_json_from_stdout(result: subprocess.CompletedProcess[str]) -> dict:
    text = result.stdout.strip()
    return json.loads(text)


def assert_fails(result: subprocess.CompletedProcess[str], label: str, needle: str) -> None:
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly succeeded\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    combined = result.stdout + "\n" + result.stderr
    if needle not in combined:
        raise AssertionError(f"{label} failed without expected message {needle!r}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def main() -> int:
    failures: list[str] = []
    try:
        subprocess.check_call([PY, "-m", "py_compile", *[str(p) for p in (ROOT / "scripts").glob("*.py")]])
    except Exception as exc:
        failures.append(f"py_compile failed: {exc}")

    for rel in ["README.md"]:
        if not (ROOT / rel).exists():
            failures.append(f"missing publish surface file: {rel}")
    for rel in [".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]:
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{rel} is not valid JSON: {exc}")
            continue
        if payload.get("name") != "creator-research-tracker":
            failures.append(f"{rel} name should be creator-research-tracker")
        if payload.get("skills") != "./":
            failures.append(f"{rel} skills should be ./")

    with tempfile.TemporaryDirectory(prefix="creator-tracker-") as tmp:
        tmpdir = Path(tmp)
        dossier = tmpdir / "creator-serenity"
        try:
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "scaffold_creator_dossier.py"),
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--platform",
                    "x",
                    "--locator",
                    "https://x.com/aleabitoreddit",
                    "--handle-or-channel",
                    "aleabitoreddit",
                ]
            )
            assert_ok(result, "scaffold")
            for rel in [
                "context.md",
                "current-synthesis.md",
                "model-map.md",
                "source-leads-index.md",
                "open-questions.md",
                "update-log.md",
                "modules/creator-viewpoint-system.md",
                "companies/.gitkeep",
            ]:
                if not (dossier / rel).exists():
                    failures.append(f"missing scaffold file: {rel}")

            raw_dir = dossier / "archive" / "creator-raw"
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "fetch_x_daily.py"),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--handle",
                    "aleabitoreddit",
                    "--output-dir",
                    str(raw_dir),
                    "--date",
                    "2026-06-08",
                    "--fixture-jsonl",
                    str(ROOT / "fixtures" / "serenity_x_posts.jsonl"),
                ]
            )
            assert_ok(result, "fetch_x fixture")
            fetched = load_json_from_stdout(result)
            input_jsonl = Path(fetched["output_jsonl"])
            collection_manifest = input_jsonl.with_name(f"{input_jsonl.stem}-manifest.json")
            if not input_jsonl.exists():
                failures.append("fetch_x did not write output_jsonl")

            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "build_daily_report.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--x-jsonl",
                    str(input_jsonl),
                    "--collection-manifest",
                    str(collection_manifest),
                ]
            )
            assert_ok(result, "build daily x")
            built = load_json_from_stdout(result)
            report_path = Path(built["daily_report_path"])
            report = report_path.read_text(encoding="utf-8")
            for needle in ["今日综合判断", "今日核心变化", "源更新摘要", "工作区动作"]:
                if needle not in report:
                    failures.append(f"main daily report missing {needle!r}")

            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "route_research_updates.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--daily-report",
                    str(report_path),
                    "--x-jsonl",
                    str(input_jsonl),
                ]
            )
            assert_ok(result, "route x")
            routed = load_json_from_stdout(result)
            if not routed["changed_files"]:
                failures.append("expected active source lead routing for fixture")
            for rel in ["source-leads-index.md", "model-map.md", "current-synthesis.md"]:
                text = (dossier / rel).read_text(encoding="utf-8")
                if "source lead" not in text.lower() and "Source Lead" not in text:
                    failures.append(f"{rel} did not reflect source lead routing")
            placeholder_needles = ["暂无。", "待一手验证后补齐", "该模块目前只沉淀", "仅为 source-lead-only"]
            for path in [*sorted((dossier / "modules").glob("*.md")), *sorted((dossier / "companies").glob("*.md")), dossier / "current-synthesis.md", dossier / "model-map.md"]:
                text = path.read_text(encoding="utf-8")
                for needle in placeholder_needles:
                    if needle in text:
                        failures.append(f"{path.relative_to(dossier)} contains placeholder marker: {needle}")
            update_log = (dossier / "update-log.md").read_text(encoding="utf-8")
            if "creator-source-routing" in update_log or "source-lead-routing" in update_log:
                failures.append("update-log should not record source-lead routing as model change")
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "route_research_updates.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--daily-report",
                    str(report_path),
                    "--x-jsonl",
                    str(input_jsonl),
                ]
            )
            assert_ok(result, "route x idempotent rerun")

            candidate_dossier = tmpdir / "creator-serenity-800v-candidate"
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "scaffold_creator_dossier.py"),
                    str(candidate_dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--platform",
                    "x",
                    "--locator",
                    "https://x.com/aleabitoreddit",
                    "--handle-or-channel",
                    "aleabitoreddit",
                ]
            )
            assert_ok(result, "scaffold 800v candidate")
            candidate_jsonl = tmpdir / "800v_candidate_bom.jsonl"
            candidate_jsonl.write_text(
                json.dumps(
                    {
                        "canonical_url": "https://x.com/aleabitoreddit/status/2063869376542192013",
                        "posted_at": "2026-06-08T06:22:58.000Z",
                        "captured_at": "2026-06-09T00:00:00Z",
                        "author_handle": "aleabitoreddit",
                        "source_status": "creator-original-live-chrome-source-detail-expanded",
                        "text": "Okay chat, here is your compiled list of favorite 800V DC related ideas. $NVTS $ON $POWI $XFAB $AOSL $WOLF $LFUS $VSH. These are follower recommended stock ideas, not mine.",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8-sig",
            )
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "build_daily_report.py"),
                    "--dossier",
                    str(candidate_dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--x-jsonl",
                    str(candidate_jsonl),
                ]
            )
            assert_ok(result, "build 800v candidate")
            candidate_report = Path(load_json_from_stdout(result)["daily_report_path"])
            report_text = candidate_report.read_text(encoding="utf-8")
            if "candidate_list" not in report_text or "$XFAB" not in report_text:
                failures.append("800V candidate list should remain candidate_list and preserve cashtags")
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "route_research_updates.py"),
                    "--dossier",
                    str(candidate_dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--daily-report",
                    str(candidate_report),
                    "--x-jsonl",
                    str(candidate_jsonl),
                ]
            )
            assert_ok(result, "route 800v candidate")
            for rel in [
                "companies/navitas.md",
                "companies/onsemi.md",
                "companies/power-integrations.md",
                "companies/xfab.md",
                "companies/alpha-omega-semiconductor.md",
            ]:
                if not (candidate_dossier / rel).exists():
                    failures.append(f"800V candidate route missing selected company page: {rel}")
            if (candidate_dossier / "companies" / "wolfspeed.md").exists():
                failures.append("800V candidate route should not create every long-tail company page")

            deprecated = run(
                [
                    PY,
                    str(ROOT / "scripts" / "normalize_intake.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--platform",
                    "x",
                    "--input-jsonl",
                    str(input_jsonl),
                    "--date",
                    "2026-06-08",
                    "--apply-research-actions",
                ]
            )
            assert_fails(deprecated, "deprecated normalize active write", "已废弃")

            bad_jsonl = tmpdir / "bad_translated_x.jsonl"
            bad_jsonl.write_text(
                json.dumps(
                    {
                        "canonical_url": "https://x.com/aleabitoreddit/status/999999999999999999",
                        "posted_at": "2026-06-08T05:00:00+00:00",
                        "author_handle": "aleabitoreddit",
                        "text": "Serenity @aleabitoreddit · 1分钟 翻译自 英语 显示原文 这是 X UI 自动翻译后的文本。",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            bad_manifest = tmpdir / "bad_translated_x-manifest.json"
            bad_manifest.write_text(
                json.dumps(
                    {
                        "source_id": "serenity",
                        "platform": "x",
                        "collection_status": "ok",
                        "known_gaps": ["x-ui-auto-translated; original text was not expanded"],
                        "raw_paths": [str(bad_jsonl)],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            bad_fetch = run(
                [
                    PY,
                    str(ROOT / "scripts" / "fetch_x_daily.py"),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--handle",
                    "aleabitoreddit",
                    "--output-dir",
                    str(tmpdir / "bad-raw"),
                    "--date",
                    "2026-06-08",
                    "--fixture-jsonl",
                    str(bad_jsonl),
                ]
            )
            assert_fails(bad_fetch, "fetch translated x fixture", "blocked")
            bad_build = run(
                [
                    PY,
                    str(ROOT / "scripts" / "build_daily_report.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--x-jsonl",
                    str(bad_jsonl),
                    "--collection-manifest",
                    str(bad_manifest),
                ]
            )
            assert_fails(bad_build, "build translated x", "raw 文本不合格")
            bad_route = run(
                [
                    PY,
                    str(ROOT / "scripts" / "route_research_updates.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--date",
                    "2026-06-08",
                    "--daily-report",
                    str(report_path),
                    "--x-jsonl",
                    str(bad_jsonl),
                ]
            )
            assert_fails(bad_route, "route translated x", "raw 文本不合格")
            bad_normalize = run(
                [
                    PY,
                    str(ROOT / "scripts" / "normalize_intake.py"),
                    "--dossier",
                    str(dossier),
                    "--source-id",
                    "serenity",
                    "--display-name",
                    "Serenity",
                    "--platform",
                    "x",
                    "--input-jsonl",
                    str(bad_jsonl),
                    "--date",
                    "2026-06-08",
                ]
            )
            assert_fails(bad_normalize, "normalize translated x", "raw 文本不合格")

            disqualified_rows = [
                {
                    "label": "public mirror",
                    "needle": "canonical_url 指向非 X 原帖来源",
                    "row": {
                        "canonical_url": "https://www.sotwe.com/ALEABITOREDDIT",
                        "posted_at": "unknown",
                        "author_handle": "aleabitoreddit",
                        "source_status": "secondary-mirror",
                        "summary": "Mirror summary",
                        "text": "Serenity said the 800V DC list was crowdsourced and not a recommendation.",
                    },
                },
                {
                    "label": "summary only",
                    "needle": "source_status 不合格",
                    "row": {
                        "canonical_url": "https://x.com/aleabitoreddit/status/999999999999999998",
                        "posted_at": "2026-06-08T05:10:00+00:00",
                        "author_handle": "aleabitoreddit",
                        "source_status": "summary-only",
                        "summary": "Summary-only item",
                        "text": "This is a short paraphrase without source-language raw evidence.",
                    },
                },
                {
                    "label": "search snippet",
                    "needle": "source_status 不合格",
                    "row": {
                        "canonical_url": "https://x.com/aleabitoreddit/status/999999999999999997",
                        "posted_at": "2026-06-08T05:20:00+00:00",
                        "author_handle": "aleabitoreddit",
                        "source_status": "search-snippet",
                        "summary": "Search snippet item",
                        "text": "Search result snippet: Serenity mentioned SIVE and 800V DC.",
                    },
                },
            ]
            for case in disqualified_rows:
                bad_case_jsonl = tmpdir / f"bad_{case['label'].replace(' ', '_')}.jsonl"
                bad_case_jsonl.write_text(json.dumps(case["row"], ensure_ascii=False) + "\n", encoding="utf-8")
                build_result = run(
                    [
                        PY,
                        str(ROOT / "scripts" / "build_daily_report.py"),
                        "--dossier",
                        str(dossier),
                        "--source-id",
                        "serenity",
                        "--display-name",
                        "Serenity",
                        "--date",
                        "2026-06-08",
                        "--x-jsonl",
                        str(bad_case_jsonl),
                    ]
                )
                assert_fails(build_result, f"build disqualified x {case['label']}", case["needle"])
                route_result = run(
                    [
                        PY,
                        str(ROOT / "scripts" / "route_research_updates.py"),
                        "--dossier",
                        str(dossier),
                        "--source-id",
                        "serenity",
                        "--display-name",
                        "Serenity",
                        "--date",
                        "2026-06-08",
                        "--daily-report",
                        str(report_path),
                        "--x-jsonl",
                        str(bad_case_jsonl),
                    ]
                )
                assert_fails(route_result, f"route disqualified x {case['label']}", case["needle"])
                normalize_result = run(
                    [
                        PY,
                        str(ROOT / "scripts" / "normalize_intake.py"),
                        "--dossier",
                        str(dossier),
                        "--source-id",
                        "serenity",
                        "--display-name",
                        "Serenity",
                        "--platform",
                        "x",
                        "--input-jsonl",
                        str(bad_case_jsonl),
                        "--date",
                        "2026-06-08",
                    ]
                )
                assert_fails(normalize_result, f"normalize disqualified x {case['label']}", case["needle"])
                fetch_result = run(
                    [
                        PY,
                        str(ROOT / "scripts" / "fetch_x_daily.py"),
                        "--source-id",
                        "serenity",
                        "--display-name",
                        "Serenity",
                        "--handle",
                        "aleabitoreddit",
                        "--output-dir",
                        str(tmpdir / f"bad-fetch-{case['label'].replace(' ', '-')}"),
                        "--date",
                        "2026-06-08",
                        "--fixture-jsonl",
                        str(bad_case_jsonl),
                    ]
                )
                assert_fails(fetch_result, f"fetch disqualified x {case['label']}", case["needle"])

            youtube_dossier = tmpdir / "creator-youtube-demo"
            run(
                [
                    PY,
                    str(ROOT / "scripts" / "scaffold_creator_dossier.py"),
                    str(youtube_dossier),
                    "--source-id",
                    "youtube-demo",
                    "--display-name",
                    "YouTube Demo Source",
                    "--platform",
                    "youtube",
                    "--locator",
                    "https://www.youtube.com/@channel/videos",
                ]
            )
            fixture_manifest = tmpdir / "youtube_demo_manifest.json"
            shutil.copy(ROOT / "fixtures" / "leopold_youtube_manifest.json", fixture_manifest)
            fixture_transcript_dir = tmpdir / "fixtures"
            fixture_transcript_dir.mkdir()
            shutil.copy(ROOT / "fixtures" / "leopold_transcript.txt", fixture_transcript_dir / "leopold_transcript.txt")
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "build_daily_report.py"),
                    "--dossier",
                    str(youtube_dossier),
                    "--source-id",
                    "youtube-demo",
                    "--display-name",
                    "YouTube Demo Source",
                    "--date",
                    "2026-06-08",
                    "--youtube-manifest",
                    str(fixture_manifest),
                ],
                cwd=tmpdir,
            )
            assert_ok(result, "build registered youtube")
            built_youtube = load_json_from_stdout(result)
            report = Path(built_youtube["daily_report_path"]).read_text(encoding="utf-8")
            if "model-candidate" not in report and "module-update" not in report:
                failures.append("youtube fixture did not produce research-relevant action")

            leopold_dossier = tmpdir / "creator-leopold"
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "scaffold_creator_dossier.py"),
                    str(leopold_dossier),
                    "--source-id",
                    "leopold",
                    "--display-name",
                    "Leopold",
                    "--platform",
                    "x",
                    "--locator",
                    "https://x.com/leopoldasch",
                ]
            )
            assert_ok(result, "scaffold leopold")
            blocked = run(
                [
                    PY,
                    str(ROOT / "scripts" / "build_daily_report.py"),
                    "--dossier",
                    str(leopold_dossier),
                    "--source-id",
                    "leopold",
                    "--display-name",
                    "Leopold",
                    "--date",
                    "2026-06-08",
                    "--youtube-manifest",
                    str(fixture_manifest),
                ],
                cwd=tmpdir,
            )
            assert_fails(blocked, "leopold unregistered youtube build", "未注册 youtube")
            blocked = run(
                [
                    PY,
                    str(ROOT / "scripts" / "route_research_updates.py"),
                    "--dossier",
                    str(leopold_dossier),
                    "--source-id",
                    "leopold",
                    "--display-name",
                    "Leopold",
                    "--date",
                    "2026-06-08",
                    "--daily-report",
                    str(leopold_dossier / "archive" / "creator-daily" / "leopold" / "2026-06-08.md"),
                    "--youtube-manifest",
                    str(fixture_manifest),
                ],
                cwd=tmpdir,
            )
            assert_fails(blocked, "leopold unregistered youtube route", "未注册 youtube")
            blocked = run(
                [
                    PY,
                    str(ROOT / "scripts" / "normalize_intake.py"),
                    "--dossier",
                    str(leopold_dossier),
                    "--source-id",
                    "leopold",
                    "--display-name",
                    "Leopold",
                    "--platform",
                    "youtube",
                    "--youtube-manifest",
                    str(fixture_manifest),
                    "--date",
                    "2026-06-08",
                ],
                cwd=tmpdir,
            )
            assert_fails(blocked, "leopold unregistered youtube normalize", "未注册 youtube")
            allowed_debug = run(
                [
                    PY,
                    str(ROOT / "scripts" / "normalize_intake.py"),
                    "--dossier",
                    str(youtube_dossier),
                    "--source-id",
                    "youtube-demo",
                    "--display-name",
                    "YouTube Demo Source",
                    "--platform",
                    "youtube",
                    "--youtube-manifest",
                    str(fixture_manifest),
                    "--date",
                    "2026-06-08",
                ],
                cwd=tmpdir,
            )
            assert_ok(allowed_debug, "normalize registered youtube debug")
            debug_payload = load_json_from_stdout(allowed_debug)
            if "creator-normalized-debug" not in debug_payload["daily_report_path"]:
                failures.append("normalize_intake should write debug report outside creator-daily")

            web_dossier = tmpdir / "creator-website"
            result = run(
                [
                    PY,
                    str(ROOT / "scripts" / "scaffold_creator_dossier.py"),
                    str(web_dossier),
                    "--source-id",
                    "web-demo",
                    "--display-name",
                    "Web Demo",
                    "--platform",
                    "website",
                    "--locator",
                    "https://example.com",
                ]
            )
            assert_ok(result, "scaffold website")
            web_registry = json.loads((web_dossier / "archive" / "creator-sources.json").read_text(encoding="utf-8"))
            method = web_registry["sources"][0]["platforms"][0]["collection_method"]
            if method != "manual-or-web":
                failures.append(f"website scaffold method should be manual-or-web, got {method}")

            skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
            registry_text = (ROOT / "references" / "source-registry.md").read_text(encoding="utf-8")
            forbidden = ["reuse `$x-digest`", "Prefer `x-digest`", "collection_method: x-digest"]
            for needle in forbidden:
                if needle in skill_text or needle in registry_text:
                    failures.append(f"forbidden x-digest wording remains: {needle}")
            required_contract_phrases = [
                "Codex Chrome 插件",
                "不能把它们当成 live X 验收成功",
                "Leopold 的内置来源必须先检查 X",
                "YouTube 不作为 Leopold 内置来源",
                "YouTube 是可选平台能力，不是 Serenity/Leopold 的默认预置来源",
                "collection_method: chrome-plugin-first",
                "scripts/build_daily_report.py",
                "scripts/route_research_updates.py",
                "必须合并该博主当天所有已抓平台",
                "自动拆解到工作区",
                "materiality 评分",
                "source-leads-index.md",
                "X UI 自动翻译",
                "不能生成正式日报",
            ]
            combined_contract = skill_text + "\n" + registry_text
            for needle in required_contract_phrases:
                if needle not in combined_contract:
                    failures.append(f"live collection contract missing: {needle}")

            readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
            required_readme_phrases = [
                "PaiWork",
                "progressive-investment-research",
                "build_daily_report.py",
                "route_research_updates.py",
                "source-leads-index.md",
                "companies/",
                "modules/",
                "UI 自动翻译",
                "待验证后补齐",
            ]
            for needle in required_readme_phrases:
                if needle not in readme_text:
                    failures.append(f"README missing: {needle}")
        except Exception as exc:
            failures.append(str(exc))

    if failures:
        print(json.dumps({"ok": False, "failures": failures}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "root": str(ROOT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
