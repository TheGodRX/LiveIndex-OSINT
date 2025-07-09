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

## 🤝 Contributing

Got a feature idea or UI enhancement? PRs welcome!

```bash
# Fork and clone your copy
git checkout -b feature/my-enhancement
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

Give it a star 🌟 — it helps boost visibility and supports development!

