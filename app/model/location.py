from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Location(Base):
    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint("campus_id", "parent_location_id", "name", name="uq_location_sibling_name"),
    )

    id = Column(Integer, primary_key=True)
    campus_id = Column(Integer, ForeignKey("campuses.id", ondelete="RESTRICT"), nullable=False)
    parent_location_id = Column(
        Integer,
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
    )
    name = Column(String(150), nullable=False)
    location_type = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)

    campus = relationship("Campus", back_populates="locations")
    parent = relationship("Location", remote_side=[id], back_populates="children")
    children = relationship("Location", back_populates="parent")
    reports = relationship("ItemReport", back_populates="location")
