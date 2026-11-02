from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


role_permission_association = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "granted_at",
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    ),
)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    roles = relationship(
        "Role",
        secondary=role_permission_association,
        back_populates="permissions",
    )
