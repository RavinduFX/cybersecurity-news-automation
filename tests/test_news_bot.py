
import unittest

from news_bot import (
    categorize_story,
    is_soc_relevant,
    prioritize_story,
    needs_urgent_attention,
)


class TestNewsBot(unittest.TestCase):

    def test_certificate_authority_compromise(self):
        story = {
            "title": "Certificate authority keys compromised",
            "summary": "",
        }
        self.assertEqual(
            categorize_story(story),
            "🔐 Certificate & Trust Infrastructure",
        )

    def test_cyberattack_category(self):
        story = {
            "title": "Cyberattack targets corporate networks",
            "summary": "",
        }
        self.assertEqual(
            categorize_story(story),
            "🛡️ Cyberattacks & Intrusions",
        )

    def test_data_breach_category(self):
        story = {
            "title": "Major data breach exposes personal information",
            "summary": "",
        }
        self.assertEqual(categorize_story(story), "🔓 Data Breach")

    def test_general_technology_story_not_soc_relevant(self):
        story = {
            "title": "New smartphone receives a design update",
            "summary": "",
        }
        self.assertFalse(is_soc_relevant(story))

    def test_high_priority(self):
        story = {
            "title": "Security vulnerability CVSS score: 8.1",
            "summary": "",
        }
        self.assertEqual(prioritize_story(story), "🔴 HIGH")

    def test_low_priority(self):
        story = {
            "title": "Security vulnerability CVSS score: 3.2",
            "summary": "",
        }
        self.assertEqual(prioritize_story(story), "🟢 LOW")

    def test_medium_priority(self):
        story = {
            "title": "Security vulnerability CVSS score: 6.5",
            "summary": "",
        }
        self.assertEqual(prioritize_story(story), "🟡 MEDIUM")

    def test_ransomware_category(self):
        story = {
            "title": "Ransomware attack hits company",
            "summary": "",
        }
        self.assertEqual(
            categorize_story(story),
            "🦠 Malware & Ransomware",
        )

    def test_soc_relevant_story(self):
        story = {
            "title": "Threat intelligence identifies a new malware campaign",
            "summary": "",
        }
        self.assertTrue(is_soc_relevant(story))

    def test_spyware_category(self):
        story = {
            "title": "New spyware discovered",
            "summary": "",
        }
        self.assertEqual(
            categorize_story(story),
            "🕵️ Spyware & Surveillance",
        )

    def test_threat_intelligence_category(self):
        story = {
            "title": "Threat intelligence report reveals APT activity",
            "summary": "",
        }
        self.assertEqual(
            categorize_story(story),
            "🎯 Threat Intelligence",
        )

    def test_unknown_story_category(self):
        story = {
            "title": "A general technology announcement",
            "summary": "",
        }
        self.assertEqual(categorize_story(story), "📰 Other")

    def test_vulnerability_category(self):
        story = {
            "title": "Critical vulnerability allows remote code execution",
            "summary": "",
        }
        self.assertEqual(
            categorize_story(story),
            "🚨 Vulnerability",
        )

    def test_missing_cvss_is_unverified(self):
        story = {
            "title": "Ransomware attack reported",
            "summary": "",
        }
        self.assertEqual(
            prioritize_story(story),
            "⚪ UNVERIFIED",
        )

    def test_critical_priority(self):
        story = {
            "title": "Vulnerability CVSS score: 9.8",
            "summary": "",
        }
        self.assertEqual(
            prioritize_story(story),
            "🚨 CRITICAL",
        )

    def test_zero_cvss_score(self):
        story = {
            "title": "Vulnerability CVSS score: 0.0",
            "summary": "",
        }
        self.assertEqual(prioritize_story(story), "⚪ NONE")

    def test_urgent_attention(self):
        story = {
            "title": "Vulnerability actively exploited in the wild",
            "summary": "",
        }
        self.assertTrue(needs_urgent_attention(story))

    def test_no_urgent_attention(self):
        story = {
            "title": "Routine security update released",
            "summary": "",
        }
        self.assertFalse(needs_urgent_attention(story))


if __name__ == "__main__":
    unittest.main()
