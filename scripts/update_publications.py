#!/usr/bin/env python3
"""Update data/publications.json from a public Google Scholar profile.

This script is designed for GitHub Actions. Google Scholar may throttle or
challenge automated traffic; when that happens, the script preserves the
existing curated JSON instead of deleting publications.
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PROFILE_USER = "7xD7XIUAAAAJ"
PROFILE_URL = f"https://scholar.google.com/citations?user={PROFILE_USER}&hl=en&pagesize=100"
OUT = Path("data/publications.json")
PINNED = {
    "title": "Safety in Self-Evolving LLM Agent Systems: Threats, Amplification, and Case Studies",
    "venue": "arXiv",
    "year": "2026",
    "url": "https://arxiv.org/abs/2606.23075",
}


def textify(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def fetch_profile() -> str:
    request = urllib.request.Request(
        PROFILE_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; YunhaoFengHomepageBot/1.0; +https://yunhao-feng.github.io/)",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_publications(page: str) -> list[dict[str, str]]:
    rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, flags=re.S)
    publications: list[dict[str, str]] = []
    for row in rows:
        title_match = re.search(r'<a[^>]+class="gsc_a_at"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', row, flags=re.S)
        if not title_match:
            continue
        href, title_html = title_match.groups()
        title = textify(title_html)
        metadata = [textify(x) for x in re.findall(r'<div class="gs_gray">(.*?)</div>', row, flags=re.S)]
        venue = metadata[1] if len(metadata) > 1 else ""
        year_match = re.search(r'<span class="gsc_a_h gsc_a_hc gs_ibl">(\d{4})</span>', row)
        year = year_match.group(1) if year_match else ""
        publications.append({
            "title": title,
            "venue": venue,
            "year": year,
            "url": urllib.parse.urljoin("https://scholar.google.com", html.unescape(href)),
        })
    return publications


def merge_with_pinned(publications: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    merged: list[dict[str, str]] = []
    for pub in [PINNED, *publications]:
        key = re.sub(r"\W+", "", pub["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        merged.append(pub)
    return merged


def main() -> int:
    try:
        page = fetch_profile()
        publications = parse_publications(page)
    except Exception as exc:  # noqa: BLE001 - preserve curated JSON on external failures.
        print(f"warning: failed to fetch Google Scholar profile: {exc}", file=sys.stderr)
        return 0

    if not publications:
        print("warning: no publications parsed; keeping existing JSON", file=sys.stderr)
        return 0

    OUT.write_text(json.dumps(merge_with_pinned(publications), ensure_ascii=False, indent=2) + "\n")
    print(f"updated {OUT} with {len(publications)} Google Scholar publications")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
