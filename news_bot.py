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


CATEGORY_KEYWORDS = {
    "🦠 Malware & Ransomware": [
        "ransomware",
        "malware",
        "infostealer",
        "information stealer",
        "trojan",
        "backdoor",
        "botnet",
        "credential stealer",
    ],
    "🕵️ Spyware & Surveillance": [
        "spyware",
        "surveillance",
        "stalkerware",
        "keylogger",
    ],
    "🔓 Data Breach": [
        "data breach",
        "data leak",
        "exposed records",
        "stolen data",
        "personal information exposed",
    ],
    "🔐 Certificate & Trust Infrastructure": [
        "certificate authority compromise",
        "certificate authority",
        "certificate authorities",
        "ca compromise",
        "ca keys",
        "ca key",
        "compromised ca",
        "compromised certificate authority",
        "certificate authority keys",
        "certificate authority key",
        "trust infrastructure",
        "code signing certificate",
        "digital certificate",
        "certificate revocation",
        "tls certificate",
        "ssl certificate",
        "root certificate",
        "root ca",
        "certificate issuer",
        "certificate issuance",
        "public key infrastructure",
        "pki",
    ],
    "🎯 Threat Intelligence": [
        "threat intelligence",
        "threat actor",
        "indicators of compromise",
        "ioc",
        "apt group",
        "cyber espionage",
    ],
    "🛡️ Cyberattacks & Intrusions": [
        "cyberattack campaign",
        "cyberattack",
        "cyber attacks",
        "cyber attack",
        "cybercriminal attack",
        "cyber crime",
        "cybercrime",
        "unauthorized access",
        "hacking",
        "hacker",
        "hackers",
        "intrusion",
        "phishing",
        "account takeover",
        "security breach",
        "network attack",
        "computer attack",
        "systems compromised",
        "system compromised",
        "compromised by hackers",
        "websites compromised",
        "compromised by attackers",
        "attacker gained access",
        "attack campaign",
        "breached network",
    ],
    "🚨 Vulnerability": [
        "critical vulnerability",
        "vulnerability",
        "zero-day",
        "zero day",
        "security flaw",
        "remote code execution",
        "rce",
        "privilege escalation",
        "exploit",
        "authentication bypass",
    ],
}


HIGH_PRIORITY_KEYWORDS = [
    "critical vulnerability",
    "critical flaw",
    "zero-day",
    "zero day",
    "actively exploited",
    "remote code execution",
    "rce",
    "ransomware",
    "data breach",
    "credential theft",
    "backdoor",
    "keys compromised",
    "key compromised",
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
    "botnet",
    "spyware",
    "certificate authority",
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
    "certificate authority",
    "unauthorized access",
    "compromised by hackers",
    "hackers",
]


def clean_text(value):
    """Decode HTML entities and remove markup from feed text."""
    if not value:
        return ""

    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(value.split())


def parse_date(value):
    """Parse a publication date and normalize it to UTC."""
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
    """Get searchable text from a story dictionary or title."""
    if isinstance(story, dict):
        title = story.get("title", "")
        description = story.get("summary", "")
        return f"{title} {description} {summary}".lower()

    return f"{story} {summary}".lower()


def categorize_story(story, summary=""):
    """Assign a cybersecurity category based on keywords."""
    text = story_text(story, summary)

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "📰 Other"


def prioritize_story(story, summary=""):
    """Return a human-readable priority label."""
    text = story_text(story, summary)

    if any(keyword in text for keyword in HIGH_PRIORITY_KEYWORDS):
        return "🔴 HIGH"

    if any(keyword in text for keyword in MEDIUM_PRIORITY_KEYWORDS):
        return "🟡 MEDIUM"

    return "🟢 LOW"


def is_soc_relevant(story, summary=""):
    """Identify stories relevant to security operations."""
    text = story_text(story, summary)
    return any(keyword in text for keyword in SOC_KEYWORDS)


def validate_https_url(url, allowed_hosts=None):
    """Reject non-HTTPS URLs and optionally restrict hostnames."""
    parsed = urlparse(url)

    if (
        parsed.scheme.lower() != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise ValueError("Only valid HTTPS URLs are allowed.")

    if allowed_hosts is not None:
        allowed = {host.lower() for host in allowed_hosts}

        if parsed.hostname.lower() not in allowed:
            raise ValueError("URL hostname is not allowed.")

    return parsed


class HTTPSOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Prevent redirects to non-HTTPS URLs."""

    def redirect_request(
        self, request, response, code, message, headers, new_url
    ):
        validate_https_url(new_url)

        return super().redirect_request(
            request, response, code, message, headers, new_url
        )


HTTPS_OPENER = urllib.request.build_opener(
    urllib.request.HTTPSHandler(),
    HTTPSOnlyRedirectHandler(),
)


def fetch_feed(source, url):
    """Fetch and safely parse a cybersecurity RSS feed."""
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
    """Build a digest with SOC-relevant stories first."""
    if not stories:
        return "No cybersecurity news stories were available today."

    priority_scores = {
        "🔴 HIGH": 3,
        "🟡 MEDIUM": 2,
        "🟢 LOW": 1,
    }

    oldest_date = datetime.min.replace(tzinfo=timezone.utc)

    ordered_stories = sorted(
        stories,
        key=lambda story: (
            is_soc_relevant(story),
            priority_scores[prioritize_story(story)],
            story.get("published", oldest_date),
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
        category = categorize_story(story)
        title = escape_slack_text(story["title"])
        source = escape_slack_text(story["source"])
        link = story["link"]

        lines.append(
            f"{index}. *<{link}|{title}>*\n"
            f"   {priority} | {category} | {source}"
        )

        summary = story.get("summary", "")

        if summary:
            summary = escape_slack_text(summary)

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
    """Fetch feeds, deduplicate stories, and post the daily digest."""
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
