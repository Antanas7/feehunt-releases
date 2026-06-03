import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import gmail_auth


class ClearSavedAccountsTests(unittest.TestCase):
    def test_clear_all_saved_accounts_removes_active_and_archived_tokens(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            token_file = root / "token.json"
            email_file = root / "connected_email.txt"
            accounts_dir = root / "accounts"
            index_file = accounts_dir / "index.json"

            accounts_dir.mkdir()
            token_file.write_text("active", encoding="utf-8")
            email_file.write_text("first@example.com", encoding="utf-8")
            index_file.write_text('["first@example.com"]', encoding="utf-8")
            (accounts_dir / "first_example_com.json").write_text("archived", encoding="utf-8")

            with (
                patch.object(gmail_auth, "GMAIL_TOKEN_FILE", token_file),
                patch.object(gmail_auth, "GMAIL_EMAIL_FILE", email_file),
                patch.object(gmail_auth, "ACCOUNTS_DIR", accounts_dir),
                patch.object(gmail_auth, "ACCOUNTS_INDEX_FILE", index_file),
            ):
                gmail_auth.clear_all_saved_accounts()

            self.assertFalse(token_file.exists())
            self.assertFalse(email_file.exists())
            self.assertFalse(accounts_dir.exists())


if __name__ == "__main__":
    unittest.main()
