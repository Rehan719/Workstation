import unittest
import os
from products.OctoVeritasEngine.constitution.compliance_checker import ComplianceChecker, ConstitutionalViolation

class TestVeritasV4Sovereign(unittest.TestCase):
    def test_compliance_checker_p0_article_42(self):
        checker = ComplianceChecker({"42": {"title": "Data Sovereignty", "text": "..."}})

        # Compliant
        self.assertTrue(checker.check_compliance("42", {"jurisdiction": "Sovereign"}))

        # Violation
        with self.assertRaises(ConstitutionalViolation) as cm:
            checker.check_compliance("42", {"jurisdiction": "OUTSIDE"})
        self.assertEqual(cm.exception.article_id, "42")

    def test_compliance_checker_p0_article_78(self):
        checker = ComplianceChecker({"78": {"title": "Accessibility", "text": "..."}})

        # Compliant
        self.assertTrue(checker.check_compliance("78", {"accessibility": {"alt_text": "Image desc"}}))

        # Violation
        with self.assertRaises(ConstitutionalViolation):
            checker.check_compliance("78", {"accessibility": {}})

if __name__ == "__main__":
    unittest.main()
