#!/usr/bin/env python3
"""Prepare oasis article payloads and merge Gemini-generated metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - import guard for prepare step
    yaml = None


def split_front_matter(text: str) -> tuple[str | None, str]:
    """Split YAML front matter from the rest of the document."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            front = parts[1].strip("\r\n")
            body = parts[2].lstrip("\r\n")
            return front or None, body
    return None, text.lstrip("\r\n")


def ensure_trailing_newline(text: str) -> str:
    """Ensure the article body ends with a newline."""
    return text if text.endswith("\n") else text + "\n"


def remove_leading_markdown_image(text: str) -> str:
    """Remove the first Markdown image from the top of the document, if present."""
    lines = text.splitlines()
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx < len(lines):
        stripped = lines[idx].strip()
        if stripped.startswith("![") and "](" in stripped:
            del lines[: idx + 1]
            while lines and not lines[0].strip():
                lines.pop(0)
    return "\n".join(lines)


_QIITA_ID_TIMESTAMP_RE = re.compile(r"-\d{14}$")
_JST = timezone(timedelta(hours=9))


def _normalise_slug(value: str) -> str:
    """Normalise a string into a lowercase, hyphen-delimited slug."""
    slug = value.lower().replace("_", "-").replace("/", "-")
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "article"


def ensure_qiita_id(qiita_meta: dict[str, Any], relative_path: Path) -> None:
    """Ensure Qiita metadata includes a timestamped id."""
    current = qiita_meta.get("id")
    if isinstance(current, str) and _QIITA_ID_TIMESTAMP_RE.search(current):
        return

    if isinstance(current, str) and current.strip():
        base_source = current
    else:
        base_source = str(relative_path.with_suffix(""))

    base_slug = _normalise_slug(base_source)
    timestamp = datetime.now(tz=_JST).strftime("%Y%m%d%H%M%S")
    qiita_meta["id"] = f"{base_slug}-{timestamp}"


def render_front_matter(data: dict[str, Any]) -> str:
    """Serialise a dictionary into a YAML front matter block."""
    if yaml is None:
        raise SystemExit("PyYAML is required to render front matter. Install pyyaml first.")
    dumped = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).strip()
    return f"---\n{dumped}\n---\n\n"


