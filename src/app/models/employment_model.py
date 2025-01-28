from sqlalchemy import Column, Integer, String, Date, DECIMAL, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from app.utils.db import Base

class Employment(Base):
    __tablename__ = "employment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    contract_type = Column(String(50), nullable=False)
    salary = Column(DECIMAL(10, 2), nullable=False)
    position = Column(String(50), nullable=False)
    department = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    user = relationship("User", back_populates="employment")