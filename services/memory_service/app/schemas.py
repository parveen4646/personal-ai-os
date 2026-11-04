"""HTTP request and response models for the Memory Service."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .models import MemoryType


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=20_000)
    memory_type: MemoryType
    user_id: str = Field(default="default", min_length=1, max_length=255)
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: dict[str, object] = Field(default_factory=dict)


class MemoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: str
    content: str
    memory_type: MemoryType
    importance: float
    metadata: dict[str, object] = Field(validation_alias="metadata_")
    created_at: datetime
    updated_at: datetime | None


class MemoryList(BaseModel):
    items: list[MemoryRead]
    total: int
