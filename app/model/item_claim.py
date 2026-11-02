from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ItemClaim(Base):
    __tablename__ = "item_claims"
    __table_args__ = (
        UniqueConstraint("report_id", "claimant_user_id", name="uq_item_claim_report_claimant"),
        CheckConstraint(
            "status IN ('SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', 'WITHDRAWN')",
            name="ck_item_claims_status",
        ),
    )

    id = Column(Integer, primary_key=True)
    report_id = Column(
        Integer,
        ForeignKey("item_reports.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    claimant_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status = Column(String(20), nullable=False, server_default="SUBMITTED")
    claim_details = Column(Text, nullable=False)
    review_note = Column(Text, nullable=True)
    reviewed_by_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    report = relationship("ItemReport", back_populates="claims")
    claimant = relationship(
        "User",
        back_populates="claims",
        foreign_keys=[claimant_user_id],
    )
    reviewer = relationship("User", foreign_keys=[reviewed_by_user_id])
