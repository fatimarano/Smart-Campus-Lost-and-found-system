from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Campus(Base):
    __tablename__ = "campuses"

    id = Column(Integer, primary_key=True)
    code = Column(String(30), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    address = Column(Text, nullable=True)

    locations = relationship("Location", back_populates="campus")
