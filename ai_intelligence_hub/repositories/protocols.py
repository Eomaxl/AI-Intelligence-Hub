""" Repository protocol interfaces for data access abstractions. """

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from ai_intelligence_hub.domain.entities import (
    AccountEvent,
    DocumentEmbedding,
    SearchResult,
    TicketClassification,
)


class VectorRepository(Protocol):
    """Protocol for vector store operations with access-scoped retrieval. """

    async def similarity_search(
        self, 
        embedding: list[float], 
        authorized_account_ids: list[int], 
        *, 
        doc_type: str | None = None, 
        limit: int = 20, 
        min_similarity:float = 0.0,
    ) -> list[SearchResult]: ...

    async def upsert_document(self, doc: DocumentEmbedding) -> None: ...


class ClassificationRepository(Protocol):
    """ Protocol for ticket classification persistence."""

    async def get_classification(self, ticket_ref: str) -> TicketClassification | None : ...

    async def upsert_classification(self, classification: TicketClassification) -> None: ...


class EventRepository(Protocol):
    """Protocol for account event retrieval."""
    async def since(
            self, account_id: int ,since_ts: datetime, limit: int = 200
    ) -> list[AccountEvent]: ...