from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def slug(path: Path) -> str:
    return path.stem


def build_index(dossier: Path) -> dict[str, object]:
    modules: dict[str, dict[str, str]] = {}
    comparisons: dict[str, dict[str, str]] = {}
    models: dict[str, dict[str, str]] = {}

    module_dir = dossier / "modules"
    if module_dir.is_dir():
        module_paths = sorted(module_dir.glob("*.md"))
    else:
        module_paths = []

    for path in module_paths:
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        heading = first_heading(text)
        entry = {"path": path.relative_to(dossier).as_posix()}
        if heading:
            entry["title"] = heading
        modules[slug(path)] = entry
        if (
            meta.get("type") == "comparison"
            or "-vs-" in path.stem
            or heading.startswith("比较：")
            or heading.startswith("Comparison:")
        ):
            comparisons[slug(path)] = entry

    model_dir = dossier / "models"
    if model_dir.is_dir():
        for path in sorted(model_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            heading = first_heading(text)
            entry = {"path": path.relative_to(dossier).as_posix()}
            if heading:
                entry["title"] = heading
            models[slug(path)] = entry

    return {
        "dossier": dossier.name,
        "source": "markdown",
        "modules": modules,
        "comparisons": comparisons,
        "models": models,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dossier", type=Path)
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print index to stdout. This is the default and kept for compatibility.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write index.json to generated/. Creates generated/ only when explicit.",
    )
    args = parser.parse_args()

    index = build_index(args.dossier)
    payload = json.dumps(index, ensure_ascii=False, indent=2)

    if args.write:
        generated = args.dossier / "generated"
        generated.mkdir(parents=True, exist_ok=True)
        (generated / "index.json").write_text(payload + "\n", encoding="utf-8")
        print(generated / "index.json")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
