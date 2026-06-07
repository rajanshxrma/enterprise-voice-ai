import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import enum

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CallStatus(str, enum.Enum):
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"

class CallOutcome(str, enum.Enum):
    SALE_CLOSED = "sale_closed"
    CLAIM_RESOLVED = "claim_resolved"
    ESCALATED_LEGAL_RISK = "escalated_legal_risk"
    ESCALATED_HUMAN = "escalated_human"
    REJECTED_PRICE = "rejected_price"
    REJECTED_OTHER = "rejected_other"
    UNKNOWN = "unknown"

class CallRecord(Base):
    __tablename__ = "call_records"
    
    id = Column(Integer, primary_key=True, index=True)
    twilio_call_sid = Column(String, unique=True, index=True)
    caller_number = Column(String)
    agent_type = Column(String) # "sales" or "claims"
    status = Column(Enum(CallStatus), default=CallStatus.RINGING)
    outcome = Column(Enum(CallOutcome), default=CallOutcome.UNKNOWN)
    duration_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Transcript(Base):
    __tablename__ = "transcripts"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("call_records.id"))
    speaker = Column(String) # "user" or "agent"
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
