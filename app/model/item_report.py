from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ItemReport(Base):
    __tablename__ = "item_reports"
    __table_args__ = (
        CheckConstraint(
            "report_type IN ('LOST', 'FOUND')",
            name="ck_item_reports_report_type",
        ),
        CheckConstraint(
            "status IN ('OPEN', 'UNDER_REVIEW', 'RESOLVED', 'CLOSED', 'WITHDRAWN')",
            name="ck_item_reports_status",
        ),
        Index("ix_item_reports_type_status", "report_type", "status"),
    )

    id = Column(Integer, primary_key=True)
    report_type = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, server_default="OPEN")
    reporter_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    location_id = Column(
        Integer,
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    brand = Column(String(100), nullable=True)
    color = Column(String(60), nullable=True)
    distinctive_features = Column(Text, nullable=True)
    occurred_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    reporter = relationship(
        "User",
        back_populates="reported_items",
        foreign_keys=[reporter_user_id],
    )
    category = relationship("Category", back_populates="reports")
    location = relationship("Location", back_populates="reports")
    photos = relationship(
        "ItemReportPhoto",
        back_populates="report",
        cascade="all, delete-orphan",
    )
    claims = relationship("ItemClaim", back_populates="report")
    lost_matches = relationship(
        "ReportMatch",
        back_populates="lost_report",
        foreign_keys="ReportMatch.lost_report_id",
    )
    found_matches = relationship(
        "ReportMatch",
        back_populates="found_report",
        foreign_keys="ReportMatch.found_report_id",
    )
