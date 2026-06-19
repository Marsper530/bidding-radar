"""Tender search API routes."""
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.tender import TenderBrief, TenderDetail
from backend.services.pcc_api import search_tenders, list_tenders_by_date, get_tender_detail
from backend.models.tender import Tender, TrackedTender

router = APIRouter(prefix="/api/tenders", tags=["tenders"])


@router.get("/search")
def search_tenders_endpoint(
    q: str = Query(..., min_length=1, description="搜尋關鍵字"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    """
    Search tenders from g0v PCC API.
    Results are cached in SQLite.
    """
    result = search_tenders(query=q, page=page)

    # Cache each record
    for r in result.get("records", []):
        brief = r.get("brief", {})
        tender = Tender(
            filename=r.get("filename", ""),
            date=r.get("date"),
            job_number=r.get("job_number"),
            unit_id=r.get("unit_id"),
            unit_name=r.get("unit_name"),
            title=brief.get("title"),
            category=brief.get("category"),
            tender_type=brief.get("type"),
            raw_json=r,
        )
        db.merge(tender)
    db.commit()

    return result


@router.get("/list-by-date/{date_str}")
def list_by_date_endpoint(
    date_str: str,
    db: Session = Depends(get_db),
):
    """
    List tenders by announcement date (YYYYMMDD).
    """
    result = list_tenders_by_date(date_str=date_str)

    for r in result.get("records", []):
        brief = r.get("brief", {})
        tender = Tender(
            filename=r.get("filename", ""),
            date=r.get("date"),
            job_number=r.get("job_number"),
            unit_id=r.get("unit_id"),
            unit_name=r.get("unit_name"),
            title=brief.get("title"),
            category=brief.get("category"),
            tender_type=brief.get("type"),
            raw_json=r,
        )
        db.merge(tender)
    db.commit()

    return result


@router.get("/{filename}", response_model=TenderDetail)
def get_tender_endpoint(
    filename: str,
    db: Session = Depends(get_db),
):
    """
    Get full tender detail. Fetches from PCC API if not cached.
    """
    tender = db.query(Tender).filter(Tender.filename == filename).first()

    if tender and tender.unit_id and tender.job_number:
        try:
            detail = get_tender_detail(unit_id=tender.unit_id, job_number=tender.job_number)
            tender.raw_json = detail
            db.commit()
        except Exception:
            pass

    if not tender:
        raise HTTPException(status_code=404, detail="找不到此標案")

    return tender


@router.post("/track")
def track_tender_endpoint(
    tender_filename: str,
    note: str = "",
    db: Session = Depends(get_db),
):
    """Add a tender to the user's watchlist."""
    tracked = TrackedTender(tender_filename=tender_filename, note=note)
    db.add(tracked)
    db.commit()
    db.refresh(tracked)
    return {"id": tracked.id, "status": "tracked"}


@router.delete("/track/{tender_filename}")
def untrack_tender_endpoint(
    tender_filename: str,
    db: Session = Depends(get_db),
):
    """Remove a tender from the watchlist."""
    row = db.query(TrackedTender).filter(
        TrackedTender.tender_filename == tender_filename
    ).first()
    if row:
        db.delete(row)
        db.commit()
    return {"status": "untracked"}
