"""
Typed domain exceptions for the AI Intelligence Hub.
Each exception maps to a specific error category and gRPC status code as defined in the design's Error handling section.
"""

class DomainError(Exception):
    """Base class for all domain-level errors.
    
    Maps tp gRPC INVALID_ARGUMENT when the query is off-domain.
    Not retryable - the caller should modify the request.
    """

    def __init__(self, message: str = "Request is outside the supported domain") -> None:
        self.message = message
        super().__init__(self.message)

class AuthorizationError(DomainError):
    """
        Raised when the authorized_account_set is null, empty, or invalid.
        Maps to gRPC PERMISSION_DENIED. Not retryable.
    """

    def __init__(self, message:str = "Invalid or missing authorized account set") -> None:
        super().__init__(message)

class InputValidationError(DomainError):
    """
        Raised when input fails validation (too long, injection detected, etc..)
        Maps to gRPC INVALID_ARGUMENT. Not retryable - the caller must fix the input.
    """

    def __init__(self, message: str="Input validation failed") -> None:
        super().__init__(message)

class RateLimitExceeded(DomainError):
    """ Raised when a user exceeds the per-user request rate limit.
        Maps to gRPC RESEOURCE_EXHAUSTED. Retryable after the window resets.
    """

    def __init__(self, message = "Rate limit exceeded", retry_after_seconds:int = 0) -> None:
        self.retry_after_seconds - retry_after_seconds
        super().__init__(message)

class LLMUnavailableError(DomainError):
    """ Raised when the LLM Gateway cannot reach bedrock after retries.
        Maps to gRPC UNAVAILABLE. Retryable.
    """

    def __init__(self, message:str="LLM Service is temporable unavailable") ->None:
        super().__init__(message)


class CostBudgetExhaustedError(DomainError):
    """
    Raised when daily token spend exceeds the configured threshold.

    Maps to gRPC UNAVAILABLE with degraded mode indication. Retryable next day.
    """

    def __init__(self,message:str = "Service is operating in degraded mode due to budget limits")-> None:
        super().__init__(message)

class GroundingFailureError(DomainError):
    """
    Raised when an LLM summary references events not in the provided input set.

    Maps to gRPC INTERNAL (details not exposed to caller). Retryable.
    """

    def __init__(self, message = "Grouding validation failed") -> None:
        super().__init__(message)

class FeatureDisabledError(DomainError):
    """
    Raised when a capability's feature flag is disabled.

    Maps to gRPC UNAVAILABLE with capability-specific message. Retryable when re-enabled.
    """

    def __init__(self, capability:str = "unknown")-> None:
        self.capability = capability
        super().__init__(f"Capability '{capability}' is temporary unavailable")