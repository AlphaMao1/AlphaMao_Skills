"""Validate the reusable and public distribution surfaces of this Skill."""

from __future__ import annotations

import argparse
from pathlib import Path


CORE_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/setup-and-capabilities.md",
    "references/workspace-init.md",
    "references/course-init.md",
    "references/validation-checklist.md",
    "assets/workspace-init/workspace_home.md",
    "assets/workspace-init/route_protocol.md",
    "assets/workspace-init/template_library.md",
    "assets/workspace-init/manual_writeback_templates.md",
    "assets/workspace-init/visual_standard.md",
    "assets/workspace-init/chatgpt_notion_plugin_setup.md",
    "assets/templates/managed_region_wrapper.md",
    "scripts/render_manifest.py",
    "scripts/validate_course_pack.py",
)

README_SECTIONS = (
    "## 它解决什么问题",
    "## 使用前必须知道的边界",
    "## 安装",
    "## 首次配置",
    "## 三种使用路径",
    "## 验证",
    "## 安全与数据边界",
    "## License",
)


def validate(root: Path, require_readme: bool = False) -> list[str]:
    errors: list[str] = []
    for relative in CORE_FILES:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty required file: {relative}")

    setup_path = root / "references/setup-and-capabilities.md"
    if setup_path.is_file():
        setup = setup_path.read_text(encoding="utf-8")
        for required in (
            "https://mcp.notion.com/mcp",
            "codex mcp login notion",
            "OAuth",
        ):
            if required not in setup:
                errors.append(f"setup contract missing required marker: {required}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        if "references/setup-and-capabilities.md" not in skill:
            errors.append("SKILL.md does not route workspace-init to setup-and-capabilities.md")

    if require_readme:
        license_path = root / "LICENSE"
        if not license_path.is_file() or "MIT License" not in license_path.read_text(encoding="utf-8"):
            errors.append("public package is missing an MIT LICENSE")
        readme_path = root / "README.md"
        if not readme_path.is_file():
            errors.append("public package is missing README.md")
        else:
            readme = readme_path.read_text(encoding="utf-8")
            for section in README_SECTIONS:
                if section not in readme:
                    errors.append(f"README.md missing section: {section}")
            if "D:\\" in readme or "C:\\Users\\" in readme:
                errors.append("README.md leaks a machine-local absolute path")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate notion-course-pack-init package surfaces.")
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--public", action="store_true", help="Also require the public README contract.")
    args = parser.parse_args()

    errors = validate(Path(args.root).resolve(), require_readme=args.public)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("SKILL PACKAGE VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
