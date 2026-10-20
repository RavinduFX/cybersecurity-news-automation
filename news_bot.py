
import unittest


class TestNewsBot(unittest.TestCase):

    def test_vulnerability_category(self):
        story = {"title": "Critical vulnerability discovered"}
        self.assertEqual(categorize_story(story), "🚨 Vulnerability")

    def test_ransomware_category(self):
        story = {"title": "New ransomware campaign targets businesses"}
        self.assertEqual(
            categorize_story(story),
            "🦠 Malware & Ransomware"
        )

    def test_high_priority(self):
        story = {
            "title": "Critical vulnerability actively exploited in attacks"
        }
        self.assertEqual(prioritize_story(story), "🔴 HIGH")

    def test_low_priority(self):
        story = {"title": "New technology trends announced"}
        self.assertEqual(prioritize_story(story), "🟢 LOW")

    def test_data_breach_category(self):
        story = {"title": "Company reports major data breach"}
        self.assertEqual(categorize_story(story), "🔓 Data Breach")

    def test_spyware_category(self):
        story = {"title": "Pegasus spyware infection discovered"}
        self.assertEqual(
            categorize_story(story),
            "🕵️ Spyware & Surveillance"
        )

    def test_threat_intelligence_category(self):
        story = {"title": "APT group launches cyber espionage campaign"}
        self.assertEqual(
            categorize_story(story),
            "🎯 Threat Intelligence"
        )

    def test_cyberattack_category(self):
        story = {"title": "Company websites compromised by hackers"}
        self.assertEqual(
            categorize_story(story),
            "🛡️ Cyberattacks & Intrusions"
        )

    def test_medium_priority(self):
        story = {"title": "New phishing campaign targets employees"}
        self.assertEqual(prioritize_story(story), "🟡 MEDIUM")

    def test_unknown_story_category(self):
        story = {"title": "New technology trends announced"}
        self.assertEqual(categorize_story(story), "📰 Other")


if __name__ == "__main__":
    unittest.main()
