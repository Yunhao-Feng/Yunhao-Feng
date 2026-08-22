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


def parse_publications(page: str) -> list[dict[str, object]]:
    rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, flags=re.S)
    publications: list[dict[str, object]] = []
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
        citation_match = re.search(r'<a[^>]+class="gsc_a_ac[^"]*"[^>]*>(\d+)</a>', row)
        citations = int(citation_match.group(1)) if citation_match else None
        item: dict[str, str | int] = {
            "title": title,
            "venue": venue,
            "year": year,
            "url": urllib.parse.urljoin("https://scholar.google.com", html.unescape(href)),
        }
        if citations is not None:
            item["citations"] = citations
        publications.append(item)
    return publications


def publication_key(pub: dict[str, object]) -> str:
    return re.sub(r"\W+", "", str(pub.get("title", "")).lower())


def read_existing() -> list[dict[str, object]]:
    if not OUT.exists():
        return []
    try:
        data = json.loads(OUT.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def merge_with_existing(publications: list[dict[str, object]]) -> list[dict[str, object]]:
    """Preserve curated homepage fields while filling in fresh Scholar data."""
    existing = read_existing()
    by_key = {publication_key(pub): pub for pub in publications}
    merged: list[dict[str, object]] = []
    seen: set[str] = set()

    for curated in existing:
        key = publication_key(curated)
        if not key:
            continue
        scholar = by_key.get(key, {})
        item = dict(curated)
        for field in ("citations", "year"):
            if scholar.get(field) not in (None, ""):
                item[field] = scholar[field]
        if "scholar_url" not in item and scholar.get("url"):
            item["scholar_url"] = scholar["url"]
        merged.append(item)
        seen.add(key)

    for pub in publications:
        key = publication_key(pub)
        if key and key not in seen:
            merged.append(pub)
            seen.add(key)
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

    OUT.write_text(json.dumps(merge_with_existing(publications), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {OUT} with {len(publications)} Google Scholar publications")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
