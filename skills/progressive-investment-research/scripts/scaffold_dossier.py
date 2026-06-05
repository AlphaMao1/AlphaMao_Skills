from __future__ import annotations

import argparse
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_template(name: str, title: str) -> str:
    text = (SKILL_ROOT / "templates" / name).read_text(encoding="utf-8")
    return text.replace("{{TITLE}}", title)


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scaffold(target: Path, title: str) -> None:
    target.mkdir(parents=True, exist_ok=True)

    write_if_missing(target / "context.md", load_template("context.md", title))
    write_if_missing(target / "model-map.md", load_template("model-map.md", title))
    write_if_missing(
        target / "current-synthesis.md",
        load_template("current-synthesis.md", title),
    )
    write_if_missing(
        target / "open-questions.md",
        f"# {title} 开放问题\n\n- \n",
    )
    write_if_missing(
        target / "update-log.md",
        f"# {title} 模型变化日志\n\n| 日期 | 类型 | 变化 | 影响 | 来源 |\n| --- | --- | --- | --- | --- |\n",
    )

    for rel in ["modules"]:
        directory = target / rel
        directory.mkdir(parents=True, exist_ok=True)
        write_if_missing(directory / ".gitkeep", "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    scaffold(args.target, args.title)
    print(f"已创建 dossier：{args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
