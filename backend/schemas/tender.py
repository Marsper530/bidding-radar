"""Pydantic schemas / request-response models."""
from datetime import datetime, date
from typing import Optional, Any
from pydantic import BaseModel, Field


# ── Tender schemas ──────────────────────────────────────────────────────────
class TenderBrief(BaseModel):
    """Brief tender info for list display."""
    filename: str
    date: int
    job_number: Optional[str] = None
    unit_id: Optional[str] = None
    unit_name: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    tender_type: Optional[str] = None
    budget: Optional[str] = None
    deadline: Optional[str] = None

    class Config:
        from_attributes = True


class TenderDetail(TenderBrief):
    """Full tender record with raw JSON."""
    raw_json: Optional[dict] = None
    cached_at: Optional[datetime] = None


class TenderSearchResponse(BaseModel):
    """Response from g0v search API."""
    query: str
    page: int
    total_records: int
    total_pages: int
    records: list[dict]


# ── Award schemas ───────────────────────────────────────────────────────────
class AwardBase(BaseModel):
    org: str
    case_no: str
    title: str
    budget: Optional[float] = None
    award_price: Optional[float] = None
    discount_rate: Optional[float] = None
    award_date: Optional[date] = None
    winners: Optional[list[str]] = None


class AwardRecord(AwardBase):
    id: int

    class Config:
        from_attributes = True


# ── Grant schemas ───────────────────────────────────────────────────────────
class GrantRecord(BaseModel):
    sid: str
    name: str
    org: Optional[str] = None
    region: Optional[str] = None
    target: Optional[str] = None
    apply_url: Optional[str] = None
    amount: Optional[str] = None
    deadline: Optional[str] = None

    class Config:
        from_attributes = True


# ── Company profile schemas ───────────────────────────────────────────────────
class CompanyProfileCreate(BaseModel):
    name: str
    description: str = ""
    keywords: list[str] = Field(default_factory=list)


class CompanyProfileOut(CompanyProfileCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Tracking schemas ────────────────────────────────────────────────────────
class TrackedTenderCreate(BaseModel):
    tender_filename: str
    note: str = ""


class TrackedTenderOut(BaseModel):
    id: int
    tender_filename: str
    tender: Optional[TenderBrief] = None
    note: str
    status: str
    tracked_at: datetime

    class Config:
        from_attributes = True
