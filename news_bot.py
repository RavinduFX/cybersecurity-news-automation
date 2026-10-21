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

# Use one opener for HTTPS requests instead of urllib.request.urlopen.
HTTPS_OPENER = urllib.request.build_opener(
    urllib.request.HTTPSHandler()
)

CATEGORY_KEYWORDS = {
    "🚨 Vulnerability": [
        "vulnerability", "cve-", "zero-day", "zero day",
        "security flaw", "remote code execution", "rce",
        "privilege escalation",
    ],
    "🦠 Malware & Ransomware": [
        "malware", "ransomware", "trojan", "infostealer",
        "backdoor", "botnet",
    ],
    "🕵️ Spyware & Surveillance": [
        "spyware", "surveillance", "stalkerware", "keylogger",
    ],
    "🔓 Data Breach": [
        "data breach", "data leak", "exposed records",
        "stolen data", "credential theft",
    ],
    "🔐 Certificate & Trust Infrastructure": [
        "certificate", "certification authority", "tls",
        "ssl", "code signing",
    ],
    "🎯 Threat Intelligence": [
        "threat intelligence", "apt", "threat actor",
        "indicators of compromise", "ioc",
    ],
    "🛡️ Cyberattacks & Intrusions": [
        "cyberattack", "cyber attack", "hacking",
        "intrusion", "phishing", "exploit",
    ],
}

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
    """Parse a published date and normalize it to UTC."""
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)

    try:
        parsed = parsedate_to_datetime(value)

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    except (TypeError, ValueError, OverflowError):
        return datetime.min.replace(tzinfo=timezone.utc)


def story_text(story, summary=""):
    """Support either a story dictionary or title plus summary."""
    if isinstance(story, dict):
        return (
            f"{story.get('title', '')} "
            f"{story.get('summary', '')}"
        ).lower()

    return f"{story} {summary}".lower()


def categorize_story(story, summary=""):
    """Assign a security category using story keywords."""
    text = story_text(story, summary)

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "📰 Other"


def prioritize_story(story, summary=""):
    """Return a numeric priority score: high 3, medium 2, low 1."""
    text = story_text(story, summary)

    if any(keyword in text for keyword in HIGH_PRIORITY_KEYWORDS):
        return 3

    if any(keyword in text for keyword in MEDIUM_PRIORITY_KEYWORDS):
        return 2

    return 1


def is_soc_relevant(story, summary=""):
    """Identify stories relevant to security operations."""
    text = story_text(story, summary)
    return any(keyword in text for keyword in SOC_KEYWORDS)


def validate_https_url(url, allowed_hosts=None):
    """Reject non-HTTPS URLs and optionally restrict hostnames."""
    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise ValueError("Only valid HTTPS URLs are allowed.")

    if allowed_hosts is not None:
        if parsed.hostname.lower() not in allowed_hosts:
            raise ValueError("URL hostname is not allowed.")

    return parsed


def fetch_feed(source, url):
    """Fetch and parse a trusted RSS feed."""
    try:
        validate_https_url(url)

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "CybersecurityNewsBot/1.0"},
        )

        with HTTPS_OPENER.open(
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

            try:
                validate_https_url(link)
            except ValueError:
                continue

            stories.append({
                "source": source,
                "title": title,
                "link": link,
                "summary": summary,
                "published": parse_date(published),
            })

        print(f"Fetched {len(stories)} stories from {source}")
        return stories

    except Exception as error:
        print(f"Warning: could not fetch {source}: {error}")
        return []


def escape_slack_text(value):
    """Escape special characters in Slack text."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_digest(stories):
    """Build a digest with SOC-relevant and high-priority stories first."""
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
            priority_label = "🚨 High Priority"
        elif priority == 2:
            priority_label = "⚠️ Medium Priority"
        else:
            priority_label = "📰 General"

        category = categorize_story(story)
        title = escape_slack_text(story["title"])
        source = escape_slack_text(story["source"])
        link = story["link"]

        lines.append(
            f"{index}. *<{link}|{title}>*\n"
            f"   {priority_label} | {category} | {source}"
        )

        if story["summary"]:
            summary = escape_slack_text(story["summary"])

            if len(summary) > 250:
                summary = summary[:247] + "..."

            lines.append(f"   _{summary}_")

        lines.append("")

    return "\n".join(lines)


def post_to_slack(message):
    """Post the digest using credentials stored in GitHub Secrets."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL_ID")

    if not token or not channel:
        raise RuntimeError(
            "Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID environment variable."
        )

    slack_url = "https://slack.com/api/chat.postMessage"
    validate_https_url(slack_url, allowed_hosts={"slack.com"})

    payload = json.dumps({
        "channel": channel,
        "text": message,
        "mrkdwn": True,
        "unfurl_links": False,
        "unfurl_media": False,
    }).encode("utf-8")

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
        with HTTPS_OPENER.open(
            request, timeout=TIMEOUT_SECONDS
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

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
    """Fetch feeds, deduplicate stories, and post the digest."""
    all_stories = []
    seen_links = set()

    for source, url in FEEDS:
        for story in fetch_feed(source, url):
            if story["link"] not in seen_links:
                seen_links.add(story["link"])
                all_stories.append(story)

    all_stories.sort(
        key=lambda story: story["published"],
        reverse=True,
    )

    post_to_slack(build_digest(all_stories))


if __name__ == "__main__":
    main()
