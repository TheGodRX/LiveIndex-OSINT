# 🕵 LiveIndex-OSINT — Onion Crawler & Live Intelligence Dashboard

**LiveIndex-OSINT** is a powerful open-source dark web crawler and intelligence toolkit for `.onion` sites. Unlike typical scrapers, this system **actively discovers**, **indexes**, and **analyzes live onion services**, capturing metadata and PGP keys in real time — all accessible through a clean Web UI dashboard.

---

## 🚀 Features

✅ **Crawls .onion sites via Tor** (using SOCKS5)  
✅ **Extracts page metadata** (title, description, HTTP status)  
✅ **Identifies and saves PGP public/private key blocks**  
✅ **Discovers new onions from visited pages**  
✅ **Stores results in SQLite & JSONL logs**  
✅ **Includes a Flask-based Web UI** for browsing, searching, and filtering onions  
✅ **Smart deduplication** — skips already-indexed sites  
✅ **Designed for OSINT workflows** and dark web research

---

## 🧠 Why It's Better Than Standard Crawlers

| Feature | LiveIndex-OSINT | Traditional Crawlers |
|--------|------------------|-----------------------|
| 🚪 Onion Routing | ✅ Full Tor Proxy Support | ❌ Usually Clear-Net Only |
| 🔐 PGP Key Extraction | ✅ Extracts & Indexes Keys | ❌ No Support |
| 📚 Live Metadata Indexing | ✅ Title, Desc, Status | ⚠️ Basic or None |
| 🔄 Recursive Discovery | ✅ From directories & pages | ❌ Static seed-based |
| 🖥️ Integrated Web UI | ✅ Search & Dashboard | ❌ CLI Only |
| 📈 Active vs Inactive Detection | ✅ Tracked & Split | ❌ No Health Checks |
| 🧩 OSINT Ready | ✅ Structured DB + JSON | ❌ Unstructured Dumps |

---

## 📦 Installation

1. **Clone the Repo**

```bash
git clone https://github.com/TheGodRX/LiveIndex-OSINT.git
cd LiveIndex-OSINT
```

2. **Install Dependencies**

Make sure you're using Python 3.9+.

```bash
sudo apt install sqlite3
sudo apt install libsqlite3-dev
pip install -r requirements.txt
```

3. **Start Tor**

Ensure Tor is running locally (default SOCKS5: `127.0.0.1:9050`)

```bash
# Debian/Ubuntu
tor
sudo service tor start
```

4. **Run the Crawler**

```bash
python indexer.py
```

Let it run in the background. It will automatically:
- Load seed onion directories
- Crawl & index live .onion pages
- Log metadata and discovered onions
- Extract embedded PGP key blocks
- Store everything to `onions2.db` and JSONL files

---

## 🌐 Web UI Usage

1. **Launch the Web Dashboard**
-In a new tab or terminal window run..:
```bash
python webUI.py
```

2. **Access the UI**

Open your browser and go to:

```
http://localhost:3000
```

### 🔎 What You Can Do

- View & search indexed `.onion` links
- Filter by **live/dead** status
- Read extracted **PGP keys**
- Explore full metadata for each domain
- Export results for further OSINT investigation
- Host as a hidden service

---

## 🗂️ Output Files

| File | Description |
|------|-------------|
| `onions2.db` | SQLite DB with all indexed results |
| `out.jsonl` | All scan logs (one JSON per line) |
| `active_onions.jsonl` | Live `.onion` pages |
| `inactive_onions.jsonl` | Dead/unreachable sites |

---

## 🧰 Tech Stack

- `httpx_socks` for Tor over SOCKS5
- `asyncio` for concurrent crawling
- `sqlite3` for lightweight storage
- `Flask` for the Web UI
- `re` for regex-based PGP and onion detection

---

## 🔐 PGP Key Extraction

The crawler looks for GPG/PGP blocks like:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
...
-----END PGP PUBLIC KEY BLOCK-----
```

These are stored and searchable through the Web UI — ideal for tracking actor identities, crypto wallets, or hidden forums.

---

## 📊 Example Use Cases

- Dark web monitoring & intelligence
- Threat actor tracking (PGP reuse)
- Crawling decentralized marketplaces
- Academic research on hidden services
- Live domain monitoring & OSINT archiving

---

## 🔍 Real-Time PGP Reuse Detection (pgp_match_daemon.py)

In addition to indexing `.onion` sites and their metadata, LiveIndex-OSINT includes a **PGP Key Match Daemon** — a continuously running script that monitors your SQLite database (`onions2.db`) and identifies any **reused PGP keys** across different dark web sites.

### 💡 What It Does

- Watches the database in real time for new entries with PGP key blocks  
- Matches identical PGP keys reused across different `.onion` URLs  
- Outputs a clean and readable OSINT report in `pgp_matches.txt`  
- Includes the **full PGP key**, matching URL list, and **site titles**  
- Helps correlate hidden services that may be operated by the same entity

### 📈 Why It’s Awesome

- 🧠 **Uncovers operational links** between threat actors or marketplaces  
- 🔁 **Runs continuously**, always monitoring for new PGP reuse  
- 📄 **Generates human-readable reports** with structured key and site data  
- 🕵️‍♂️ **Perfect for OSINT analysts**, journalists, or law enforcement mapping onion ecosystems

Sample Output (pgp_matches.txt)
markdown
Copy
Edit
====================================================================
🔐 Reused PGP Key Match
====================================================================
Used by 3 onion site(s)
Key Fingerprint (SHA-256): 8a7c6f9e92f6cbde66c5bd3f4f716b4be1d99d5ddbe63e9e92b69e56e25d8a24

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: OpenPGP.js v4.10.10

xsBNBFmABCABC...
...
-----END PGP PUBLIC KEY BLOCK-----

🧭 Associated .onion URLs:
 - http://marketxyz.onion           | "XYZ Market"
 - http://securechatxyz.onion       | "Secure Drop Alpha"
 - http://unknownforum77.onion      | "(No Title Found)"

--------------------------------------------------------------------
This script empowers deep linkage analysis of hidden services based on cryptographic reuse — a vital tool in modern darknet OSINT workflows.

### ▶️ How to Use It

Open a new terminal (while `indexer.py` is running) and execute:

```bash
python pgp_match_daemon.py

```

---

## ⚠️ Legal Notice

This tool is for **educational and lawful OSINT research only**. Do not use it to access illegal content. You're responsible for ensuring compliance with your jurisdiction’s laws.

---

## 📫 Contact

**Author**: [TheGodRX](https://github.com/TheGodRX)  
DM via GitHub or submit issues via the [Issues tab](https://github.com/TheGodRX/LiveIndex-OSINT/issues)

---

## ⭐️ If you like this project...
<img src="https://raw.githubusercontent.com/TheGodRX/LiveIndex-OSINT/refs/heads/main/donate.svg" width="200" />
DONATE XMR TO:  42uJeqTHZbgVhrGvkjBTRTMTavgNQSVJ64YLVGdiPMuP4s3zdXv6rr5HSSVo7yvDACPtXv9bdZ554Hf1rstvzL4sEgSVeT9 
DONATE BTC TO: 34SJhbCJAjMB9NpXxXiKBR7BAGNQFrKgFN

Give it a star 🌟 — it helps boost visibility and supports development!

