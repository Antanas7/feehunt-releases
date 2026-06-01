import unittest

from subscription_actions import (
    direct_cancel_url_is_trusted,
    select_cancel_target,
)


class SelectCancelTargetTests(unittest.TestCase):
    def test_official_billing_hub_beats_email_link(self):
        target = select_cancel_target(
            "Apple <receipt@apple.com>",
            "https://apple.com/account/cancel",
            {"name": "App Store", "url": "https://apps.apple.com/account/subscriptions"},
        )

        self.assertEqual(target["tier"], "hub")
        self.assertEqual(target["confidence"], "official")
        self.assertEqual(target["url"], "https://apps.apple.com/account/subscriptions")

    def test_reviewed_service_page_beats_email_link(self):
        target = select_cancel_target(
            "Netflix <info@netflix.com>",
            "https://netflix.com/some-email-cancel-link",
        )

        self.assertEqual(target["tier"], "known")
        self.assertEqual(target["confidence"], "reviewed")
        self.assertEqual(target["url"], "https://www.netflix.com/CancelPlan")

    def test_unrecognized_hub_is_ignored(self):
        target = select_cancel_target(
            "Small Service <billing@small-service.example>",
            None,
            {"name": "Fake Hub", "url": "https://unknown-cancel.example.net/stop-now"},
        )

        self.assertEqual(target["tier"], "site")
        self.assertEqual(target["url"], "https://small-service.example")

    def test_same_site_email_link_is_allowed_for_small_service(self):
        target = select_cancel_target(
            "Small Service <billing@small-service.example>",
            "https://account.small-service.example/cancel-subscription",
        )

        self.assertTrue(direct_cancel_url_is_trusted(
            "Small Service <billing@small-service.example>",
            "https://account.small-service.example/cancel-subscription",
        ))
        self.assertEqual(target["tier"], "direct")
        self.assertEqual(target["confidence"], "email")
        self.assertFalse(target["email_link_skipped"])

    def test_different_domain_email_link_is_not_recommended(self):
        target = select_cancel_target(
            "Small Service <billing@small-service.example>",
            "https://unknown-cancel.example.net/stop-now",
        )

        self.assertEqual(target["tier"], "site")
        self.assertEqual(target["url"], "https://small-service.example")
        self.assertTrue(target["email_link_skipped"])

    def test_generic_mail_sender_falls_back_to_search(self):
        target = select_cancel_target(
            "Mystery Membership <mysterymembership@gmail.com>",
            "https://unknown-cancel.example.net/stop-now",
        )

        self.assertEqual(target["tier"], "search")
        self.assertEqual(target["confidence"], "search")
        self.assertTrue(target["email_link_skipped"])


if __name__ == "__main__":
    unittest.main()
