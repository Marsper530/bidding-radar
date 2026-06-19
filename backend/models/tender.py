"""SQLAlchemy models for bidding-radar."""
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Float, Text, Date, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base


class Tender(Base):
    """Cached tender/標案 records from g0v API."""
    __tablename__ = "tenders"

    filename = Column(String(100), primary_key=True)
    date = Column(Integer, nullable=False, index=True)
    job_number = Column(String(50))
    unit_id = Column(String(50), index=True)
    unit_name = Column(String(200))
    title = Column(String(500))
    category = Column(String(200))
    tender_type = Column(String(100))
    budget = Column(String(100))
    deadline = Column(String(50))
    raw_json = Column(JSON)
    cached_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tracking = relationship("TrackedTender", back_populates="tender", cascade="all, delete-orphan")


class Award(Base):
    """決標 records from government OpenData."""
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    org = Column(String(200), index=True)
    case_no = Column(String(100), index=True)
    title = Column(String(500))
    budget = Column(Float)
    award_price = Column(Float)
    discount_rate = Column(Float)
    award_date = Column(Date)
    winners = Column(JSON)  # list of company names
    raw_json = Column(JSON)
    imported_at = Column(DateTime, default=datetime.utcnow)

    bidders = relationship("Bidder", back_populates="award", cascade="all, delete-orphan")


class Bidder(Base):
    """投標廠商 associated with an award."""
    __tablename__ = "bidders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    award_id = Column(Integer, ForeignKey("awards.id"))
    name = Column(String(200), index=True)
    won = Column(Boolean, default=False)

    award = relationship("Award", back_populates="bidders")


class Grant(Base):
    """補助 records from open data."""
    __tablename__ = "grants"

    sid = Column(String(50), primary_key=True)
    name = Column(String(300))
    org = Column(String(200))
    region = Column(String(50))
    target = Column(Text)
    apply_url = Column(String(500))
    amount = Column(String(100))
    deadline = Column(String(100))
    raw_json = Column(JSON)
    imported_at = Column(DateTime, default=datetime.utcnow)


class CompanyProfile(Base):
    """Company profile for AI matching."""
    __tablename__ = "company_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, index=True)
    description = Column(Text)  # Free-text description of what the company does
    keywords = Column(JSON)  # List of keywords
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrackedTender(Base):
    """User's watchlist of tracked tenders."""
    __tablename__ = "tracked_tenders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tender_filename = Column(String(100), ForeignKey("tenders.filename"))
    note = Column(Text, default="")
    status = Column(String(50), default="watching")  # watching, applied, archived
    tracked_at = Column(DateTime, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="tracking")
