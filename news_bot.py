
import re
import html
import urllib.request
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


def main():
    print("CYBERSECURITY DAILY NEWS")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 50)

    all_stories = []
    for source, url in FEEDS:
        all_stories.extend(fetch_feed(source, url))

    # Keep recent stories first when publication dates are available.
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

    if not selected:
        print("\nNo stories could be retrieved. Check the feed warnings above.")
        return

    for number, story in enumerate(selected, start=1):
        published = story["published"]
        date_text = published.strftime("%Y-%m-%d %H:%M UTC") if published else "Date unavailable"

        print(f"\n{number}. {story['title']}")
        print(f"   Source: {story['source']} | Published: {date_text}")
        print(f"   Link: {story['link']}")

    print(f"\nTotal stories: {len(selected)}")


if __name__ == "__main__":
    main()
