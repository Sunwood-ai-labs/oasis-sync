#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from typing import List
from urllib.parse import quote


def parse_saved_paths(saved_files_raw: str) -> List[str]:
    paths: List[str] = []
    for line in saved_files_raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("-"):
            stripped = stripped[1:].strip()
        if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
            stripped = stripped[1:-1].strip()
        if stripped:
            paths.append(stripped)
    return paths


def build_lines(
    saved_files_raw: str,
    commit_performed: bool,
    repository: str,
    default_branch: str,
    server_url: str,
) -> List[str]:
    lines: List[str] = [
        "## ✅ サムネイルを保存しました",
        "",
        "- 保存ファイル:",
    ]

    saved_paths = parse_saved_paths(saved_files_raw)
    server_url = server_url.rstrip("/")
    repo = repository.strip()
    branch = default_branch.strip()

    if saved_paths:
        branch_url = quote(branch, safe="")
        for path in saved_paths:
            display = path
            if repo:
                encoded_path = "/".join(quote(part, safe="") for part in path.split("/"))
                link = f"{server_url}/{repo}/blob/{branch_url}/{encoded_path}"
                lines.append(f"  - [{display}]({link})")
            else:
                lines.append(f"  - `{display}`")
    else:
        lines.append("  - (保存ファイルはありません)")

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
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    default_branch = os.environ.get("DEFAULT_BRANCH") or os.environ.get(
        "GITHUB_REF_NAME", "main"
    )
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")

    lines = build_lines(
        saved_files_raw,
        commit_performed,
        repository,
        default_branch,
        server_url,
    )

    with open(args.output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
