class AggregatorError(Exception):
    """Base class for errors raised by this project."""

    pass


class TransientProviderError(AggregatorError):
    """Base class for temporary provider errors that may succeed on retry."""

    pass


class ClientTimeoutError(TransientProviderError):
    """Raised when one provider request times out."""

    pass


class ProviderConnectionError(TransientProviderError):
    """Raised when a provider cannot temporarily be reached."""

    pass


class RateLimitExceededError(TransientProviderError):
    """Raised when a provider rate limit is reached."""

    pass


class ProviderServerError(TransientProviderError):
    """Raised when a provider has a temporary server-side failure."""

    pass


class ModelNotFoundError(AggregatorError):
    """Raised when the requested model cannot be found."""

    pass
