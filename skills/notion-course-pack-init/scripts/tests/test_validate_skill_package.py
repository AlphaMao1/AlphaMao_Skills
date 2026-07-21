from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "validate_skill_package.py"
SPEC = importlib.util.spec_from_file_location("validate_skill_package", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ValidateSkillPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Path(__file__).resolve().parents[2]

    def test_current_core_package_passes(self) -> None:
        self.assertEqual([], MODULE.validate(self.source))

    def test_missing_workspace_asset_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skill"
            shutil.copytree(self.source, target)
            (target / "assets/workspace-init/route_protocol.md").unlink()
            errors = MODULE.validate(target)
            self.assertTrue(any("route_protocol.md" in error for error in errors))

    def test_public_readme_must_cover_user_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skill"
            shutil.copytree(self.source, target)
            (target / "README.md").write_text("# Incomplete\n", encoding="utf-8")
            errors = MODULE.validate(target, require_readme=True)
            self.assertTrue(any("三种使用路径" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