def write_article(target_path: Path, metadata: dict[str, Any], body: str) -> None:
    """Write an article with front matter, overwriting any existing file."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    payload = render_front_matter(metadata) + body
    target_path.write_text(payload, encoding="utf-8")


def prepare_payload(
    files: list[str],
    output_path: Path,
    gemini_output_path: Path,
    needs_gemini_path: Path,
    github_output_path: Path | None,
    base_prefix: Path,
) -> None:
    """Collect article content for the newly added oasis Markdown files."""
    entries: list[dict[str, Any]] = []
    gemini_entries: list[dict[str, Any]] = []
    for rel_path in files:
        path = Path(rel_path)
        if not path.exists():
            raise SystemExit(f"Input file not found: {rel_path}")
        try:
            raw_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:  # pragma: no cover - defensive path
            raise SystemExit(f"Failed to read {rel_path} as UTF-8") from exc
        try:
            relative_path = str(path.relative_to(base_prefix))
        except ValueError as exc:
            raise SystemExit(f"File {rel_path} does not reside under {base_prefix}") from exc

        front_matter, body = split_front_matter(raw_text)
        has_hybrid_metadata = False
        if front_matter:
            has_zenn = "zenn:" in front_matter
            has_qiita = "qiita:" in front_matter
            has_wordpress = "wordpress:" in front_matter
            has_hybrid_metadata = has_zenn and has_qiita and has_wordpress

        entries.append(
            {
                "filename": rel_path,
                "relative_path": relative_path,
                "content_without_front_matter": body,
                "front_matter": front_matter,
                "has_hybrid_metadata": has_hybrid_metadata,
            }
        )

        if not has_hybrid_metadata:
            gemini_entries.append(
                {
                    "filename": rel_path,
                    "relative_path": relative_path,
                    "content_without_front_matter": body,
                }
            )

    output_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    gemini_output_path.write_text(
        json.dumps(gemini_entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    needs_gemini_path.write_text("true\n" if gemini_entries else "false\n", encoding="utf-8")
    if github_output_path is not None:
        write_github_output(
            payload_path=output_path,
            gemini_path=gemini_output_path,
            needs_path=needs_gemini_path,
            target_path=github_output_path,
        )


def apply_metadata(
    payload_path: Path,
    metadata_path: Path,
    zenn_dir: Path,
    qiita_dir: Path,
    wordpress_dir: Path,
    oasis_dir: Path,
) -> None:
    """Merge Gemini-generated metadata into oasis/zenn/qiita articles."""
    payload_data = json.loads(payload_path.read_text(encoding="utf-8"))
    lookup = {entry["filename"]: entry for entry in payload_data}

    if yaml is None:
        raise SystemExit("PyYAML is required to merge metadata. Install pyyaml first.")

    raw_metadata = metadata_path.read_text(encoding="utf-8") if metadata_path.exists() else ""
    docs = list(yaml.safe_load_all(raw_metadata)) if raw_metadata.strip() else []
    gemini_lookup: dict[str, dict[str, Any]] = {}
    for record in docs:
        if not isinstance(record, dict):
            raise SystemExit("Gemini YAML document is not a mapping.")
        filename = record.get("filename")
        if not filename:
            raise SystemExit("Gemini YAML document missing 'filename'.")
        if filename not in lookup:
            raise SystemExit(f"Gemini output references unknown filename: {filename!r}")
        gemini_lookup[filename] = record

    for payload_entry in payload_data:
        filename = payload_entry["filename"]
        body = ensure_trailing_newline(payload_entry["content_without_front_matter"])
        rel_path = Path(payload_entry["relative_path"])
        front_matter = payload_entry.get("front_matter")
        has_hybrid_metadata = payload_entry.get("has_hybrid_metadata", False)

        if has_hybrid_metadata:
            try:
                parsed_meta = yaml.safe_load(front_matter) if front_matter else None
            except yaml.YAMLError as exc:  # pragma: no cover - defensive path
                raise SystemExit(f"Failed to parse existing front matter for {filename}") from exc
            if not isinstance(parsed_meta, dict):
                raise SystemExit(f"Existing front matter for {filename} is not a mapping.")
            zenn_meta = parsed_meta.get("zenn")
            qiita_meta = parsed_meta.get("qiita")
            wordpress_meta = parsed_meta.get("wordpress")
            if not isinstance(zenn_meta, dict) or not isinstance(qiita_meta, dict) or not isinstance(wordpress_meta, dict):
                raise SystemExit(
                    f"Existing front matter for {filename} must include 'zenn', 'qiita', and 'wordpress' mappings."
                )
            # ensure_qiita_id(qiita_meta, rel_path)
            combined_meta = parsed_meta
        else:
            generated = gemini_lookup.get(filename)
            if not generated:
                raise SystemExit(f"No Gemini metadata found for {filename}.")
            zenn_meta = generated.get("zenn")
            qiita_meta = generated.get("qiita")
            wordpress_meta = generated.get("wordpress")
            if not isinstance(zenn_meta, dict) or not isinstance(qiita_meta, dict) or not isinstance(wordpress_meta, dict):
                raise SystemExit(
                    f"Gemini YAML for {filename} must include 'zenn', 'qiita', and 'wordpress' mappings."
                )
            # ensure_qiita_id(qiita_meta, rel_path)
            combined_meta = {"zenn": zenn_meta, "qiita": qiita_meta, "wordpress": wordpress_meta}

        zenn_path = (zenn_dir / rel_path).with_suffix(".md")
        qiita_path = (qiita_dir / rel_path).with_suffix(".md")
        wordpress_path = (wordpress_dir / rel_path).with_suffix(".md")
        oasis_path = oasis_dir / rel_path

        write_article(zenn_path, zenn_meta, body)
        write_article(qiita_path, qiita_meta, body)
        wordpress_body = ensure_trailing_newline(remove_leading_markdown_image(body))
        write_article(wordpress_path, wordpress_meta, wordpress_body)
        write_article(oasis_path, combined_meta, body)


def normalise_json_file(path: Path) -> str:
    """Load JSON from file and serialise into a single-line string."""
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return "[]"
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive path
        raise SystemExit(f"Failed to decode JSON from {path}") from exc
    return json.dumps(data, ensure_ascii=False)


def write_github_output(
    payload_path: Path,
    gemini_path: Path,
    needs_path: Path,
    target_path: Path,
) -> None:
    """Write formatted GitHub Actions output variables to a file."""
    payload_json = normalise_json_file(payload_path)
    gemini_json = normalise_json_file(gemini_path)
    needs_value = needs_path.read_text(encoding="utf-8").strip() or "false"

    lines = [
        f"payload={payload_json}",
        f"gemini_payload={gemini_json}",
        f"needs_gemini={needs_value}",
        "",
    ]
    target_path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Collect oasis article payloads")
    prepare.add_argument("--files-json", required=True, help="JSON array of newly added files")
    prepare.add_argument("--output", required=True, help="Path to write the payload JSON")
    prepare.add_argument("--gemini-output", required=True, help="Path to write Gemini input JSON")
    prepare.add_argument("--needs-gemini-output", required=True, help="Path to write Gemini usage flag")
    prepare.add_argument("--github-output", help="Path to write GitHub Actions output block")
    prepare.add_argument(
        "--base-prefix",
        default="articles/oasis",
        help="Expected prefix for oasis articles (default: %(default)s)",
    )

    apply = subparsers.add_parser("apply", help="Merge Gemini metadata with articles")
    apply.add_argument("--payload", required=True, help="Path to payload JSON from prepare step")
    apply.add_argument("--metadata", required=True, help="Path to Gemini-generated YAML metadata")
    apply.add_argument("--zenn-dir", required=True, help="Directory for Zenn articles")
    apply.add_argument("--qiita-dir", required=True, help="Directory for Qiita articles")
    apply.add_argument("--wordpress-dir", required=True, help="Directory for WordPress articles")
    apply.add_argument("--oasis-dir", required=True, help="Directory for Oasis source articles")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "prepare":
        files = json.loads(args.files_json)
        if not isinstance(files, list):
            raise SystemExit("files-json must decode to a list")
        prepare_payload(
            files,
            Path(args.output),
            Path(args.gemini_output),
            Path(args.needs_gemini_output),
            Path(args.github_output) if args.github_output else None,
            Path(args.base_prefix),
        )
        return 0

    if args.command == "apply":
        apply_metadata(
            payload_path=Path(args.payload),
            metadata_path=Path(args.metadata),
            zenn_dir=Path(args.zenn_dir),
            qiita_dir=Path(args.qiita_dir),
            wordpress_dir=Path(args.wordpress_dir),
            oasis_dir=Path(args.oasis_dir),
        )
        return 0

    parser.error("Unknown command")  # pragma: no cover
    return 2


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    sys.exit(main())
