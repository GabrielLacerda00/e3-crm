from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", back_populates="unit")
    messages = relationship("Message", back_populates="unit")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    unit = relationship("Unit", back_populates="users")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, nullable=False)
    content = Column(String, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    unit = relationship("Unit", back_populates="messages")
    