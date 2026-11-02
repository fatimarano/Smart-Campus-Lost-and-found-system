from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    recipient_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    report_id = Column(
        Integer,
        ForeignKey("item_reports.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    notification_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    read_at = Column(DateTime, nullable=True)

    recipient = relationship("User", back_populates="notifications")
    report = relationship("ItemReport")
