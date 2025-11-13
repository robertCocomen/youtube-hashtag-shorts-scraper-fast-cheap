from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)

NumberLike = Union[int, float]

def safe_int(value: Any, default: int | None = None) -> Optional[int]:
    try:
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            cleaned = value.replace(",", "").strip()
            if cleaned.endswith(" views"):
                cleaned = cleaned[:-6].strip()
            return int(float(cleaned))
    except (ValueError, TypeError):
        logger.debug("Failed to parse int from %r", value)
    return default

def compact_number(num: NumberLike) -> str:
    n = float(num)
    abs_n = abs(n)
    if abs_n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    if abs_n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if abs_n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return f"{int(n)}"

def build_view_text(view_raw: Union[str, int, float, None]) -> str:
    if view_raw is None:
        return "Unknown views"

    if isinstance(view_raw, str) and "view" in view_raw.lower():
        return view_raw.strip()

    parsed = safe_int(view_raw)
    if parsed is None:
        return str(view_raw).strip()

    return f"{compact_number(parsed)} views"

def build_record(
    idx: int,
    title: str,
    view_raw: Union[str, int, float, None],
    short_id: str,
) -> Dict[str, Any]:
    view_text = build_view_text(view_raw)
    short_url = f"https://www.youtube.com/shorts/{short_id}"
    thumb_url = f"https://i.ytimg.com/vi/{short_id}/hqdefault.jpg"

    return {
        "ID": idx,
        "Title": title,
        "View Count": view_text,
        "Short URL": short_url,
        "Thumbnail URL": thumb_url,
        "Short ID": short_id,
    }