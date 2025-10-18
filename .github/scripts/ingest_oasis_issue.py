#!/usr/bin/env python3
"""Convert an Oasis Issue Form submission into an article file (and optional image)."""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from process_oasis_articles import (  # noqa: E402
    ensure_trailing_newline,
    render_front_matter,
    split_front_matter,
    _normalise_slug,
)

JST = timezone(timedelta(hours=9))

FIELD_ALIASES = {
    "記事スラッグ (拡張子不要)": "slug",
    "公開日 (オプション)": "publish_date",
    "ヘッダー画像 URL (オプション)": "header_image_url",
    "記事ヘッダー画像 URL (オプション)": "header_image_url",
    "Oasis ハイブリッド Markdown": "markdown",
}

KNOWN_FORM_LABELS = {
    "記事スラッグ (拡張子不要)",
    "公開日 (オプション)",
    "ヘッダー画像 URL (オプション)",
    "記事ヘッダー画像 URL (オプション)",
    "Oasis ハイブリッド Markdown",
    "保存ファイル名（拡張子不要）",
    "保存ファイル名（拡張子不要・必須）",
    "保存ディレクトリ（相対パス）",
    "リサイズ（任意）",
    "背景色（レターボックス用・任意）",
    "画像 URL（任意）",
    "備考（任意・🚧 実験的な `<img>` 埋め込み対応可）",
    "確認事項",
}

ASSET_URL_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/assets/\d{9,}/[A-Za-z0-9_.-]+"
)
IMAGE_MARKDOWN_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<url>[^)]+)\)")


class IssuePayloadError(RuntimeError):
    """Raised when the issue payload is invalid."""


def parse_issue_fields(issue_body: str) -> dict[str, str]:
    """Extract form fields while ignoring markdown headings inside the content."""
    lines = issue_body.replace("\r\n", "\n").splitlines()
    fields: dict[str, str] = {}
    current_label: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, current_label
        if current_label is None:
            return
        raw_value = "\n".join(buffer).strip()
        if raw_value == "_No response_":
            raw_value = ""
        fields[current_label] = raw_value
        buffer = []

    for line in lines:
        if line.startswith("### "):
            label = line[4:].strip()
            if label in KNOWN_FORM_LABELS:
                flush()
                current_label = label
                continue
        if current_label is not None:
            buffer.append(line)

    flush()
    return fields


def normalise_slug(value: str | None) -> str | None:
    if not value:
        return None
    slug = _normalise_slug(value)
    if not slug:
        return None
    if len(slug) < 12:
        slug = (slug + "-article").strip("-")
    return slug[:50]


def build_slug(
    preferred: str | None,
    publish_date: str | None,
    issue_title: str,
    issue_number: int,
    oasis_dir: Path,
) -> str:
    slug = normalise_slug(preferred)
    date_part = None
    if publish_date:
        try:
            parsed = datetime.strptime(publish_date.strip(), "%Y-%m-%d")
            date_part = parsed.strftime("%Y%m%d")
        except ValueError as exc:
            raise IssuePayloadError(
                f"公開日 '{publish_date}' は YYYY-MM-DD 形式で入力してください。"
            ) from exc
    if slug:
        if date_part and not slug.startswith(date_part):
            slug = f"{date_part}-{slug}"
    else:
        base_title = normalise_slug(issue_title)
        if not base_title:
            base_title = f"issue-{issue_number}"
        if not date_part:
            date_part = datetime.now(tz=JST).strftime("%Y%m%d")
        slug = f"{date_part}-{base_title}"
    slug = slug.strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if len(slug) > 50:
        slug = slug[:50].rstrip("-")
    while len(slug) < 12:
        slug = f"{slug}x"
    if not re.fullmatch(r"[a-z0-9_-]{12,50}", slug):
        raise IssuePayloadError(
            f"生成されたスラッグ '{slug}' が制約 (英小文字・数字・ハイフン/アンダースコア、12〜50文字) を満たしません。"
        )
    base_slug = slug
    counter = 1
    while (oasis_dir / f"{slug}.md").exists():
        slug = f"{base_slug}-{counter}"
        if len(slug) > 50:
            slug = slug[:50]
        counter += 1
    return slug


def pick_header_image_url(
    fields: dict[str, str],
    issue_body: str,
) -> str | None:
    field_url = fields.get("ヘッダー画像 URL (オプション)") or fields.get("header_image_url")
    if field_url:
        return field_url.strip()
    match = ASSET_URL_RE.search(issue_body)
    if match:
        return match.group(0)
    return None


def download_image(url: str, target_dir: Path, token: str | None, slug: str) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    headers = {"Accept": "application/octet-stream"}
    parsed = urllib.parse.urlparse(url)
    if "github.com" in parsed.netloc.lower():
        if not token:
            raise IssuePayloadError("GitHub 添付画像を取得するには GITHUB_TOKEN が必要です。")
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type", "")
        original_name = Path(parsed.path).name
    extension = Path(original_name).suffix.lower()
    if extension not in {".png", ".jpg", ".jpeg", ".webp"}:
        extension = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/webp": ".webp",
        }.get(content_type.split(";")[0], ".png")
    filename = f"{slug}{extension}"
    image_path = target_dir / filename
    image_path.write_bytes(data)
    return image_path


def update_markdown_image(body: str, new_url: str, alt: str = "") -> str:
    """Ensure body references the provided image URL near the top."""
    def replacer(match: re.Match[str]) -> str:
        existing_alt = match.group("alt")
        return f"![{existing_alt}]({new_url})"

    if IMAGE_MARKDOWN_RE.search(body):
        return IMAGE_MARKDOWN_RE.sub(replacer, body, count=1)

    lines = body.splitlines()
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    insert_line = f"![{alt}]({new_url})"
    lines[idx:idx] = [insert_line, ""]
    return "\n".join(lines)


