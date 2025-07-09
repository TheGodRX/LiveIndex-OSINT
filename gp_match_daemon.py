#!/usr/bin/env python3
import sqlite3
import time
import hashlib
from collections import defaultdict
import re

DB_FILE = "onions2.db"
OUTPUT_FILE = "pgp_matches.txt"
SLEEP_SECONDS = 30

def hash_key(pgp_key):
    return hashlib.sha256(pgp_key.encode()).hexdigest()

def normalize_key(pgp_key):
    return pgp_key.strip()

def load_existing_matches():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return set(re.findall(r'Key Fingerprint \(SHA-256\): (\w+)', f.read()))
    except FileNotFoundError:
        return set()

def fetch_pgp_data():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT url, pgp_key, title FROM scanned WHERE pgp_key IS NOT NULL AND pgp_key != ''")
    rows = cur.fetchall()
    conn.close()
    return rows

def scan_for_matches(known_hashes):
    rows = fetch_pgp_data()
    pgp_map = defaultdict(list)

    for url, key, title in rows:
        norm_key = normalize_key(key)
        pgp_map[norm_key].append((url, title or "(No Title Found)"))

    matched = {}
    for key, entries in pgp_map.items():
        if len(entries) > 1:
            key_hash = hash_key(key)
            if key_hash not in known_hashes:
                matched[key_hash] = (key, entries)

    return matched

def append_matches(matches):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        for key_hash, (pgp_key, entries) in matches.items():
            f.write("====================================================================\n")
            f.write("🔐 Reused PGP Key Match\n")
            f.write("====================================================================\n")
            f.write(f"Used by {len(entries)} onion site(s)\n")
            f.write(f"Key Fingerprint (SHA-256): {key_hash}\n\n")
            f.write(pgp_key + "\n\n")
            f.write("🧭 Associated .onion URLs:\n")
            for url, title in entries:
                f.write(f" - {url:<40} | \"{title}\"\n")
            f.write("\n--------------------------------------------------------------------\n\n")

def main_loop():
    print("🔍 PGP monitor running — will update when reused keys are found...\n")
    known_hashes = load_existing_matches()

    try:
        while True:
            new_matches = scan_for_matches(known_hashes)
            if new_matches:
                print(f"✅ {len(new_matches)} new reused PGP key(s) found and written to report")
                append_matches(new_matches)
                known_hashes.update(new_matches.keys())
            else:
                print("🔄 No new reused PGP keys found.")
            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped by user.")

if __name__ == "__main__":
    main_loop()
