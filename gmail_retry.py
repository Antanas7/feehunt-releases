"""Resilient wrapper around Gmail API calls.

The Gmail API regularly returns transient failures during a real scan of a
large inbox over a normal home connection: rate limits (HTTP 429), backend
blips (500/502/503/504), and plain network hiccups (timeouts, dropped TLS
connections). Without retries a single blip aborts the whole scan, and the user
just sees "scan crashed" with no way forward.

This module retries those transient failures with exponential backoff (honouring
a server `Retry-After` header when present) and only gives up — raising a clear,
user-facing GmailTransientError — once retries are exhausted. Genuinely
non-recoverable errors (revoked token, permission denied, bad request) are NOT
retried; they propagate immediately so the caller can react.

Usage: wrap the request object instead of calling .execute() directly:

    response = execute_with_retry(service.users().messages().list(**request))

The request object is re-executed on each attempt, which re-issues the HTTP
request — the standard googleapiclient retry pattern.
"""

from __future__ import annotations

import socket
import ssl
import time
from typing import Any, Callable, TypeVar

from googleapiclient.errors import HttpError

T = TypeVar("T")


# HTTP statuses worth retrying: rate limiting + transient backend errors.
# Everything else (401 revoked token, 403 permission, 400 bad request, 404)
# is a real problem that more attempts won't fix.
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# Network-level exceptions that mean "the request never got a clean answer",
# which on a home connection is almost always transient.
RETRYABLE_NETWORK_ERRORS = (
    socket.timeout,
    ConnectionError,
    TimeoutError,
    ssl.SSLError,
    OSError,  # dropped connections, transient DNS failures, etc.
)

DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_BASE_DELAY = 1.0    # seconds; doubles each retry (1, 2, 4, 8, ...)
DEFAULT_MAX_DELAY = 30.0    # cap on a single backoff wait


class GmailTransientError(RuntimeError):
    """A Gmail call kept failing transiently after every retry was used up.

    Carries the last underlying error in __cause__ for logging, but its message
    is written to be shown to a non-technical user.
    """


def http_status(error: HttpError) -> int | None:
    """Best-effort extraction of the HTTP status code from an HttpError,
    across googleapiclient versions (older expose .resp.status, newer add
    .status_code)."""
    status = getattr(getattr(error, "resp", None), "status", None)
    if status is None:
        status = getattr(error, "status_code", None)
    try:
        return int(status) if status is not None else None
    except (TypeError, ValueError):
        return None


def _retry_after_seconds(error: HttpError) -> float | None:
    """Read a server-provided Retry-After hint (seconds) from a 429/503, if any.
    Only plain integer-seconds form is honoured; HTTP-date form is ignored."""
    resp = getattr(error, "resp", None)
    if resp is None:
        return None
    try:
        raw = resp.get("retry-after")  # httplib2 Response: dict-like, lowercased keys
    except Exception:
        raw = None
    if not raw:
        return None
    try:
        value = float(str(raw).strip())
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None


def _backoff_delay(attempt: int, base_delay: float, max_delay: float) -> float:
    """Exponential backoff for the given 1-based attempt number, capped."""
    return min(base_delay * (2 ** (attempt - 1)), max_delay)


def is_retryable(error: Exception) -> bool:
    """Whether an exception represents a transient failure worth retrying."""
    if isinstance(error, HttpError):
        return http_status(error) in RETRYABLE_STATUS_CODES
    return isinstance(error, RETRYABLE_NETWORK_ERRORS)


def execute_with_retry(
    request: Any,
    *,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    base_delay: float = DEFAULT_BASE_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
    sleep: Callable[[float], None] = time.sleep,
    description: str = "Gmail request",
) -> T:
    """Execute a googleapiclient request, retrying transient failures.

    Args:
        request: an object with an .execute() method (a googleapiclient
            HttpRequest), or any zero-arg callable returning the result.
        max_attempts: total attempts including the first (so N-1 retries).
        base_delay / max_delay: exponential backoff bounds, in seconds.
        sleep: injected for testability (defaults to time.sleep).
        description: short label used in the user-facing error message.

    Returns:
        Whatever request.execute() returns.

    Raises:
        GmailTransientError: after exhausting retries on a transient failure.
        HttpError / other: immediately, for non-retryable failures.
    """
    run = request if callable(request) else request.execute
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return run()
        except HttpError as error:
            last_error = error
            if http_status(error) not in RETRYABLE_STATUS_CODES or attempt >= max_attempts:
                raise
            wait = _retry_after_seconds(error) or _backoff_delay(attempt, base_delay, max_delay)
            sleep(min(wait, max_delay))
        except RETRYABLE_NETWORK_ERRORS as error:
            last_error = error
            if attempt >= max_attempts:
                raise GmailTransientError(
                    f"{description} failed after {max_attempts} attempts because the "
                    "connection to Google kept dropping. Check your internet connection "
                    "and try again."
                ) from error
            sleep(_backoff_delay(attempt, base_delay, max_delay))

    # Loop only exits via return/raise; this guards against an unexpected
    # max_attempts <= 0 being passed in.
    raise GmailTransientError(
        f"{description} did not run (no attempts were made)."
    ) from last_error
