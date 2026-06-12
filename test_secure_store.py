"""Tests for secure_store (DPAPI token-at-rest encryption).

Roundtrip + legacy plain-text passthrough are checked everywhere. The
"actually encrypts" assertions only run where DPAPI is available (Windows).
"""

import json
import unittest

import secure_store


class SecureStoreTest(unittest.TestCase):
    def test_seal_unseal_roundtrip(self):
        original = json.dumps({"token": "abc", "refresh_token": "xyz", "scopes": ["a"]})
        sealed = secure_store.seal(original)
        self.assertIsInstance(sealed, bytes)
        self.assertEqual(secure_store.unseal(sealed), original)

    def test_unseal_passes_through_legacy_plaintext(self):
        # A token file written by an older build has no magic header.
        legacy = json.dumps({"token": "old"}).encode("utf-8")
        self.assertEqual(secure_store.unseal(legacy), '{"token": "old"}')

    def test_roundtrip_unicode(self):
        original = "wörld — ąčę 🌍"
        self.assertEqual(secure_store.unseal(secure_store.seal(original)), original)

    @unittest.skipUnless(secure_store.is_available(), "DPAPI only available on Windows")
    def test_sealed_is_encrypted_on_windows(self):
        original = "super-secret-refresh-token"
        sealed = secure_store.seal(original)
        # Marked as DPAPI and the plaintext is not present in the ciphertext.
        self.assertTrue(sealed.startswith(b"FHDPAPI1\n"))
        self.assertNotIn(original.encode("utf-8"), sealed)


if __name__ == "__main__":
    unittest.main()
