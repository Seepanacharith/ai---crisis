from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Chat & RAG Schemas ---
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    disaster_type: Optional[str] = "all"  # "flood", "earthquake", "fire", "cyclone", "all"
    language: Optional[str] = "en"  # "en", "hi", "te"
    user_location: Optional[str] = None

class SourceCitation(BaseModel):
    source: str
    disaster_type: Optional[str] = None
    section: Optional[str] = None
    chunk_id: Optional[str] = None
    snippet: Optional[str] = None

class LatencyBreakdown(BaseModel):
    cache_lookup_ms: float = 0.0
    embedding_ms: float = 0.0
    retrieval_ms: float = 0.0
    reranking_ms: float = 0.0
    llm_ms: float = 0.0
    total_ms: float = 0.0

class ChatResponse(BaseModel):
    message_id: str
    conversation_id: str
    response: str
    language: str
    disaster_type: Optional[str] = None
    sources: List[SourceCitation] = []
    cache_hit: bool = False
    latency: LatencyBreakdown

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    language: str
    disaster_type: Optional[str] = None
    latency_ms: float
    cache_hit: bool
    sources: Optional[List[SourceCitation]] = []
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

# --- Disaster Schemas ---
class DisasterGuide(BaseModel):
    type: str
    title: str
    overview: str
    before: List[str]
    during: List[str]
    after: List[str]
    icon: str

# --- Checklist Schemas ---
class ChecklistItem(BaseModel):
    id: str
    disaster_type: str
    item: str
    completed: bool

class ChecklistSaveRequest(BaseModel):
    disaster_type: str
    items: List[Dict[str, Any]]  # [{"item": "Water", "completed": true}]

# --- Alert Schemas ---
class AlertResponse(BaseModel):
    id: str
    title: str
    disaster_type: str
    severity: str  # "Critical", "Warning", "Advisory"
    description: str
    location: str
    source: str
    issued_at: datetime

    class Config:
        from_attributes = True

# --- Emergency Services Schemas ---
class EmergencyFacility(BaseModel):
    id: str
    name: str
    type: str  # "hospital", "shelter", "police", "fire_station"
    address: str
    phone: str
    distance_km: float
    capacity: Optional[str] = None
    status: str = "Open"
    latitude: float
    longitude: float

# --- Health & Metrics Schemas ---
class HealthStatus(BaseModel):
    api: str = "healthy"
    database: str = "healthy"
    redis: str = "healthy"
    vector_db: str = "healthy"
    llm: str = "healthy"
    version: str = "1.0.0"

class BenchmarkReport(BaseModel):
    total_queries_tested: int
    no_cache_avg_latency_ms: float
    cached_avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    cache_hit_rate_pct: float
    latency_reduction_pct: float

class AdminDashboardMetrics(BaseModel):
    total_users: int
    total_questions: int
    questions_today: int
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    cache_hit_rate_pct: float
    llm_errors_count: int
    most_queried_disaster: str
    system_status: HealthStatus
