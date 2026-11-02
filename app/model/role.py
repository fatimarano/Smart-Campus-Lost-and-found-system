from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.model.permission import role_permission_association
from app.model.user_role import user_role_association


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    users = relationship(
        "User",
        secondary=user_role_association,
        primaryjoin="Role.id == user_role.c.role_id",
        secondaryjoin="User.id == user_role.c.user_id",
        back_populates="roles",
    )
    permissions = relationship(
        "Permission",
        secondary=role_permission_association,
        back_populates="roles",
    )
