import unittest

from phishing_detector import analyze_phishing


class PhishingRiskLevelTests(unittest.TestCase):
    def test_cross_service_link_is_caution_not_danger(self):
        result = analyze_phishing(
            "Render <no-reply@render.com>",
            "deploy failed for besafe",
            "",
            '<a href="https://github.com/Antanas7/besafe/commit/abc">render.com</a>',
        )

        self.assertTrue(result["is_phishing_risk"])
        self.assertEqual(result["risk_level"], "caution")
        self.assertEqual(result["reasons"][0]["code"], "hidden_link")

    def test_hidden_link_with_pressure_is_danger(self):
        result = analyze_phishing(
            "Render <no-reply@render.com>",
            "action required",
            "Verify your account immediately.",
            '<a href="https://evil.example/login">render.com</a>',
        )

        self.assertTrue(result["is_phishing_risk"])
        self.assertEqual(result["risk_level"], "danger")
        self.assertEqual(
            {reason["code"] for reason in result["reasons"]},
            {"hidden_link", "urgency_credentials"},
        )

    def test_known_brand_sender_mismatch_remains_danger(self):
        result = analyze_phishing(
            "PayPal <billing@gmail.com>",
            "Your receipt",
            "",
            "",
        )

        self.assertTrue(result["is_phishing_risk"])
        self.assertEqual(result["risk_level"], "danger")
        self.assertEqual(result["reasons"][0]["code"], "name_domain_mismatch")


if __name__ == "__main__":
    unittest.main()
