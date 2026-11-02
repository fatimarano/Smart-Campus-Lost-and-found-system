from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, text
from sqlalchemy.orm import relationship, synonym

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    password_hash = Column("password_hash", String(255), nullable=False)
    password = synonym("password_hash")
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text("1"))
    email_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    roles = relationship(
        "Role",
        secondary="user_role",
        primaryjoin="User.id == user_role.c.user_id",
        secondaryjoin="Role.id == user_role.c.role_id",
        back_populates="users",
    )
    reported_items = relationship(
        "ItemReport",
        back_populates="reporter",
        foreign_keys="ItemReport.reporter_user_id",
    )
    claims = relationship(
        "ItemClaim",
        back_populates="claimant",
        foreign_keys="ItemClaim.claimant_user_id",
    )
    notifications = relationship("Notification", back_populates="recipient")
    audit_events = relationship("AuditLog", back_populates="actor")
