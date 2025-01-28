from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.db import Base

class ProfileUser(Base):
    __tablename__ = "profile_user"

    id_profile = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    users = relationship("User", back_populates="profile")