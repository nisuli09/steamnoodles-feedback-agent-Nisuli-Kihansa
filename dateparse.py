
from __future__ import annotations
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import re

def parse_range(s: str, now: datetime | None = None) -> tuple[datetime, datetime]:
    """Parse strings like:
    - "last 7 days"
    - "2025-06-01 to 2025-06-15"
    Returns (start, end) datetimes (inclusive end at 23:59:59).
    """
    if now is None:
        now = datetime.now()

    s_norm = s.strip().lower()
    m = re.match(r"last\s+(\d+)\s+days", s_norm)
    if m:
        days = int(m.group(1))
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
        start = (now - timedelta(days=days-1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, end

    
    if "to" in s_norm:
        left, right = [x.strip() for x in s_norm.split("to", 1)]
        start = dateparser.parse(left).replace(hour=0, minute=0, second=0, microsecond=0)
        end = dateparser.parse(right).replace(hour=23, minute=59, second=59, microsecond=0)
        return start, end

    # fallback: single day
    dt = dateparser.parse(s_norm)
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end = dt.replace(hour=23, minute=59, second=59, microsecond=0)
    return start, end
