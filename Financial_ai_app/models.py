from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="Client")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    company_name = Column(String)
    document_type = Column(String)
    uploaded_by = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text)