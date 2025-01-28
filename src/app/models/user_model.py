from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from app.utils.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    identification_number = Column(String(20), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    id_profile = Column(Integer, ForeignKey("profile_user.id_profile"), nullable=True)

    employment = relationship("Employment", back_populates="user", cascade="all, delete-orphan")
    pdfs = relationship("CreatePDF", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("ProfileUser", back_populates="users")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")