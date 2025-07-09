#!/usr/bin/env python3
import re
import json
import sqlite3
import asyncio
import logging
import socket
import ssl
from datetime import datetime
from urllib.parse import urlparse, urljoin

import httpx
from httpx_socks import AsyncProxyTransport
from bs4 import BeautifulSoup

# === CONFIG ===
PROXY_URL = "socks5://127.0.0.1:9050"
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; OnionScanner/1.0)'}
RE_ONION_V3 = re.compile(r'\b[a-z2-7]{56}\.onion\b')

RE_PGP_KEY = re.compile(
    r"-----BEGIN PGP (PUBLIC|PRIVATE) KEY BLOCK-----.*?-----END PGP \1 KEY BLOCK-----",
    re.DOTALL | re.IGNORECASE
)

SEEDS = {
    "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion",
    "http://propublica.securedrop.tor.onion",
    "http://onionrot.abusus.org",
    "http://onion.live/trending",
    "http://onionzwpil5nbukgflurrfvommx6aznkz7aaqh2gwm4qsxjj6yvihxid.onion",
    "http://torlistbsvieqsqctmi5fv2dbfxg7p3x77po7fhdcwfcr3xv5shxmzad.onion",
     "https://onionindex.org/",
    "https://tordir.org/",
    "http://ahmia.fi/onions"
}

DIRS_TO_SCRAPE = [
    "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion",
    "http://propublica.securedrop.tor.onion",
    "http://onionrot.abusus.org",
    "http://onion.live/trending",
    "http://onionzwpil5nbukgflurrfvommx6aznkz7aaqh2gwm4qsxjj6yvihxid.onion",
    "http://torlistbsvieqsqctmi5fv2dbfxg7p3x77po7fhdcwfcr3xv5shxmzad.onion",
     "https://onionindex.org/",
    "https://tordir.org/",
    "http://ahmia.fi/onions"
]

ALL_OUTPUT = "out.jsonl"
ACTIVE_FILE = "active_onions.jsonl"
INACTIVE_FILE = "inactive_onions.jsonl"
DB_FILE = "onions2.db"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# === DATABASE ===
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS scanned (
    url TEXT PRIMARY KEY,
    status INT,
    title TEXT,
    scanned_at TEXT,
    pgp_key TEXT
)
""")
conn.commit()

def parse_metadata(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
    except Exception:
        title = ""
    desc = ""
    meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", property="og:description")
    if meta:
        desc = meta.get("content", "")
    return title, desc

def extract_onions(html, base_url=None):
    onions = set(RE_ONION_V3.findall(html or ""))
    soup = BeautifulSoup(html or "", "html.parser")
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a['href']) if base_url else a['href']
        match = RE_ONION_V3.search(href)
        if match:
            onions.add(match.group(0))
    return onions

def extract_pgp_keys(text):
    return [m.group(0) for m in RE_PGP_KEY.finditer(text or "")]

async def fetch_url(url, client):
    try:
        r = await client.get(url, follow_redirects=True)
        return {"status": r.status_code, "html": r.text, "headers": r.headers}
    except Exception as e:
        logging.warning(f"[FAILED] {url} — {e}")
        return None

async def scan_onion(url, client, scanned_set, to_crawl):
    if url in scanned_set:
        return None

    result = await fetch_url(url, client)
    now = datetime.utcnow().isoformat() + "Z"

    if result:
        title, desc = parse_metadata(result["html"])
        pgp_keys = extract_pgp_keys(result["html"])
        pgp_key_text = "\n\n".join(pgp_keys) if pgp_keys else ""

        new_onions = extract_onions(result["html"], base_url=url)
        for new_url in new_onions:
            full_url = "http://" + new_url if not new_url.startswith("http") else new_url
            if full_url not in scanned_set and full_url not in to_crawl:
                to_crawl.add(full_url)

        cur.execute("""
            INSERT OR REPLACE INTO scanned (url, status, title, scanned_at, pgp_key) 
            VALUES (?, ?, ?, ?, ?)
        """, (url, result["status"], title, now, pgp_key_text))
        conn.commit()

        record = {
            "url": url,
            "status": result["status"],
            "title": title,
            "description": desc,
            "headers": dict(result["headers"]),
            "timestamp": now,
            "pgp_key_found": bool(pgp_keys),
            "pgp_key": pgp_key_text if pgp_keys else None,
        }

        return record
    else:
        return {"url": url, "status": 0, "error": "Fetch failed", "timestamp": now}

async def pull_directory_onions(client):
    found = set()
    for url in DIRS_TO_SCRAPE:
        resp = await fetch_url(url, client)
        if resp:
            found.update(extract_onions(resp["html"], base_url=url))
    return found

async def main():
    scanned_set = {row[0] for row in cur.execute("SELECT url FROM scanned")}
    to_crawl = set(SEEDS) - scanned_set
    transport = AsyncProxyTransport.from_url(PROXY_URL)
    concurrency = 10

    while True:
        if not to_crawl:
            logging.info("🔄 Pulling new links from onion directories...")
            async with httpx.AsyncClient(transport=transport, headers=HEADERS, timeout=30) as client:
                new_onions = await pull_directory_onions(client)
                to_crawl.update({"http://" + o if not o.startswith("http") else o for o in new_onions if o not in scanned_set})
            if not to_crawl:
                logging.info("💤 No new links found. Sleeping for 60 seconds...")
                await asyncio.sleep(60)
                continue

        logging.info(f"🔎 Starting batch scan — {len(to_crawl)} remaining")
        with open(ALL_OUTPUT, "a", encoding="utf-8") as allf, \
             open(ACTIVE_FILE, "a", encoding="utf-8") as activef, \
             open(INACTIVE_FILE, "a", encoding="utf-8") as inactivef:

            async with httpx.AsyncClient(transport=transport, headers=HEADERS, timeout=30) as client:
                semaphore = asyncio.Semaphore(concurrency)

                async def worker(url):
                    async with semaphore:
                        result = await scan_onion(url, client, scanned_set, to_crawl)
                        if result:
                            scanned_set.add(url)
                            json.dump(result, allf)
                            allf.write("\n")

                            if result["status"] == 200:
                                json.dump(result, activef)
                                activef.write("\n")
                                logging.info(f"[LIVE] {url}")
                            else:
                                json.dump(result, inactivef)
                                inactivef.write("\n")
                                logging.info(f"[DEAD] {url}")

                batch = list(to_crawl)[:concurrency]
                to_crawl.difference_update(batch)
                await asyncio.gather(*(worker(url) for url in batch))
                await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Interrupted by user")
    finally:
        conn.close()
