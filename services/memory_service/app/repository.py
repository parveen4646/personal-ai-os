"""Database operations kept separate from HTTP concerns."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Memory, MemoryType
from .schemas import MemoryCreate


class MemoryRepository:
    """CRUD access for `Memory` records.

    Retrieval by semantic similarity belongs in a later repository method once
    pgvector embeddings are produced by the model integration.
    """

    def create(self, session: Session, payload: MemoryCreate) -> Memory:
        memory = Memory(
            user_id=payload.user_id,
            content=payload.content,
            memory_type=payload.memory_type,
            importance=payload.importance,
            metadata_=payload.metadata,
        )
        session.add(memory)
        session.commit()
        session.refresh(memory)
        return memory

    def get(self, session: Session, memory_id: UUID) -> Memory | None:
        return session.get(Memory, memory_id)

    def list(
        self,
        session: Session,
        *,
        user_id: str = "default",
        memory_type: MemoryType | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Memory], int]:
        filters = [Memory.user_id == user_id]
        if memory_type is not None:
            filters.append(Memory.memory_type == memory_type)

        statement = (
            select(Memory)
            .where(*filters)
            .order_by(Memory.importance.desc(), Memory.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        items = list(session.scalars(statement))
        total = session.scalar(select(func.count()).select_from(Memory).where(*filters)) or 0
        return items, total

    def delete(self, session: Session, memory: Memory) -> None:
        session.delete(memory)
        session.commit()
