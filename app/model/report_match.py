from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ReportMatch(Base):
    __tablename__ = "report_matches"
    __table_args__ = (
        UniqueConstraint("lost_report_id", "found_report_id", name="uq_report_match_pair"),
        CheckConstraint(
            "lost_report_id <> found_report_id",
            name="ck_report_matches_distinct_reports",
        ),
        CheckConstraint(
            "status IN ('PROPOSED', 'CONFIRMED', 'DISMISSED')",
            name="ck_report_matches_status",
        ),
        CheckConstraint(
            "confidence_score IS NULL OR confidence_score BETWEEN 0 AND 100",
            name="ck_report_matches_confidence",
        ),
    )

    id = Column(Integer, primary_key=True)
    lost_report_id = Column(
        Integer,
        ForeignKey("item_reports.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    found_report_id = Column(
        Integer,
        ForeignKey("item_reports.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_by_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status = Column(String(20), nullable=False, server_default="PROPOSED")
    confidence_score = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    lost_report = relationship(
        "ItemReport",
        back_populates="lost_matches",
        foreign_keys=[lost_report_id],
    )
    found_report = relationship(
        "ItemReport",
        back_populates="found_matches",
        foreign_keys=[found_report_id],
    )
    created_by = relationship("User", foreign_keys=[created_by_user_id])
