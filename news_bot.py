
import os
import re
import html
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from defusedxml import ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


TIMEOUT_SECONDS = 20
MAX_STORIES = 10

FEEDS = [
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
]

HIGH_PRIORITY_KEYWORDS = [
    "critical vulnerability",
    "zero-day",
    "zero day",
    "actively exploited",
    "remote code execution",
    "rce",
    "ransomware",
    "data breach",
    "credential theft",
    "privilege escalation",
]

MEDIUM_PRIORITY_KEYWORDS = [
    "vulnerability",
    "exploit",
    "malware",
    "phishing",
    "cyberattack",
    "cyber attack",
    "security flaw",
    "patch",
    "backdoor",
    "botnet",
]

SOC_KEYWORDS = [
    "threat intelligence",
    "incident response",
    "security operations",
    "soc",
    "siem",
    "detection",
    "indicators of compromise",
    "ioc",
    "intrusion",
    "malware",
    "ransomware",
    "phishing",
    "exploit",
    "vulnerability",
    "data breach",
    "cyberattack",
    "cyber attack",
    "zero-day",
    "zero day",
]


def clean_text(value):
    """Decode HTML entities and remove markup from feed text."""
    if not value:
        return ""

    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(value.split())


def parse_date(value):
    """Parse a published date and return a UTC datetime."""
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)

    try:
        parsed = parsedate_to_datetime(value)

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    except (TypeError, ValueError, OverflowError):
        return datetime.min.replace(tzinfo=timezone.utc)


def prioritize_story(story):
    """Assign a priority score based on security keywords."""
    text = f"{story['title']} {story['summary']}".lower()

    if any(keyword in text for keyword in HIGH_PRIORITY_KEYWORDS):
        return 3

    if any(keyword in text for keyword in MEDIUM_PRIORITY_KEYWORDS):
        return 2

    return 1


def is_soc_relevant(story):
    """Return True when a story is relevant to SOC work."""
    text = f"{story['title']} {story['summary']}".lower()
    return any(keyword in text for keyword in SOC_KEYWORDS)


def fetch_feed(source, url):
    """Fetch and parse an RSS feed from a validated HTTPS URL."""
    try:
        parsed_url = urlparse(url)

        if (
            parsed_url.scheme != "https"
            or not parsed_url.hostname
            or parsed_url.username
            or parsed_url.password
        ):
            raise ValueError("Only valid HTTPS feed URLs are allowed.")

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "CybersecurityNewsBot/1.0"},
        )

        with urllib.request.urlopen(
            request, timeout=TIMEOUT_SECONDS
        ) as response:
            content = response.read()

        root = ET.fromstring(content)
        stories = []

        for item in root.findall(".//item"):
            title = clean_text(item.findtext("title", ""))
            link = item.findtext("link", "").strip()
            summary = clean_text(
                item.findtext("description", "")
            )
            published = item.findtext("pubDate", "")

            if not title or not link:
                continue

            link_url = urlparse(link)

            if (
                link_url.scheme != "https"
                or not link_url.hostname
                or link_url.username
                or link_url.password
            ):
                continue

            stories.append(
                {
                    "source": source,
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": parse_date(published),
                }
            )

        print(f"Fetched {len(stories)} stories from {source}")
        return stories

    except Exception as error:
        print(f"Warning: could not fetch {source}: {error}")
        return []


def escape_slack_text(value):
    """Escape Slack's special characters in plain text."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_digest(stories):
    """Build a Slack digest with SOC-relevant stories first."""
    if not stories:
        return "No cybersecurity news stories were available today."

    ordered_stories = sorted(
        stories,
        key=lambda story: (
            is_soc_relevant(story),
            prioritize_story(story),
            story["published"],
        ),
        reverse=True,
    )

    selected_stories = ordered_stories[:MAX_STORIES]

    lines = [
        "*Daily Cybersecurity News Digest*",
        f"_{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
    ]

    for index, story in enumerate(selected_stories, start=1):
        priority = prioritize_story(story)

        if priority == 3:
            category = "🚨 High Priority"
        elif priority == 2:
            category = "⚠️ Medium Priority"
        else:
            category = "📰 General"

        title = escape_slack_text(story["title"])
        source = escape_slack_text(story["source"])
        link = story["link"]

        lines.append(
            f"{index}. *<{link}|{title}>*\n"
            f"   {category} | {source}"
        )

        if story["summary"]:
            summary = escape_slack_text(story["summary"])
            if len(summary) > 250:
                summary = summary[:247] + "..."

            lines.append(f"   _{summary}_")

        lines.append("")

    return "\n".join(lines)


def post_to_slack(message):
    """Post the digest to Slack using credentials from environment secrets."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL_ID")

    if not token or not channel:
        raise RuntimeError(
            "Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID environment variable."
        )

    slack_url = "https://slack.com/api/chat.postMessage"
    parsed_url = urlparse(slack_url)

    if (
        parsed_url.scheme != "https"
        or parsed_url.hostname != "slack.com"
    ):
        raise RuntimeError("Invalid Slack API URL.")

    payload = json.dumps(
        {
            "channel": channel,
            "text": message,
            "mrkdwn": True,
            "unfurl_links": False,
            "unfurl_media": False,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        slack_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request, timeout=TIMEOUT_SECONDS
        ) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        raise RuntimeError(
            f"Slack API returned HTTP {error.code}."
        ) from error

    if not result.get("ok"):
        raise RuntimeError(
            f"Slack API error: {result.get('error', 'unknown_error')}"
        )

    print("Cybersecurity news digest posted to Slack successfully.")


def main():
    """Fetch feeds, deduplicate stories, and post the daily digest."""
    all_stories = []
    seen_links = set()

    for source, url in FEEDS:
        stories = fetch_feed(source, url)

        for story in stories:
            if story["link"] not in seen_links:
                seen_links.add(story["link"])
                all_stories.append(story)

    all_stories.sort(
        key=lambda story: story["published"],
        reverse=True,
    )

    digest = build_digest(all_stories)
    post_to_slack(digest)


if __name__ == "__main__":
    main()
