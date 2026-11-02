from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, func

from app.database import Base


user_role_association = Table(
    "user_role",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_user_role_user"),
        primary_key=True,
    ),
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE", name="fk_user_role_role"),
        primary_key=True,
    ),
    Column(
        "granted_at",
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    ),
    Column(
        "granted_by_user_id",
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", name="fk_user_role_granted_by"),
        nullable=True,
    ),
)
