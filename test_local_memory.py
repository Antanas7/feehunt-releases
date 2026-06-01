import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import local_memory


class SubscriptionStatusMemoryTests(unittest.TestCase):
    def test_status_progress_is_saved_with_email_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory_file = Path(tmp) / "memory.json"
            with patch.object(local_memory, "MEMORY_FILE", memory_file):
                saved = local_memory.set_subscription_status(
                    "small-service.example",
                    "requested",
                    "Small Service",
                    "message-1",
                    "Sat, 30 May 2026 12:00:00 +0000",
                )
                entry = local_memory.get_subscription_status("small-service.example")

        self.assertTrue(saved)
        self.assertEqual(entry["status"], "requested")
        self.assertEqual(entry["marked_message_id"], "message-1")
        self.assertEqual(entry["marked_email_date"], "Sat, 30 May 2026 12:00:00 +0000")

    def test_legacy_cancelled_status_remains_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory_file = Path(tmp) / "memory.json"
            with patch.object(local_memory, "MEMORY_FILE", memory_file):
                saved = local_memory.set_subscription_status(
                    "legacy.example",
                    "cancelled",
                    "Legacy Service",
                )
                entry = local_memory.get_subscription_status("legacy.example")

        self.assertTrue(saved)
        self.assertEqual(entry["status"], "cancelled")


if __name__ == "__main__":
    unittest.main()
