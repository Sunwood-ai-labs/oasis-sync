#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import io
import os
import pathlib
import re
import sys
from datetime import datetime
from typing import List, Tuple, Optional

import requests
from PIL import Image, ImageColor

# ---- Patterns ----
USER_ATTACH_PATTERN = re.compile(
    r"https://github\.com/user-attachments/assets/[0-9a-f\-]{36,}",
    re.IGNORECASE,
)

# ---- Helpers ----
def read_body(path: str) -> str:
    return pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")

def pick_section_value(markdown: str, heading_ja: str) -> Optional[str]:
    """
    GitHub Issue Forms の本文は以下のように出力される:
      ### 見出し
      入力値...
    見出しの「次ブロック（次の見出し/末尾まで）」を拾ってトリムする。
    """
    pattern = re.compile(rf"^###\s*{re.escape(heading_ja)}\s*$", re.MULTILINE)
    m = pattern.search(markdown)
    if not m:
        return None
    start = m.end()
    rest = markdown[start:]
    # 次の見出しで分割
    blocks = re.split(r"\n(?=### )", rest, maxsplit=1)
    block = blocks[0]
    # 先頭の空行を除去し、末尾をトリム
    block = re.sub(r"^\s*\n", "", block)
    return block.strip() or None

def parse_resize_preset(s: Optional[str]) -> Optional[Tuple[int, int]]:
    if not s or s.strip() == "なし":
        return None
    s = s.strip().lower()
    if "x" in s:
        w, h = s.split("x", 1)
        try:
            return int(w), int(h)
        except Exception:
            return None
    return None

def parse_hex_color(s: Optional[str]) -> Optional[Tuple[int, int, int, int]]:
    if not s:
        return None
    s = s.strip()
    try:
        r, g, b = ImageColor.getrgb(s)
        return (r, g, b, 255)
    except Exception:
        return None

def download_bytes(url: str) -> bytes:
    r = requests.get(url, allow_redirects=True, timeout=60)
    r.raise_for_status()
    return r.content

def save_png(
    data: bytes,
    out_path: pathlib.Path,
    size: Optional[Tuple[int, int]],
    bg_rgba: Optional[Tuple[int, int, int, int]],
):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(io.BytesIO(data)).convert("RGBA")

    if size:
        target_w, target_h = size
        # アスペクト比維持でフィット
        im_ratio = im.width / im.height
        tgt_ratio = target_w / target_h
        if im_ratio > tgt_ratio:
            new_w = target_w
            new_h = round(target_w / im_ratio)
        else:
            new_h = target_h
            new_w = round(target_h * im_ratio)
        resized = im.resize((new_w, new_h), Image.LANCZOS)

        # レターボックス（透明 or 指定色）
        canvas_bg = (0, 0, 0, 0) if bg_rgba is None else bg_rgba
        canvas = Image.new("RGBA", (target_w, target_h), canvas_bg)
        offset = ((target_w - new_w) // 2, (target_h - new_h) // 2)
        canvas.paste(resized, offset, mask=resized)
        im = canvas

    im.save(out_path, format="PNG", optimize=True)

def extract_all_urls(body: str, explicit_url: Optional[str]) -> List[str]:
    urls: List[str] = []
    if explicit_url:
        urls.append(explicit_url.strip())
    urls.extend(USER_ATTACH_PATTERN.findall(body))
    # 重複排除・順序維持
    seen = set()
    uniq = []
    for u in urls:
        if u not in seen:
            uniq.append(u)
            seen.add(u)
    return uniq

def sanitize_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-]", "-", s)
    s = re.sub(r"\-+", "-", s).strip("-")
    return s or "thumbnail"

def is_blank_or_no_response(s: Optional[str]) -> bool:
    if s is None:
        return True
    t = s.strip().lower()
    candidates = {
        "",
        "_no response_",
        "no response",
        "no-response",
        "n/a",
        "(none)",
        "none",
    }
    return t in candidates

# ---- Main ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-number", required=True)
    ap.add_argument("--issue-title", required=True)
    ap.add_argument("--issue-body-path", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--default-branch", required=True)
    args = ap.parse_args()

    body = read_body(args.issue_body_path)

    # 見出しの表記揺れ（・必須 有無）に両対応
    slug = (
        pick_section_value(body, "保存ファイル名（拡張子不要）")
        or pick_section_value(body, "保存ファイル名（拡張子不要・必須）")
    )
    dest_dir = pick_section_value(body, "保存ディレクトリ（相対パス）") or "images/thumbnails"
    preset = pick_section_value(body, "リサイズ（任意）")
    bg_hex = pick_section_value(body, "背景色（レターボックス用・任意）")
    src_url = pick_section_value(body, "画像 URL（任意）")

    # 🕒 空欄扱いならタイムスタンプから自動生成（例: 20251016-oasis-thumb）
    if is_blank_or_no_response(slug):
        slug = datetime.now().strftime("%Y%m%d") + "-oasis-thumb"

    slug = sanitize_slug(slug)
    size = parse_resize_preset(preset)
    bg_rgba = parse_hex_color(bg_hex)

    urls = extract_all_urls(body, src_url)
    if not urls:
        print("::warning::画像 URL も添付も見つかりませんでした。")
        # 最低限の出力（後続 step で参照）
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"dest_dir={dest_dir}\n")
            f.write("saved_files=\n")
        sys.exit(0)

    saved_paths: List[str] = []
    for i, u in enumerate(urls, 1):
        try:
            data = download_bytes(u)
        except Exception as e:
            print(f"::warning::{u} のダウンロードに失敗: {e}")
            continue

        # 複数ある場合は -1, -2 サフィックス
        name = slug if len(urls) == 1 else f"{slug}-{i}"
        out_path = pathlib.Path(dest_dir) / f"{name}.png"

        try:
            save_png(data, out_path, size=size, bg_rgba=bg_rgba)
            saved_paths.append(str(out_path).replace("\\", "/"))
        except Exception as e:
            print(f"::warning::{u} の変換/保存に失敗: {e}")

    # GitHub Actions の出力（後続 steps が参照）
    saved_list = "\n".join(f"- `{p}`" for p in saved_paths)
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write(f"dest_dir={dest_dir}\n")
        f.write(f"saved_files={saved_list}\n")

if __name__ == "__main__":
    main()
