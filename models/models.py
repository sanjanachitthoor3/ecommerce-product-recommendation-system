from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserPassport(Base):
    __tablename__ = "user_passports"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    state = Column(String)
    income_range = Column(String)
    language = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
