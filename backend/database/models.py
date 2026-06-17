import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    favorite_team = Column(String, default="None")
    notifications_enabled = Column(Boolean, default=True)
    whatsapp_enabled = Column(Boolean, default=False)
    whatsapp_phone = Column(String, nullable=True) # e.g. "+919876543210"
    whatsapp_apikey = Column(String, nullable=True) # CallMeBot API key
    daily_digest_enabled = Column(Boolean, default=True)
    preferred_language = Column(String, default="English") # English, Hindi, Spanish, etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    email_logs = relationship("EmailLog", back_populates="user")


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(String, primary_key=True, index=True) # e.g. "WC2026-M01"
    team_1 = Column(String, nullable=False)
    team_2 = Column(String, nullable=False)
    score_1 = Column(Integer, default=0)
    score_2 = Column(Integer, default=0)
    status = Column(String, default="scheduled") # scheduled, live, completed
    match_date = Column(DateTime, nullable=False)
    stadium = Column(String, nullable=False)
    group_name = Column(String, nullable=False) # e.g. "Group A"
    stats_json = Column(JSON, nullable=True) # Scorers, cards, possession, shots, etc.

    summaries = relationship("Summary", back_populates="match")
    email_logs = relationship("EmailLog", back_populates="match")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), nullable=False)
    ai_summary = Column(String, nullable=False) # 150-250 words summary
    storyline = Column(String, nullable=True)
    turning_points = Column(String, nullable=True)
    tactical_analysis = Column(String, nullable=True)
    best_player = Column(String, nullable=True)
    tournament_impact = Column(String, nullable=True)
    language = Column(String, default="English")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    match = relationship("Match", back_populates="summaries")


class Standings(Base):
    __tablename__ = "standings"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    team_name = Column(String, nullable=False)
    played = Column(Integer, default=0)
    won = Column(Integer, default=0)
    drawn = Column(Integer, default=0)
    lost = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    points = Column(Integer, default=0)


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), nullable=True) # Null for Daily Digest
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    delivery_status = Column(String, default="sent") # sent, failed
    email_type = Column(String, default="match_report") # match_report, daily_digest

    user = relationship("User", back_populates="email_logs")
    match = relationship("Match", back_populates="email_logs")
