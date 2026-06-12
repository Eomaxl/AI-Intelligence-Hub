""" Domain layer - entities , value objects, and domain errors. """

from ai_intelligence_hub.domain.entities import (
    AccountEvent,
    AccountSummaryResult,
    Chunk,
    DocType,
    DocumentEmbedding,
    RagAnswerResult,
    RankedEvent,
    SearchResult,
    Source,
    TicketClassification,
    TicketStatus,
    TicketSuggestionResult,
)

from ai_intelligence_hub.domain.errors import (
    AuthorizationError,
    CostBudgetExhaustedError,
    DomainError,
    FeatureDisabledError,
    GroundingFailureError,
    InputValidationError,
    LLMUnavailableError,
    RateLimitExceeded,
)

__all__ = [
    # Enums
    "Source",
    "DocType",
    "TicketStatus",
    # Entities
    "AccountEvent",
    "RankedEvent",
    "DocumentEmbedding",
    "Chunk",
    "SearchResult",
    "TicketClassification",
    "AccountSummaryResult",
    "RagAnswerResult",
    "TicketSuggestionResult",
    # Errors
    "AuthorizationError",
    "InputValidationError",
    "DomainError",
    "RateLimitExceeded",
    "LLMUnavailableError",
    "CostBudgetExhaustedError",
    "GroundingFailureError",
    "FeatureDisabledError",
]