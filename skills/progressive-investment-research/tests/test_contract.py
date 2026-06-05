from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ai-industry-chain-mini"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicReleaseContractTests(unittest.TestCase):
    def test_required_release_files_exist(self) -> None:
        for rel in [
            "README.md",
            "LICENSE",
            ".gitignore",
            "SKILL.md",
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
        ]:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_fixture_validates_strictly(self) -> None:
        validator = load_module(ROOT / "scripts" / "validate_dossier.py", "validate_dossier")
        report = validator.validate(FIXTURE, strict=True)
        self.assertTrue(report["valid"], json.dumps(report, ensure_ascii=False, indent=2))
        self.assertEqual(report["errors"], [])

    def test_fixture_represents_current_contract(self) -> None:
        expected = [
            "context.md",
            "current-synthesis.md",
            "model-map.md",
            "open-questions.md",
            "update-log.md",
            "modules/important-signals-assumptions.md",
            "models/token-demand-envelope.md",
        ]
        for rel in expected:
            self.assertTrue((FIXTURE / rel).is_file(), rel)

    def test_public_readmes_explain_usage_and_fallback(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        for phrase in [
            "它是什么",
            "它怎么运行",
            "建立一个研究工作区",
            "推荐工作流",
            "依赖与 fallback",
            "python scripts/scaffold_dossier.py",
            "fixtures/ai-industry-chain-mini",
        ]:
            self.assertIn(phrase, readme)
        for phrase in [
            "What It Is",
            "How It Works",
            "Create A Research Workspace",
            "Recommended Workflow",
            "Dependencies And Fallback",
            "python scripts/scaffold_dossier.py",
            "fixtures/ai-industry-chain-mini",
        ]:
            self.assertIn(phrase, readme_en)
        for rel in ["current-synthesis.md", "model-map.md", "open-questions.md", "update-log.md"]:
            self.assertIn(rel, readme)
            self.assertIn(rel, readme_en)

    def test_no_private_paths_or_cache_surface(self) -> None:
        forbidden = ["C:\\Users\\", "D:\\research\\", "D:\\AI_Skills\\"]
        for path in ROOT.rglob("*"):
            if path.is_dir():
                self.assertNotIn(path.name, {".pytest_cache", "__pycache__"})
                continue
            if path.suffix.lower() in {".pyc", ".pyo"}:
                self.fail(f"bytecode file should not be committed: {path}")
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle in forbidden:
                self.assertNotIn(needle, text, f"{needle} leaked in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    unittest.main()
