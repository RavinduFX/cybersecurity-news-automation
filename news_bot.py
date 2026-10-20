import os
import re
import html
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
]

MAX_STORIES = 10
TIMEOUT_SECONDS = 20


def fetch_feed(source, url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CybersecurityNewsBot/1.0"},
    )

    try:
        with urllib.request.urlopen(
            request, timeout=TIMEOUT_SECONDS
        ) as response:
            content = response.read()

        root = ET.fromstring(content)
        stories = []

        for item in root.findall(".//item"):
            title = item.findtext("title", default="").strip()
            link = item.findtext("link", default="").strip()
            pub_date = item.findtext("pubDate", default="").strip()

            if not title or not link:
                continue

            published = None
            if pub_date:
                try:
                    published = parsedate_to_datetime(pub_date)
                    if published.tzinfo is None:
                        published = published.replace(tzinfo=timezone.utc)
                except (TypeError, ValueError, OverflowError):
                    published = None

            stories.append({
                "source": source,
                "title": html.unescape(re.sub(r"<[^>]+>", "", title)),
                "link": link,
                "published": published,
            })

        print(f"Fetched {len(stories)} stories from {source}")
        return stories

    except Exception as error:
        print(f"Warning: could not fetch {source}: {error}")
        return []



def categorize_story(story):
    text = story["title"].lower()

    categories = {
        "🚨 Vulnerability": [
            "cve-", "zero-day", "zero day", "vulnerability",
            "security flaw", "patch", "exploit", "mfa bypass",
            "bypass mfa", "remote code execution"
        ],
        "🦠 Malware & Ransomware": [
            "ransomware", "malware", "trojan", "rootkit",
            "botnet"
        ],
        "🕵️ Spyware & Surveillance": [
            "spyware", "pegasus", "surveillanceware"
        ],
        "🔓 Data Breach": [
            "data breach", "data leak", "leaked data",
            "stolen data", "exposed database", "exposed records",
            "credential theft"
        ],
        "🎯 Threat Intelligence": [
            "apt", "threat actor", "phishing campaign",
            "indicators of compromise", "ioc", "cyber espionage"
        ],
        "🛡️ Cyberattacks & Intrusions": [
            "cyberattack", "cyber attack", "hackers use",
            "breach company websites", "unauthorized access",
            "websites compromised", "systems compromised",
            "intrusion", "hacked"
        ],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "📰 Other"

def prioritize_story(story):
    text = story["title"].lower()

    high_priority = [
        "zero-day", "zero day",
        "actively exploited", "exploited in attacks",
        "remote code execution", "unauthenticated rce",
        "ransomware", "bypass mfa", "mfa bypass",
        "actively targeted", "critical vulnerability",
        "mass exploitation", "systems compromised",
        "spyware infection", "company websites"
    ]

    medium_priority = [
        "vulnerability", "security flaw", "data breach",
        "data leak", "phishing", "malware",
        "exploit", "credential theft", "spyware",
        "cyberattack", "cyber attack", "hacked",
        "stolen data", "account takeover",
        "security patch", "privilege escalation"
    ]

    if any(keyword in text for keyword in high_priority):
        return "🔴 HIGH"

    if any(keyword in text for keyword in medium_priority):
        return "🟡 MEDIUM"

    return "🟢 LOW"


def build_digest(stories):
    now = datetime.now(timezone.utc)
    lines = [
        ":newspaper: *Daily Cybersecurity News*",
        f"_Generated {now.strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
    ]

    if not stories:
        lines.append("No stories could be retrieved today.")
        return "\n".join(lines)

    for number, story in enumerate(stories, start=1):
        title = story["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        source = story["source"]
        link = story["link"]

        category = categorize_story(story)
        priority = prioritize_story(story)

        lines.append(f"*{number}. <{link}|{title}>*")
        lines.append(f"{priority} · {category} · _{source}_")
        
        lines.append("")

    lines.append(f"_Total stories: {len(stories)}_")
    return "\n".join(lines)


def post_to_slack(message):
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL_ID")

    if not token or not channel:
        raise RuntimeError(
            "Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID environment secret."
        )

    payload = json.dumps({
        "channel": channel,
        "text": message,
        "unfurl_links": False,
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
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
        error_code = result.get("error", "unknown_error")
        raise RuntimeError(f"Slack rejected the message: {error_code}")

    print("Successfully posted the cybersecurity digest to Slack.")


def main():
    print("CYBERSECURITY DAILY NEWS")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 50)

    all_stories = []
    for source, url in FEEDS:
        all_stories.extend(fetch_feed(source, url))

    all_stories.sort(
        key=lambda story: story["published"] or datetime.min.replace(
            tzinfo=timezone.utc
        ),
        reverse=True,
    )

    unique_stories = []
    seen_links = set()

    for story in all_stories:
        if story["link"] in seen_links:
            continue
        seen_links.add(story["link"])
        unique_stories.append(story)

    selected = unique_stories[:MAX_STORIES]

    for number, story in enumerate(selected, start=1):
        published = story["published"]
        date_text = (
            published.strftime("%Y-%m-%d %H:%M UTC")
            if published else "Date unavailable"
        )
        print(f"{number}. {story['title']}")
        print(f"   Source: {story['source']} | Published: {date_text}")
        print(f"   Link: {story['link']}")

    digest = build_digest(selected)
    post_to_slack(digest)

    print(f"Total stories: {len(selected)}")


if __name__ == "__main__":
    main()
