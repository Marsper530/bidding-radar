"""Service for interacting with g0v PCC API (pcc-api.openfun.app)."""
import time
import httpx
from typing import Optional
from functools import lru_cache

BASE_URL = "https://pcc-api.openfun.app/api"

# Rate-limiting: minimum seconds between requests
_MIN_INTERVAL = 1.1
_last_request_time = 0.0


def _rate_limit():
    """Enforce 1 req/sec rate limit."""
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


@lru_cache(maxsize=1)
def _get_client() -> httpx.Client:
    """Return a reusable httpx client with proper headers."""
    return httpx.Client(
        timeout=30.0,
        headers={
            "User-Agent": "bidding-radar/1.0 (local tool; contact: will@example.com)",
            "Accept": "application/json",
        },
    )


def search_tenders(query: str, page: int = 1) -> dict:
    """
    Search tenders by keyword via g0v PCC API.
    
    Returns:
        {
            "query": str,
            "page": int,
            "total_records": int,
            "total_pages": int,
            "records": list[dict]
        }
    """
    _rate_limit()
    client = _get_client()
    resp = client.get(
        f"{BASE_URL}/searchbytitle",
        params={"query": query, "page": page},
    )
    resp.raise_for_status()
    return resp.json()


def list_tenders_by_date(date_str: str) -> dict:
    """
    List tenders by announcement date.
    
    Args:
        date_str: Date in YYYYMMDD format, e.g. "20260618"
    
    Returns:
        {"records": list[dict]}
    """
    _rate_limit()
    client = _get_client()
    resp = client.get(
        f"{BASE_URL}/listbydate",
        params={"date": date_str},
    )
    resp.raise_for_status()
    return resp.json()


def get_tender_detail(unit_id: str, job_number: str) -> dict:
    """
    Get full tender detail by unit_id and job_number.
    
    Args:
        unit_id: Tender unit ID (e.g. "A.21.100.33")
        job_number: Tender job number (e.g. "YY1150017-01")
    
    Returns:
        Full tender record dict
    """
    _rate_limit()
    client = _get_client()
    resp = client.get(
        f"{BASE_URL}/tender",
        params={"unit_id": unit_id, "job_number": job_number},
    )
    resp.raise_for_status()
    return resp.json()