def merge_front_matter(
    front_matter: str,
    image_url: Optional[str],
    publish_date: Optional[str],
    article_slug: Optional[str] = None,
) -> tuple[str, dict[str, Any]]:
    try:
        data = yaml.safe_load(front_matter) if front_matter else None
    except yaml.YAMLError as exc:
        raise IssuePayloadError("front matter を YAML として解釈できませんでした。") from exc
    if not isinstance(data, dict):
        raise IssuePayloadError("front matter が辞書形式ではありません。")
    if publish_date:
        data.setdefault("date", publish_date)
    if article_slug:
        data["article_slug"] = article_slug
    if image_url:
        wp = data.get("wordpress")
        if isinstance(wp, dict):
            wp["featured_image"] = image_url
    return render_front_matter(data), data


def write_article_file(
    target_path: Path,
    front_matter: str,
    body: str,
) -> bool:
    body = ensure_trailing_newline(body)
    content = front_matter + body
    if target_path.exists():
        existing = target_path.read_text(encoding="utf-8")
        if existing == content:
            return False
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--issue-body-path", required=True)
    parser.add_argument("--oasis-dir", default="articles/oasis")
    parser.add_argument("--images-root", default="generated-images")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--default-branch", required=True)
    parser.add_argument("--header-image-path", help="Relative path to existing header image")
    args = parser.parse_args(argv)

    issue_body_path = Path(args.issue_body_path)
    if not issue_body_path.exists():
        raise SystemExit(f"Issue body file not found: {issue_body_path}")
    issue_body = issue_body_path.read_text(encoding="utf-8")

    fields = parse_issue_fields(issue_body)
    markdown = fields.get("Oasis ハイブリッド Markdown") or fields.get("markdown")
    if not markdown:
        raise IssuePayloadError("Oasis ハイブリッド Markdown が入力されていません。")

    front_matter_text, body = split_front_matter(markdown)
    if front_matter_text is None:
        raise IssuePayloadError("front matter (`---` ... `---`) が見つかりません。")
    try:
        front_matter_data = yaml.safe_load(front_matter_text) if front_matter_text else None
    except yaml.YAMLError as exc:
        raise IssuePayloadError("front matter を YAML として解釈できませんでした。") from exc
    if not isinstance(front_matter_data, dict):
        raise IssuePayloadError("front matter が辞書形式ではありません。")
    front_matter_slug = front_matter_data.get("article_slug")
    if front_matter_slug is not None:
        front_matter_slug = str(front_matter_slug).strip()
        if not front_matter_slug:
            front_matter_slug = None

    slug = build_slug(
        preferred=fields.get("記事スラッグ (拡張子不要)") or fields.get("slug") or front_matter_slug,
        publish_date=fields.get("公開日 (オプション)") or fields.get("publish_date"),
        issue_title=args.issue_title,
        issue_number=args.issue_number,
        oasis_dir=Path(args.oasis_dir),
    )

    publish_date = fields.get("公開日 (オプション)") or fields.get("publish_date")

    provided_header_path = (args.header_image_path or "").strip()
    header_url = pick_header_image_url(fields, issue_body) if not provided_header_path else None
    image_rel_path: Optional[str] = None
    raw_image_url: Optional[str] = None

    provided_header_path = (args.header_image_path or "").strip()
    if provided_header_path:
        header_candidate = Path(provided_header_path)
        header_candidate_abs = header_candidate if header_candidate.is_absolute() else header_candidate
        if header_candidate_abs.exists():
            suffix = header_candidate_abs.suffix or ".png"
            dest_path = header_candidate_abs.with_name(f"{slug}{suffix}")
            if dest_path != header_candidate_abs:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                if dest_path.exists():
                    dest_path.unlink()
                header_candidate_abs.rename(dest_path)
            provided_header_path = dest_path.as_posix()

    token = os.environ.get("GITHUB_TOKEN", "")
    images_dir = Path(args.images_root) / f"issue-{args.issue_number}-{datetime.now(tz=JST).strftime('%Y%m%d%H%M%S')}"
    if provided_header_path:
        image_rel_path = Path(provided_header_path).as_posix()
        raw_image_url = f"https://raw.githubusercontent.com/{args.repo}/{args.default_branch}/{image_rel_path}"
        body = update_markdown_image(body, raw_image_url, Path(image_rel_path).stem or slug)
    elif header_url:
        image_path = download_image(header_url, images_dir, token, slug)
        image_rel_path = image_path.as_posix()
        raw_image_url = f"https://raw.githubusercontent.com/{args.repo}/{args.default_branch}/{image_rel_path}"
        body = update_markdown_image(body, raw_image_url, Path(image_rel_path).stem or slug)

    rendered_front_matter, _ = merge_front_matter(front_matter_text, raw_image_url, publish_date, slug)
    article_path = Path(args.oasis_dir) / f"{slug}.md"
    has_changes = write_article_file(article_path, rendered_front_matter, body)

    if image_rel_path and not raw_image_url:
        raw_image_url = image_rel_path

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"slug={slug}\n")
            handle.write(f"article_path={article_path.as_posix()}\n")
            handle.write(f"has_changes={'true' if has_changes else 'false'}\n")
            if image_rel_path:
                handle.write(f"image_path={image_rel_path}\n")
            if raw_image_url:
                handle.write(f"image_url={raw_image_url}\n")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except IssuePayloadError as error:
        print(f"::error::{error}", file=sys.stderr)
        sys.exit(1)
