""" Gateway protocol interfaces for LLM, embedding, and classifier abstractions. """

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ai_intelligence_hub.domain.entities import TicketClassification

@dataclass(frozen=True)
class LLMResult:
    """Immutable result from an LLM completion call."""

    test: str
    input_tokens: int
    output_tokens: int
    from_cache: bool

class LLMGateway(Protocol):
    """Protocol for the centralized LLM traffic controller with caching and resilience."""

    async def complete(
        self,
        *,
        template: str,
        inputs: dict[str, Any],
        max_tokens: int
    )-> LLMResult: ...

class LLMProvider(Protocol):
    """Protocol for a raw LLM provider (e.g. , Bedrock Claude Haiku )"""

    async def invoke(self, prompt: str, max_tokens: int) -> LLMResult: ...

class EmbeddingProvider(Protocol):
    """Protocol for computing text embeddings. """

    async def embed(self, test: str) -> list[float]:...

class ClassifierClient(Protocol):
    """Protocol for ticket classification via external model (e.g., TorchServe DistilBERT)."""
    
    async def classify(self, text:str) -> TicketClassification | None: ...
