
import unittest

from news_bot import categorize_story, prioritize_story


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
        story = {"title": "Critical vulnerability actively exploited in attacks"}
        self.assertEqual(prioritize_story(story), "🔴 HIGH")

    def test_low_priority(self):
        story = {"title": "New technology trends announced"}
        self.assertEqual(prioritize_story(story), "🟢 LOW")


if __name__ == "__main__":
    unittest.main()
