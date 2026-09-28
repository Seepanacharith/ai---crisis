from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Float, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")  # "user" or "admin"
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    checklists = relationship("SavedChecklist", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, default="Emergency Assistance Chat")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    language = Column(String, default="en")
    disaster_type = Column(String, nullable=True)
    latency_ms = Column(Float, default=0.0)
    cache_hit = Column(Boolean, default=False)
    sources = Column(JSON, nullable=True)  # List of source document dicts
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class SavedChecklist(Base):
    __tablename__ = "saved_checklists"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    disaster_type = Column(String, nullable=False)
    item = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="checklists")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    disaster_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # "Critical", "Warning", "Advisory"
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    source = Column(String, default="National Emergency Operations Center")
    issued_at = Column(DateTime, default=datetime.utcnow)

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(String, primary_key=True, default=generate_uuid)
    endpoint = Column(String, nullable=False)
    total_latency_ms = Column(Float, nullable=False)
    embedding_latency_ms = Column(Float, default=0.0)
    retrieval_latency_ms = Column(Float, default=0.0)
    reranking_latency_ms = Column(Float, default=0.0)
    llm_latency_ms = Column(Float, default=0.0)
    cache_hit = Column(Boolean, default=False)
    is_error = Column(Boolean, default=False)
    error_type = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
