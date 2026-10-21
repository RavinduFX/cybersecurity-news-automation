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
CISA_KEV_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)
CVE_PATTERN = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.IGNORECASE)

FEEDS = [
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
]

CATEGORY_KEYWORDS = {
    "🦠 Malware & Ransomware": [
        "ransomware", "malware", "infostealer",
        "information stealer", "trojan", "backdoor",
        "botnet", "credential stealer",
    ],
    "🕵️ Spyware & Surveillance": [
        "spyware", "surveillance", "stalkerware", "keylogger",
    ],
    "🔓 Data Breach": [
        "data breach", "data leak", "exposed records",
        "stolen data", "personal information exposed",
    ],
    "🔐 Certificate & Trust Infrastructure": [
        "certificate authority compromise",
        "certificate authority", "certificate authorities",
        "ca compromise", "ca keys", "ca key",
        "compromised ca", "compromised certificate authority",
        "certificate authority keys", "certificate authority key",
        "trust infrastructure", "code signing certificate",
        "digital certificate", "certificate revocation",
        "tls certificate", "ssl certificate", "root certificate",
        "root ca", "certificate issuer", "certificate issuance",
        "public key infrastructure", "pki",
    ],
    "🎯 Threat Intelligence": [
        "threat intelligence", "threat actor",
        "indicators of compromise", "ioc", "apt group",
        "cyber espionage",
    ],
    "🛡️ Cyberattacks & Intrusions": [
        "cyberattack campaign", "cyberattack", "cyber attacks",
        "cyber attack", "cybercriminal attack", "cyber crime",
        "cybercrime", "unauthorized access", "hacking", "hacker",
        "hackers", "intrusion", "phishing", "account takeover",
        "security breach", "network attack", "computer attack",
        "systems compromised", "system compromised",
        "compromised by hackers", "websites compromised",
        "compromised by attackers", "attacker gained access",
        "attack campaign", "breached network",
    ],
    "🚨 Vulnerability": [
        "critical vulnerability", "vulnerability", "zero-day",
        "zero day", "security flaw", "remote code execution",
        "rce", "privilege escalation", "exploit",
        "authentication bypass",
    ],
}

SOC_KEYWORDS = [
    "threat intelligence", "incident response",
    "security operations", "soc", "siem", "detection",
    "indicators of compromise", "ioc", "intrusion",
    "malware", "ransomware", "phishing", "exploit",
    "vulnerability", "data breach", "cyberattack",
    "cyber attack", "zero-day", "zero day",
    "certificate authority", "unauthorized access",
    "compromised by hackers", "hackers",
]


def clean_text(value):
    """Decode HTML entities and remove markup from feed text."""
    if not value:
        return ""

    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(value.split())
