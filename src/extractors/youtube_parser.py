from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from urllib.parse import quote_plus

from .utils_format import build_record, build_view_text

logger = logging.getLogger(__name__)

YOUTUBE_BASE = "https://www.youtube.com"

@dataclass
class ShortRecord:
    idx: int
    title: str
    view_count_text: str
    short_url: str
    thumbnail_url: str
    short_id: str

    def to_dict(self) -> dict:
        return {
            "ID": self.idx,
            "Title": self.title,
            "View Count": self.view_count_text,
            "Short URL": self.short_url,
            "Thumbnail URL": self.thumbnail_url,
            "Short ID": self.short_id,
        }

class YouTubeShortsParser:
    """
    Lightweight YouTube Shorts scraper based on public pages.

    It does not use the official API and may be sensitive to layout changes,
    but it keeps things simple and dependency-free.
    """

    def __init__(self, timeout: int = 15, user_agent: str | None = None) -> None:
        self.timeout = max(5, int(timeout))
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent
                or (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    # Public API -------------------------------------------------------------

    def search_shorts(self, hashtag: str, max_items: int = 50) -> List[ShortRecord]:
        hashtag = hashtag.lstrip("#").strip()
        if not hashtag:
            raise ValueError("Hashtag must not be empty.")

        logger.info("Searching shorts for hashtag '#%s'", hashtag)
        search_html = self._fetch_search_page(hashtag)
        short_ids = self._extract_short_ids(search_html)

        if not short_ids:
            logger.warning("No shorts IDs found for hashtag '#%s'.", hashtag)
            return []

        limited_ids = short_ids[: max(1, max_items)]
        records: List[ShortRecord] = []
        idx = 1

        for sid in limited_ids:
            try:
                meta = self._fetch_short_metadata(sid)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to fetch metadata for %s: %s", sid, exc)
                continue

            if meta is None:
                continue

            record_data = build_record(
                idx=idx,
                title=meta["title"],
                view_raw=meta.get("views_raw"),
                short_id=sid,
            )

            record = ShortRecord(
                idx=record_data["ID"],
                title=record_data["Title"],
                view_count_text=record_data["View Count"],
                short_url=record_data["Short URL"],
                thumbnail_url=record_data["Thumbnail URL"],
                short_id=record_data["Short ID"],
            )
            records.append(record)
            idx += 1

        logger.info("Finished parsing %d records.", len(records))
        return records

    # Network helpers --------------------------------------------------------

    def _fetch_search_page(self, hashtag: str) -> str:
        query = quote_plus(f"#{hashtag}")
        # sp parameter nudges results towards Shorts
        url = f"{YOUTUBE_BASE}/results?search_query={query}&sp=EgIQAQ%253D%253D"
        logger.debug("Fetching search page: %s", url)
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text

    def _fetch_short_metadata(self, short_id: str) -> Optional[dict]:
        url = f"{YOUTUBE_BASE}/shorts/{short_id}"
        logger.debug("Fetching short page: %s", url)
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        html = resp.text

        title = self._extract_title(html) or f"Short {short_id}"
        views_raw = self._extract_view_count_raw(html)

        return {
            "title": title,
            "views_raw": views_raw,
            "views_text": build_view_text(views_raw),
        }

    # Parsing helpers --------------------------------------------------------

    @staticmethod
    def _extract_short_ids(html: str) -> List[str]:
        # Extract shorts video IDs from the search results page.
        pattern = re.compile(r'"/shorts/([a-zA-Z0-9_-]{11})"', re.MULTILINE)
        ids = pattern.findall(html)

        seen = set()
        ordered_ids: List[str] = []
        for vid in ids:
            if vid not in seen:
                seen.add(vid)
                ordered_ids.append(vid)

        logger.debug("Extracted %d unique short IDs.", len(ordered_ids))
        return ordered_ids

    @staticmethod
    def _extract_title(html: str) -> Optional[str]:
        # Try standard OpenGraph title first
        m = re.search(
            r'<meta\s+property="og:title"\s+content="(.*?)"',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        if m:
            title = m.group(1).strip()
            logger.debug("Extracted og:title: %s", title)
            return title

        # Fallback: document.title
        m = re.search(
            r'"title"\s*:\s*{"runs":\s*\[\s*{"text"\s*:\s*"(.*?)"}\s*]}',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        if m:
            title = m.group(1).encode("utf-8").decode("unicode_escape").strip()
            logger.debug("Extracted JSON title: %s", title)
            return title

        return None

    @staticmethod
    def _extract_view_count_raw(html: str) -> Optional[str]:
        # Multiple fallbacks: various JSON and meta representations.
        patterns = [
            # View count renderer simple text
            r'"viewCount"\s*:\s*{\s*"videoViewCountRenderer"\s*:\s*{.*?"simpleText"\s*:\s*"(.*?)"',
            # Compact text
            r'"viewCountText"\s*:\s*{\s*"simpleText"\s*:\s*"(.*?)"',
            # Accessibility label like "7,123,456 views"
            r'"accessibilityData"\s*:\s*{\s*"label"\s*:\s*"(.*?)"',
            # Direct meta property (rare)
            r'<meta\s+itemprop="interactionCount"\s+content="(.*?)"',
        ]

        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE | re.DOTALL)
            if m:
                text = m.group(1)
                # Keep only the leading numeric / compact part and "views".
                cleaned = re.sub(r"\\u003c.*?\\u003e", "", text)
                cleaned = cleaned.replace("\n", " ").strip()
                logger.debug("Extracted raw view count: %s", cleaned)
                return cleaned

        logger.debug("No view count found in HTML.")
        return None