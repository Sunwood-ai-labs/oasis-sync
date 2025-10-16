#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from typing import List


def build_lines(saved_files_raw: str, commit_performed: bool) -> List[str]:
    lines: List[str] = [
        "## ✅ サムネイルを保存しました",
        "",
        "- 保存ファイル:",
    ]

    saved_files = saved_files_raw.strip()
    if saved_files:
        lines.extend(saved_files.splitlines())

    lines.append("")

    if commit_performed:
        lines.append("変更をコミットし、デフォルトブランチへプッシュしました。")
    else:
        lines.append("差分が無かったためコミットはスキップしました。")

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the issue comment body for thumbnail ingest workflow."
    )
    parser.add_argument(
        "output_path", help="Path to write the generated Markdown comment."
    )
    args = parser.parse_args()

    saved_files_raw = os.environ.get("SAVED_FILES", "")
    commit_performed = os.environ.get("COMMIT_PERFORMED", "").lower() == "true"

    lines = build_lines(saved_files_raw, commit_performed)

    with open(args.output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
