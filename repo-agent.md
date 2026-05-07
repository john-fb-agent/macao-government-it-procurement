# AGENTS.md — AI Agent Guide

**Last Updated:** 2026-04-29 | **Author:** Killua (OpenClaw Agent)
**Last Review:** 2026-04-29

---

## 🤖 Purpose

This file is for AI agents working in this repository. For **development workflows**, see the `github-repo-dev` skill instead of duplicating rules here.

---

## 📖 What Is This Repo?

**macao-government-it-procurement** monitors Macau government IT-related procurement announcements.

### Core Mission
Scrape the Macau Legal Affairs Bureau (DSAJ) tender listings page (`/?d=13` = 公開競投 服務提供/物品供應), filter for IT-related procurements, and publish them to GitHub Pages.

### Data Flow
```
DSAJ Website → scraper.py → ai_filter.py → records.json → generator.py → index.html/recent.html → GitHub Pages
```

### Key URLs
- **Source:** https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13
- **Published:** https://john-fb-agent.github.io/macao-government-it-procurement/
- **Recent (6mo):** https://john-fb-agent.github.io/macao-government-it-procurement/recent.html

---

## 📂 Repository Structure

```
macao-government-it-procurement/
├── repo-agent.md      ← YOU ARE HERE (repo-specific info)
├── README.md          ← Human-facing overview
├── docs/
│   ├── DESIGN.md      ← System design docs
│   ├── API.md         ← Website structure analysis
│   └── CHANGELOG.md   ← Update history
├── src/
│   ├── main.py        ← Entry point (run the scraper)
│   ├── scraper.py     ← Fetch + parse DSAJ tender listings
│   ├── ai_filter.py   ← AI-powered IT relevance filter
│   ├── storage.py     ← Save/load records.json
│   ├── generator.py   ← Generate static HTML pages
│   └── notifier.py   ← Send notifications (Telegram/etc)
├── data/
│   └── records.json   ← IT procurement records (JSON)
├── config/
│   ├── config.json    ← Active config
│   └── config.example.json
└── index.html / recent.html  ← Generated output pages
```

---

## 🔑 Key Concepts

### IT Keywords (Include)
- 資訊科技 / Information Technology
- 軟件 / Software / 軟體
- 硬件 / Hardware / 硬體
- 電腦 / Computer / 伺服器 / Server
- 網絡 / Network / 防火牆 / Firewall
- 數據庫 / Database / 數據中心 / Data Center
- 雲端 / Cloud / 人工智能 / AI / 大數據 / Big Data
- 平台 / Platform

### Exclude Keywords
- 消防系統, 安全救助, 保安服務, 清潔服務, 餐飲, 物業管理

### Record Schema (records.json)
```json
{
  "id": "sha-hash",
  "department": "部門名稱",
  "summary": "採購摘要",
  "bulletin_number": "《公報》第X期,第二組,YYYY/MM/DD",
  "date": "YYYY/MM/DD",
  "url": "https://.../[link id]",
  "title": "【部門】公告一則，關於...",
  "keywords_matched": ["matched", "keywords"],
  "ai_matched": true,
  "ai_reason": "AI判斷理由",
  "ai_categories": ["IT 系統"],
  "match_type": "keyword" | "ai",
  "found_at": "ISO timestamp"
}
```

---

## ⚙️ How to Run

### Run scraper
```bash
cd /home/js/.openclaw/workspace/github-repos/macao-government-it-procurement
python3 src/main.py
```

### Cron job
- **Schedule:** Wed 14:30 (Asia/Shanghai/Macau — both GMT+8)
- **Repo path:** `/home/js/.openclaw/workspace/github-repos/macao-government-it-procurement`
- **Timeout:** 3600 seconds (1 hour)
- **Check:** `openclaw cron list`

### Manual test
```bash
python3 -c "from src.scraper import fetch_tenders; print(fetch_tenders())"
python3 -c "from src.ai_filter import is_it_procurement; print(is_it_procurement('...'))"
```

---

## 🔐 Important Notes

### Website Blocking
- DSAJ blocks browser (WAF) — use `web_fetch` or `requests`
- Chrome DevTools will get blocked

### Date Format Bug (Fixed)
- Dates in records.json use `YYYY/MM/DD` format
- generator.py normalizes to `YYYY-MM-DD` before parsing (`.replace('/', '-')`)

---

## 📞 References

- **DSAJ Source:** https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13
- **GitHub Pages:** https://john-fb-agent.github.io/macao-government-it-procurement/
- **Repo:** https://github.com/john-fb-agent/macao-government-it-procurement

---

_Last updated by Killua on 2026-04-29 | Last Review: 2026-04-29_
