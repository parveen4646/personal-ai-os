"""HTTP entry point for the Personal AI OS Memory Service."""

from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from shared.config.settings import get_settings

from .database import Base, engine, get_session
from .models import MemoryType
from .repository import MemoryRepository
from .schemas import MemoryCreate, MemoryList, MemoryRead

settings = get_settings()
repository = MemoryRepository()
SessionDependency = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize the local schema until Alembic migrations are introduced."""

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=f"{settings.app_name} — Memory Service",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "memory-service"}


@app.post("/v1/memories", response_model=MemoryRead, status_code=status.HTTP_201_CREATED)
def create_memory(payload: MemoryCreate, session: SessionDependency) -> MemoryRead:
    return MemoryRead.model_validate(repository.create(session, payload))


@app.get("/v1/memories", response_model=MemoryList)
def list_memories(
    session: SessionDependency,
    user_id: str = Query(default="default", min_length=1),
    memory_type: MemoryType | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> MemoryList:
    items, total = repository.list(
        session, user_id=user_id, memory_type=memory_type, limit=limit, offset=offset
    )
    return MemoryList(items=[MemoryRead.model_validate(item) for item in items], total=total)


@app.get("/v1/memories/{memory_id}", response_model=MemoryRead)
def get_memory(memory_id: UUID, session: SessionDependency) -> MemoryRead:
    memory = repository.get(session, memory_id)
    if memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return MemoryRead.model_validate(memory)


@app.delete("/v1/memories/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(memory_id: UUID, session: SessionDependency) -> None:
    memory = repository.get(session, memory_id)
    if memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    repository.delete(session, memory)
