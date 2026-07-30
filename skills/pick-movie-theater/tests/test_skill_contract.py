import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_ROOT / "SKILL.md"
TRACEABILITY_FILE = SKILL_ROOT / "references" / "requirements-traceability.md"
FORMAT_TAXONOMY_FILE = SKILL_ROOT / "references" / "format-taxonomy.md"
SEARCH_PLAYBOOK_FILE = SKILL_ROOT / "references" / "search-playbook.md"
DECISION_SUPPORT_FILE = SKILL_ROOT / "scripts" / "decision_support.py"
CASE_ROOT = SKILL_ROOT / "tests" / "cases"


def load_decision_support():
    spec = importlib.util.spec_from_file_location(
        "pick_movie_theater_decision_support", DECISION_SUPPORT_FILE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load decision_support.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillContractTests(unittest.TestCase):
    def test_core_skill_contract_is_runnable_without_optional_inputs(self):
        text = SKILL_FILE.read_text(encoding="utf-8")

        self.assertNotIn("TODO", text)
        self.assertIn("影片", text)
        self.assertIn("位置", text)
        self.assertIn("不要求用户提供选座截图", text)
        self.assertIn("不要求登录态", text)
        self.assertIn("不依赖付费 API", text)
        self.assertIn("具体影厅", text)
        self.assertIn("覆盖审计", text)

    def test_required_progressive_disclosure_references_exist(self):
        expected = {
            "source-and-evidence-policy.md",
            "format-taxonomy.md",
            "film-version-card.md",
            "search-playbook.md",
            "hall-and-screening.md",
            "decision-and-output.md",
            "seat-selection.md",
            "requirements-traceability.md",
        }
        actual = {path.name for path in (SKILL_ROOT / "references").glob("*.md")}

        self.assertTrue(expected.issubset(actual), expected - actual)

    def test_consumer_format_guide_distinguishes_ticket_labels(self):
        taxonomy = FORMAT_TAXONOMY_FILE.read_text(encoding="utf-8")

        for label in (
            "IMAX 70mm",
            "GT 激光",
            "Commercial Laser",
            "Laser XT",
            "氙灯数字 IMAX",
            "Dolby Cinema",
            "Dolby Atmos 厅",
            "杜比 7.1",
            "CINITY LED",
        ):
            self.assertIn(label, taxonomy)
        self.assertIn("购票标签", taxonomy)
        self.assertIn("普通用户", taxonomy)
        self.assertIn("遮幅", taxonomy)
        self.assertIn("跨格式快速选择表", taxonomy)
        for family in ("CGS", "ScreenX", "MX4D", "DTS:X", "LUXE"):
            self.assertIn(family, taxonomy)

    def test_search_playbook_requires_a_citywide_effect_first_census(self):
        playbook = SEARCH_PLAYBOOK_FILE.read_text(encoding="utf-8")

        self.assertIn("效果优先候选全集", playbook)
        self.assertIn("下辖区县", playbook)
        self.assertIn("县级市", playbook)
        self.assertIn("院线电影资料库", playbook)
        self.assertIn("只使用微博", playbook)

    def test_traceability_covers_every_spec_requirement_once(self):
        text = TRACEABILITY_FILE.read_text(encoding="utf-8")

        for number in range(1, 19):
            requirement = f"FR-{number:02d}"
            self.assertEqual(
                text.count(f"| {requirement} |"),
                1,
                f"{requirement} must appear exactly once in the traceability table",
            )

    def test_real_run_cases_preserve_actionable_degradation(self):
        no_login_case = (
            CASE_ROOT / "2026-07-29-hong-kong-odyssey-no-login.md"
        ).read_text(encoding="utf-8")
        missing_data_case = (
            CASE_ROOT / "2026-07-29-shanghai-odyssey-missing-data.md"
        ).read_text(encoding="utf-8")

        self.assertIn("无截图", no_login_case)
        self.assertIn("不使用登录态", no_login_case)
        self.assertIn("IMAX/House 12", no_login_case)
        self.assertIn("条件式场次", no_login_case)
        self.assertIn("中轴", no_login_case)
        self.assertIn("尚未达到饱和", no_login_case)
        self.assertIn("旧信息", missing_data_case)
        self.assertIn("2026-08-14", missing_data_case)
        self.assertIn("不生成具体可购场次", missing_data_case)

    def test_chengdu_regression_keeps_non_imax_effect_candidates(self):
        case = (
            CASE_ROOT / "2026-07-29-chengdu-spider-odyssey-regression.md"
        ).read_text(encoding="utf-8")

        self.assertIn("简阳东来印象", case)
        self.assertIn("CINITY LED", case)
        self.assertIn("ScreenX", case)
        self.assertIn("遮幅", case)
        self.assertIn("九个格式家族", case)
        self.assertIn("不能宣称搜索饱和", case)

    def test_avatar3_historical_case_balances_format_and_opening_stability(self):
        case = (
            CASE_ROOT / "2025-12-chengdu-avatar3-historical.md"
        ).read_text(encoding="utf-8")

        self.assertIn("东来印象", case)
        self.assertIn("4K、3D、48fps", case)
        self.assertIn("上一场已稳定放完", case)
        self.assertIn("环球中心", case)
        self.assertIn("Dolby Cinema", case)
        self.assertIn("严重闪烁并中止", case)
        self.assertIn("九个效果型格式家族覆盖", case)
        self.assertIn("第 6–8 排横向中轴", case)


class DecisionSupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.support = load_decision_support()

    def test_seat_geometry_uses_known_screen_dimensions(self):
        result = self.support.calculate_seat_geometry(
            screen_width_m=20.0,
            seat_distance_m=20.0,
            lateral_offset_m=0.0,
            screen_top_delta_m=5.0,
        )

        self.assertAlmostEqual(result["horizontal_fov_deg"], 53.130102, places=5)
        self.assertAlmostEqual(result["lateral_offset_deg"], 0.0, places=5)
        self.assertAlmostEqual(result["screen_top_elevation_deg"], 14.036243, places=5)

    def test_seat_geometry_rejects_non_positive_dimensions(self):
        with self.assertRaisesRegex(ValueError, "screen_width_m"):
            self.support.calculate_seat_geometry(
                screen_width_m=0,
                seat_distance_m=20,
                lateral_offset_m=0,
            )

        with self.assertRaisesRegex(ValueError, "seat_distance_m"):
            self.support.calculate_seat_geometry(
                screen_width_m=20,
                seat_distance_m=-1,
                lateral_offset_m=0,
            )

    def test_decisive_fact_requires_primary_or_corrobated_community_evidence(self):
        single_social = [
            {
                "id": "hall-format",
                "decisive": True,
                "evidence": [{"grade": "D", "source_id": "post-1"}],
            }
        ]
        result = self.support.audit_evidence(single_social)
        self.assertFalse(result["ready"])
        self.assertEqual(result["unsupported_decisive_facts"], ["hall-format"])

        corroborated_community = [
            {
                "id": "hall-format",
                "decisive": True,
                "evidence": [
                    {"grade": "C", "source_id": "post-1"},
                    {"grade": "C", "source_id": "post-2"},
                ],
            }
        ]
        result = self.support.audit_evidence(corroborated_community)
        self.assertTrue(result["ready"])
        self.assertEqual(result["unsupported_decisive_facts"], [])

    def test_evidence_rejects_superseded_primary_and_unresolved_conflict(self):
        facts = [
            {
                "id": "release-date",
                "decisive": True,
                "evidence": [
                    {
                        "grade": "A",
                        "source_id": "old-announcement",
                        "superseded": True,
                    },
                    {"grade": "D", "source_id": "single-repost"},
                ],
            },
            {
                "id": "hall-projector",
                "decisive": True,
                "conflict_unresolved": True,
                "evidence": [{"grade": "B", "source_id": "cinema-announcement"}],
            },
        ]

        result = self.support.audit_evidence(facts)

        self.assertFalse(result["ready"])
        self.assertEqual(
            result["unsupported_decisive_facts"],
            ["release-date", "hall-projector"],
        )

    def test_cross_platform_posts_from_one_source_family_are_not_independent(self):
        facts = [
            {
                "id": "film-ratio",
                "decisive": True,
                "evidence": [
                    {
                        "grade": "C",
                        "source_id": "weibo-post",
                        "source_family": "院线电影资料库",
                    },
                    {
                        "grade": "C",
                        "source_id": "xiaohongshu-post",
                        "source_family": "院线电影资料库",
                    },
                ],
            }
        ]

        result = self.support.audit_evidence(facts)

        self.assertFalse(result["ready"])
        self.assertEqual(
            result["facts"][0]["independent_c_sources"],
            ["院线电影资料库"],
        )

    def test_coverage_saturates_only_after_required_passes_and_two_zero_yield_passes(self):
        packet = {
            "official_relevant_checked": True,
            "required_passes": {
                "format_official": True,
                "city_format": True,
                "reputation": True,
                "upgrade": True,
                "snowball": True,
            },
            "format_families": {
                family: {"searched": True}
                for family in self.support.REQUIRED_FORMAT_FAMILIES
            },
            "discovery_passes": [
                {"name": "official", "independent": True, "new_candidates": 4},
                {"name": "upgrade", "independent": True, "new_candidates": 0},
                {"name": "snowball", "independent": True, "new_candidates": 0},
            ],
            "candidates": [
                {"id": "cinema-a", "status": "verified"},
                {"id": "cinema-b", "status": "unresolved"},
            ],
            "screening_binding_audit": {
                "ready": True,
                "invalid_screening_ids": [],
            },
            "blocked_sources": ["xiaohongshu-login"],
        }

        result = self.support.audit_coverage(packet)
        self.assertTrue(result["saturated"])
        self.assertEqual(result["blocked_sources"], ["xiaohongshu-login"])
        self.assertEqual(result["claim"], "本轮优质候选搜索达到饱和")
        self.assertNotIn("xiaohongshu-login", result["reasons"])

        packet["candidates"].append({"id": "cinema-c", "status": "pending"})
        result = self.support.audit_coverage(packet)
        self.assertFalse(result["saturated"])
        self.assertIn("存在尚未处理的候选", result["reasons"])

    def test_coverage_rejects_a_packet_that_omits_required_passes(self):
        packet = {
            "official_relevant_checked": True,
            "required_passes": {"format_official": True},
            "discovery_passes": [
                {"name": "public-social", "independent": True, "new_candidates": 0},
                {"name": "comparison", "independent": True, "new_candidates": 0},
            ],
            "candidates": [],
            "screening_binding_audit": {
                "ready": True,
                "invalid_screening_ids": [],
            },
            "blocked_sources": [],
        }

        result = self.support.audit_coverage(packet)

        self.assertFalse(result["saturated"])
        self.assertTrue(
            any(reason.startswith("规定入口尚未完成：") for reason in result["reasons"])
        )

    def test_coverage_requires_every_effect_first_format_family(self):
        packet = {
            "official_relevant_checked": True,
            "required_passes": {
                "format_official": True,
                "city_format": True,
                "reputation": True,
                "upgrade": True,
                "snowball": True,
            },
            "format_families": {
                "imax": {"searched": True},
                "dolby": {"searched": True},
            },
            "discovery_passes": [
                {"name": "upgrade", "independent": True, "new_candidates": 0},
                {"name": "snowball", "independent": True, "new_candidates": 0},
            ],
            "candidates": [],
            "screening_binding_audit": {
                "ready": True,
                "invalid_screening_ids": [],
            },
            "blocked_sources": [],
        }

        result = self.support.audit_coverage(packet)

        self.assertFalse(result["saturated"])
        self.assertTrue(
            any(reason.startswith("效果优先格式家族尚未逐项覆盖：") for reason in result["reasons"])
        )

        packet["format_families"] = {
            family: {"searched": True}
            for family in self.support.REQUIRED_FORMAT_FAMILIES
        }
        result = self.support.audit_coverage(packet)
        self.assertTrue(result["saturated"])

    def test_screening_binding_rejects_cross_film_ticket_rows(self):
        shared = {
            field: "maoyan-cinema-15618-movie-section-八仙"
            for field in self.support.REQUIRED_SCREENING_FIELDS
        }
        packet = {
            "expected_film": "奥德赛",
            "screenings": [
                {
                    "id": "heshenghui-0915",
                    "film": "八仙！",
                    "date": "2026-08-14",
                    "time": "09:15",
                    "cinema": "中影国际影城（合生汇CINITY LED店）",
                    "hall": "7号CINITYLED4K120帧全景声",
                    "ticket_label": "国语CINITY2D",
                    "source_kind": "search_index_snapshot",
                    "source_block_id": "maoyan-cinema-15618-movie-section-八仙",
                    "field_block_ids": shared,
                    "page_reopened": False,
                }
            ],
        }

        result = self.support.audit_screening_bindings(packet)

        self.assertFalse(result["ready"])
        self.assertEqual(result["invalid_screening_ids"], ["heshenghui-0915"])
        self.assertEqual(
            result["screenings"][0]["recommended_status"], "invalid"
        )

    def test_screening_binding_requires_one_source_block(self):
        field_blocks = {
            field: "odyssey-block"
            for field in self.support.REQUIRED_SCREENING_FIELDS
        }
        field_blocks["hall"] = "other-film-block"
        packet = {
            "expected_film": "奥德赛",
            "screenings": [
                {
                    "id": "mixed-row",
                    "film": "奥德赛",
                    "date": "2026-08-14",
                    "time": "09:15",
                    "cinema": "某影院",
                    "hall": "7号厅",
                    "ticket_label": "CINITY2D",
                    "source_kind": "direct_ticket_page",
                    "source_block_id": "odyssey-block",
                    "field_block_ids": field_blocks,
                    "page_reopened": True,
                }
            ],
        }

        result = self.support.audit_screening_bindings(packet)

        self.assertFalse(result["ready"])
        self.assertIn(
            "影片、日期、时间、影院、影厅或版本来自不同页面区块",
            result["screenings"][0]["reasons"],
        )

    def test_search_index_snapshot_is_only_a_conditional_screening(self):
        block_id = "odyssey-block"
        packet = {
            "expected_film": "奥德赛",
            "screenings": [
                {
                    "id": "sanlitun-1510",
                    "film": "奥德赛",
                    "date": "2026-08-01",
                    "time": "15:10",
                    "cinema": "英皇电影城（三里屯太古里店）",
                    "hall": "IMAX Laser",
                    "ticket_label": "原版IMAX2D",
                    "source_kind": "search_index_snapshot",
                    "source_block_id": block_id,
                    "field_block_ids": {
                        field: block_id
                        for field in self.support.REQUIRED_SCREENING_FIELDS
                    },
                    "page_reopened": False,
                }
            ],
        }

        result = self.support.audit_screening_bindings(packet)

        self.assertTrue(result["ready"])
        self.assertEqual(
            result["screenings"][0]["recommended_status"], "conditional"
        )
        self.assertFalse(result["screenings"][0]["current_confirmable"])

    def test_coverage_requires_a_successful_screening_binding_audit(self):
        packet = {
            "official_relevant_checked": True,
            "required_passes": {
                name: True for name in self.support.REQUIRED_COVERAGE_PASSES
            },
            "format_families": {
                family: {"searched": True}
                for family in self.support.REQUIRED_FORMAT_FAMILIES
            },
            "discovery_passes": [
                {"name": "upgrade", "independent": True, "new_candidates": 0},
                {"name": "snowball", "independent": True, "new_candidates": 0},
            ],
            "candidates": [{"id": "cinema-a", "status": "verified"}],
            "screening_binding_audit": {
                "ready": False,
                "invalid_screening_ids": ["mixed-row"],
            },
            "blocked_sources": [],
        }

        result = self.support.audit_coverage(packet)

        self.assertFalse(result["saturated"])
        self.assertEqual(result["invalid_screening_ids"], ["mixed-row"])
        self.assertIn("存在跨影片或跨区块拼接的场次", result["reasons"])

    def test_cli_returns_machine_readable_json(self):
        payload = {
            "facts": [
                {
                    "id": "film-version",
                    "decisive": True,
                    "evidence": [{"grade": "A", "source_id": "official-film-page"}],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            packet_path = Path(temp_dir) / "evidence.json"
            packet_path.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(DECISION_SUPPORT_FILE),
                    "evidence",
                    "--input",
                    str(packet_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["ready"])

    def test_screenings_cli_accepts_a_reopened_same_block_schedule(self):
        block_id = "official-odyssey-schedule"
        payload = {
            "expected_film": "奥德赛",
            "screenings": [
                {
                    "id": "official-screening",
                    "film": "奥德赛",
                    "date": "2026-08-14",
                    "time": "15:10",
                    "cinema": "某影院",
                    "hall": "IMAX GT厅",
                    "ticket_label": "原版IMAX2D",
                    "source_kind": "official_schedule",
                    "source_block_id": block_id,
                    "field_block_ids": {
                        field: block_id
                        for field in self.support.REQUIRED_SCREENING_FIELDS
                    },
                    "page_reopened": True,
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            packet_path = Path(temp_dir) / "screenings.json"
            packet_path.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(DECISION_SUPPORT_FILE),
                    "screenings",
                    "--input",
                    str(packet_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(result["ready"])
        self.assertEqual(
            result["screenings"][0]["recommended_status"],
            "current_confirmed",
        )


if __name__ == "__main__":
    unittest.main()
