#!/usr/bin/env python3
"""Prepare oasis article payloads and merge Gemini-generated metadata."""

from __future__ import annotations

import argparse
import json
import sys
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


def prepare_payload(
    files: list[str],
    output_path: Path,
    gemini_output_path: Path,
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
        if front_matter and "zenn:" in front_matter and "qiita:" in front_matter:
            has_hybrid_metadata = True

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


def apply_metadata(
    payload_path: Path,
    metadata_path: Path,
    zenn_dir: Path,
    qiita_dir: Path,
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
            if not isinstance(zenn_meta, dict) or not isinstance(qiita_meta, dict):
                raise SystemExit(f"Existing front matter for {filename} must include 'zenn' and 'qiita' mappings.")
            combined_meta = parsed_meta
        else:
            generated = gemini_lookup.get(filename)
            if not generated:
                raise SystemExit(f"No Gemini metadata found for {filename}.")
            zenn_meta = generated.get("zenn")
            qiita_meta = generated.get("qiita")
            if not isinstance(zenn_meta, dict) or not isinstance(qiita_meta, dict):
                raise SystemExit(f"Gemini YAML for {filename} must include 'zenn' and 'qiita' mappings.")
            combined_meta = {"zenn": zenn_meta, "qiita": qiita_meta}

        zenn_path = (zenn_dir / rel_path).with_suffix(".md")
        qiita_path = (qiita_dir / rel_path).with_suffix(".md")
        oasis_path = oasis_dir / rel_path

        zenn_path.parent.mkdir(parents=True, exist_ok=True)
        qiita_path.parent.mkdir(parents=True, exist_ok=True)
        oasis_path.parent.mkdir(parents=True, exist_ok=True)

        zenn_path.write_text(render_front_matter(zenn_meta) + body, encoding="utf-8")
        qiita_path.write_text(render_front_matter(qiita_meta) + body, encoding="utf-8")
        oasis_path.write_text(render_front_matter(combined_meta) + body, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Collect oasis article payloads")
    prepare.add_argument("--files-json", required=True, help="JSON array of newly added files")
    prepare.add_argument("--output", required=True, help="Path to write the payload JSON")
    prepare.add_argument("--gemini-output", required=True, help="Path to write Gemini input JSON")
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
            Path(args.base_prefix),
        )
        return 0

    if args.command == "apply":
        apply_metadata(
            payload_path=Path(args.payload),
            metadata_path=Path(args.metadata),
            zenn_dir=Path(args.zenn_dir),
            qiita_dir=Path(args.qiita_dir),
            oasis_dir=Path(args.oasis_dir),
        )
        return 0

    parser.error("Unknown command")  # pragma: no cover
    return 2


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    sys.exit(main())
