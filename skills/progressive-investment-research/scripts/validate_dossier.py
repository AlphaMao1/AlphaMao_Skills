from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "model-map.md",
    "current-synthesis.md",
    "open-questions.md",
    "update-log.md",
]

REQUIRED_DIRS = [
    "modules",
]

OPTIONAL_FILES = [
    "context.md",
]

REQUIRED_HEADING_GROUPS = {
    "model-map.md": [
        ["Model Map", "模型地图"],
        ["研究边界", "Research Boundary"],
        ["核心问题", "Core Questions"],
        ["分析轴", "Analysis Axes"],
        ["模块", "Modules"],
        ["开放问题", "Open Questions"],
    ],
    "current-synthesis.md": [
        ["Current Model", "当前模型"],
        ["当前一句话判断", "One-Line Judgment"],
        ["我们知道什么", "Known"],
        ["我们不确定什么", "Unknowns"],
        ["当前冲突", "Conflicts"],
        ["下一步", "Next"],
    ],
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def has_any_heading(text: str, names: list[str]) -> bool:
    headings = [
        line.lstrip("#").strip()
        for line in text.splitlines()
        if line.startswith("#")
    ]
    return any(name in heading for heading in headings for name in names)


def first_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def validate(dossier: Path, strict: bool = False) -> dict[str, object]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    for rel in REQUIRED_FILES:
        if not (dossier / rel).is_file():
            errors.append({"code": "missing_required_file", "path": rel})

    for rel in REQUIRED_DIRS:
        if not (dossier / rel).is_dir():
            errors.append({"code": "missing_required_directory", "path": rel})

    for rel in OPTIONAL_FILES:
        if not (dossier / rel).is_file():
            warnings.append({"code": "missing_optional_context", "path": rel})

    if strict and (dossier / "team-runs").exists():
        errors.append(
            {
                "code": "discouraged_default_directory",
                "path": "team-runs",
            }
        )

    generated = dossier / "generated"
    if generated.is_dir():
        generated_files = [
            path
            for path in generated.rglob("*")
            if path.name not in {".gitkeep", "README.md"} and path.is_file()
        ]
        if generated_files:
            warnings.append(
                {
                    "code": "generated_cache_ignored",
                    "message": "Generated artifacts exist and were ignored as source of truth.",
                }
            )

    for rel, heading_groups in REQUIRED_HEADING_GROUPS.items():
        path = dossier / rel
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for heading_group in heading_groups:
                if not has_any_heading(text, heading_group):
                    issue = {
                        "code": "missing_expected_heading",
                        "path": rel,
                        "heading": " / ".join(heading_group),
                    }
                    if strict:
                        errors.append(issue)
                    else:
                        warnings.append(issue)

            if rel == "current-synthesis.md":
                heading = first_h1(text)
                if not heading.startswith("Current Model"):
                    issue = {
                        "code": "current_model_heading_required",
                        "path": rel,
                        "heading": "Current Model",
                    }
                    if strict:
                        errors.append(issue)
                    else:
                        warnings.append(issue)

    modules: list[str] = []
    comparisons: list[str] = []
    module_dir = dossier / "modules"
    if module_dir.is_dir():
        for path in sorted(module_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            meta = parse_frontmatter(text)
            modules.append(path.stem)
            if meta.get("type") == "comparison" or "# 比较：" in text or "# Comparison:" in text:
                comparisons.append(path.stem)

    model_dir = dossier / "models"
    models = sorted(path.stem for path in model_dir.glob("*.md")) if model_dir.is_dir() else []

    return {
        "valid": not errors,
        "canonical_source": "markdown",
        "errors": errors,
        "warnings": warnings,
        "modules": modules,
        "comparisons": comparisons,
        "models": models,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dossier", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    report = validate(args.dossier, strict=args.strict)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
