#!/usr/bin/env python3
"""Generate issue comment for combined Oasis article and thumbnail workflow."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from urllib.parse import quote

from write_thumbnail_comment import parse_saved_paths


def build_comment() -> str:
    saved_files_raw = os.environ.get("SAVED_FILES", "")
    article_path = os.environ.get("ARTICLE_PATH", "")
    article_image_url = os.environ.get("ARTICLE_IMAGE_URL", "")
    commit_performed = os.environ.get("COMMIT_PERFORMED", "").lower() == "true"
    article_image_path = os.environ.get("ARTICLE_IMAGE_PATH", "").strip()
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    default_branch = os.environ.get("DEFAULT_BRANCH", "main")
    server_raw = "https://raw.githubusercontent.com"

    saved_paths = parse_saved_paths(saved_files_raw)
    filtered_paths: list[str] = []
    for rel_path in saved_paths:
        path_obj = Path(rel_path)
        if path_obj.exists():
            filtered_paths.append(rel_path)
    saved_paths = filtered_paths
    if article_image_path:
        if article_image_path in saved_paths:
            saved_paths.remove(article_image_path)
        saved_paths.insert(0, article_image_path)

    comment_lines: list[str] = [
        "## ✅ Oasis記事とサムネイルを登録しました",
        "",
    ]

    if article_path:
        comment_lines.append(f"- 記事ファイル: `{article_path}`")
    if article_image_url:
        comment_lines.append(f"- 記事ヘッダー画像: {article_image_url}")

    comment_lines.append("- サムネイル:")
    if saved_paths and repository:
        branch_encoded = quote(default_branch, safe="")
        for rel_path in saved_paths:
            encoded_path = "/".join(quote(part, safe="") for part in rel_path.split("/"))
            link = f"{server_raw}/{repository}/{branch_encoded}/{encoded_path}"
            comment_lines.append(f"  - [{rel_path}]({link})")
    elif saved_paths:
        for rel_path in saved_paths:
            comment_lines.append(f"  - `{rel_path}`")
    else:
        comment_lines.append("  - (保存されたサムネイルはありません)")

    comment_lines.append("")
    if commit_performed:
        comment_lines.append("変更をコミットし、デフォルトブランチへプッシュしました。")
    else:
        comment_lines.append("差分が検出されなかったためコミットはスキップしました。")

    comment_lines.append("")
    return "\n".join(comment_lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write combined Oasis article + thumbnail workflow comment."
    )
    parser.add_argument("output_path", help="Path to write the generated Markdown comment.")
    args = parser.parse_args()

    content = build_comment()
    with open(args.output_path, "w", encoding="utf-8") as handle:
        handle.write(content)


if __name__ == "__main__":
    main()
