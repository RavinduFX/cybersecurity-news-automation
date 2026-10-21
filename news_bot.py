    lines = [
        "*Daily Cybersecurity News Digest*",
        f"_{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
    ]

    for index, story in enumerate(selected_stories, start=1):
        priority = prioritize_story(story)
        labels = [priority]

        if is_known_exploited(story, kev_cves):
            labels.append("🚨 KNOWN EXPLOITED — CISA KEV")
        elif needs_urgent_attention(story):
            labels.append("🚨 POSSIBLY URGENT")

        category = categorize_story(story)
        title = escape_slack_text(story["title"])
        source = escape_slack_text(story["source"])
        link = story["link"]

        lines.append(
            f"{index}. *<{link}|{title}>*\n"
            f"   {' | '.join(labels)} | {category} | {source}"
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
        for story in fetch_feed(source, url):
            if story["link"] not in seen_links:
                seen_links.add(story["link"])
                all_stories.append(story)

    all_stories.sort(
        key=lambda story: story["published"],
        reverse=True,
    )

    kev_cves = fetch_cisa_kev()
    post_to_slack(build_digest(all_stories, kev_cves=kev_cves))


if __name__ == "__main__":
    main()
