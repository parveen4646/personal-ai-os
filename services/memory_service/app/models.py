"""Persistence models for durable assistant memories."""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, Enum as SqlEnum, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class MemoryType(str, Enum):
    """The role a memory plays in future assistant reasoning."""

    semantic = "semantic"
    episodic = "episodic"
    procedural = "procedural"
    preference = "preference"


class Memory(Base):
    """A durable, user-scoped unit of long-term memory.

    `embedding` is intentionally absent from the first migration. A pgvector
    column will be added alongside the retrieval pipeline once embeddings are
    generated consistently by the future Model Service.
    """

    __tablename__ = "memories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[str] = mapped_column(String(255), index=True, default="default")
    content: Mapped[str] = mapped_column(Text)
    memory_type: Mapped[MemoryType] = mapped_column(SqlEnum(MemoryType), index=True)
    importance: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_: Mapped[dict[str, object]] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
