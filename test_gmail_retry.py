"""Tests for gmail_retry.execute_with_retry.

Covers the transient-failure paths that previously had no coverage: rate limits
(429), backend errors (5xx), network blips, give-up-after-retries, immediate
propagation of non-retryable errors, and Retry-After handling. A fake sleep is
injected so the tests never actually wait.
"""

import socket
import unittest

from googleapiclient.errors import HttpError

from gmail_retry import GmailTransientError, execute_with_retry, http_status, is_retryable


class FakeResp(dict):
    """Minimal stand-in for an httplib2 Response: a dict (for header lookups
    like retry-after) that also carries a .status attribute."""

    def __init__(self, status, headers=None):
        super().__init__(headers or {})
        self.status = status
        self.reason = "Test error"


def make_http_error(status, headers=None):
    return HttpError(FakeResp(status, headers), b"{}", uri="https://gmail.example/test")


class FlakyRequest:
    """A request whose .execute() raises the given errors in order, then
    returns `result`. Records how many times it was called."""

    def __init__(self, errors, result="ok"):
        self._errors = list(errors)
        self._result = result
        self.calls = 0

    def execute(self):
        self.calls += 1
        if self._errors:
            raise self._errors.pop(0)
        return self._result


class ExecuteWithRetryTest(unittest.TestCase):
    def setUp(self):
        self.slept = []

    def _sleep(self, seconds):
        self.slept.append(seconds)

    def test_returns_immediately_on_success(self):
        req = FlakyRequest([])
        result = execute_with_retry(req, sleep=self._sleep)
        self.assertEqual(result, "ok")
        self.assertEqual(req.calls, 1)
        self.assertEqual(self.slept, [])

    def test_retries_on_429_then_succeeds(self):
        req = FlakyRequest([make_http_error(429), make_http_error(429)])
        result = execute_with_retry(req, sleep=self._sleep, base_delay=1, max_delay=30)
        self.assertEqual(result, "ok")
        self.assertEqual(req.calls, 3)
        # Two backoff waits: 1s then 2s (exponential).
        self.assertEqual(self.slept, [1, 2])

    def test_retries_on_5xx(self):
        for status in (500, 502, 503, 504):
            with self.subTest(status=status):
                req = FlakyRequest([make_http_error(status)])
                result = execute_with_retry(req, sleep=self._sleep)
                self.assertEqual(result, "ok")
                self.assertEqual(req.calls, 2)

    def test_retries_on_network_error_then_succeeds(self):
        req = FlakyRequest([socket.timeout(), ConnectionError()])
        result = execute_with_retry(req, sleep=self._sleep)
        self.assertEqual(result, "ok")
        self.assertEqual(req.calls, 3)

    def test_does_not_retry_non_retryable_status(self):
        # 403 (permission) / 401 (revoked token) / 400 (bad request) must not retry.
        for status in (400, 401, 403, 404):
            with self.subTest(status=status):
                req = FlakyRequest([make_http_error(status)])
                with self.assertRaises(HttpError):
                    execute_with_retry(req, sleep=self._sleep)
                self.assertEqual(req.calls, 1)
                self.assertEqual(self.slept, [])

    def test_gives_up_after_max_attempts_on_http(self):
        req = FlakyRequest([make_http_error(503)] * 10)
        with self.assertRaises(HttpError):
            execute_with_retry(req, max_attempts=3, sleep=self._sleep)
        self.assertEqual(req.calls, 3)
        # Slept between the 3 attempts -> 2 waits.
        self.assertEqual(len(self.slept), 2)

    def test_gives_up_after_max_attempts_on_network(self):
        req = FlakyRequest([socket.timeout()] * 10)
        with self.assertRaises(GmailTransientError):
            execute_with_retry(req, max_attempts=3, sleep=self._sleep)
        self.assertEqual(req.calls, 3)

    def test_honours_retry_after_header(self):
        req = FlakyRequest([make_http_error(429, {"retry-after": "7"})])
        execute_with_retry(req, sleep=self._sleep, base_delay=1)
        # First wait should follow the server hint (7s), not the 1s backoff.
        self.assertEqual(self.slept[0], 7)

    def test_caps_backoff_at_max_delay(self):
        req = FlakyRequest([make_http_error(503)] * 4)
        execute_with_retry(req, sleep=self._sleep, base_delay=10, max_delay=15)
        # Backoff would be 10, 20, 40, ... but capped at 15.
        self.assertTrue(all(w <= 15 for w in self.slept))

    def test_accepts_plain_callable(self):
        calls = {"n": 0}

        def call():
            calls["n"] += 1
            if calls["n"] < 2:
                raise make_http_error(503)
            return "done"

        result = execute_with_retry(call, sleep=self._sleep)
        self.assertEqual(result, "done")
        self.assertEqual(calls["n"], 2)


class HelpersTest(unittest.TestCase):
    def test_http_status_extraction(self):
        self.assertEqual(http_status(make_http_error(429)), 429)

    def test_is_retryable(self):
        self.assertTrue(is_retryable(make_http_error(503)))
        self.assertTrue(is_retryable(socket.timeout()))
        self.assertFalse(is_retryable(make_http_error(403)))
        self.assertFalse(is_retryable(ValueError("nope")))


if __name__ == "__main__":
    unittest.main()
