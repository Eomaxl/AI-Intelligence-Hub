"""Domain entities - frozen dataclasses and enums for the AI Intelligence Hub. """

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Source(str, Enum):
    """Data source systems integrated with the Intelligence Hub. """
    
    SALESFORCE = "salesforce"
    GAINSIGHT = "gainsight"
    ZENDESK = "zendesk"
    SIXSENSE = "6sense"
    TABLEAU = "tableau"

class DocType(str, Enum):
    """Document type stored in the vector store."""

    NOTE="note"
    TICKET = "ticket"
    HEALTH_SUMMARY= "health_summary"
    INTENT = "intent"
    METRIC_ANNOTATION = "metric_annotation"

class TicketStatus (str, Enum):
    """Classification status for triaged tickets."""

    OPEN = "open"
    RESOLVED = "resolved"
    LOW_CONFIDENCE = "low_confidence"


@dataclass(frozen=True)    
class AccountEvent:
    """An enriched event for a customer account from any integrated source."""

    event_id: str
    account_id: int
    event_type: str
    source: Source
    content: str
    event_ts: datetime
    metadata: dict[str, str]

    def as_struct(self) -> dict:
        """Structured representation for LLM prompt context."""
        return {
            "event_id":self.event_id,
            "account_id":self.account_id,
            "event_type":   self.event_type,
            "source": self.source,
            "content": self.content,
            "event_ts": self.event_ts.isoformat(),
            "metadata": self.metadata,
        }
    
@dataclass(frozen=True)
class RankedEvent:
    """An account event with a deterministic priority score assigned by the Event Ranker."""

    event: AccountEvent
    priority_score: int     # 0 - 100 inclusive

    @property
    def is_high_priority(self)-> bool:
        """ An event is high priority when its score is 80 or above."""
        return self.priority_score >= 80
    

@dataclass(frozen=True)
class DocumentEmbedding:
    """A document chunk with its computed embedding, ready for vector store upsert."""

    account_id: int
    source: Source
    doc_type: DocType
    source_ref: str
    content: str
    embedding: list[float]      # 1024-dim
    event_ts: datetime


@dataclass(frozen=True)
class Chunk:
    """ A document chunk produced by source-aware chunking strategies."""

    content: str
    source_ref: str
    doc_type: DocType
    account_id: int
    sequence_position: int | None = None
    parent_chunk_id: str | None = None


@dataclass(frozen=True)
class SearchResult:
    """ A vector similarity search result with metadata for citation."""

    source_ref: str
    source: Source
    doc_type: DocType
    content: str
    similarity_score: float


@dataclass(frozen=True)
class TicketClassification:
    """A ticket classification produced by the DistilBERT classifier."""

    ticket_ref: str
    account_id: int
    category: str
    priority: str
    confidence: float # 0.0-1.0
    status: TicketStatus
    classified_at: datetime


@dataclass(frozen=True)
class AccountSummaryResult:
    """The result of an account summarization request."""

    account_id: int
    narrative: str
    high_priority_events: list[RankedEvent]
    from_cache: bool


@dataclass(frozen=True)
class RagAnswerResult:
    """The result of a RAG chatbot query with citations."""
    text: str
    citations: list[SearchResult]


@dataclass(frozen=True)
class TicketSuggestionResult:
    """The result of a ticket triage suggestion request."""

    ticket_id: str
    classification: TicketClassification
    similar_tickets: list[SearchResult]
    suggested_action: str | None
    action_generated: bool