from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class ItemReportPhoto(Base):
    __tablename__ = "item_report_photos"

    id = Column(Integer, primary_key=True)
    report_id = Column(
        Integer,
        ForeignKey("item_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    storage_key = Column(String(500), nullable=False, unique=True)
    uploaded_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    report = relationship("ItemReport", back_populates="photos")
