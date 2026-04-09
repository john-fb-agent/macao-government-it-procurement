# 澳門政府 IT 採購監控系統

監控澳門政府部門資訊科技、軟件、硬件及網絡安全相關的採購公告。

## 資料來源

- **網址**: https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13
- **內容**: 澳門政府各部門採購公告
- **檢查頻率**: 每週四早上 8:30

## 監控關鍵詞

- 資訊科技 / Information Technology
- 軟件 / Software
- 硬件 / Hardware
- 電腦 / Computer
- 伺服器 / Server
- 網絡 / Network
- 網路 / Network
- 安全 / Security
- 防火牆 / Firewall
- 系統 / System
- 數據中心 / Data Center
- 雲端 / Cloud
- 軟體 / Software
- 硬體 / Hardware

## 網頁結構

每條公告包含：
- **部門**: 發佈部門名稱
- **摘要**: 採購內容摘要
- **《公報》編號**: 政府公報編號
- **日期**: 發佈日期

## GitHub Pages

- **所有記錄**: https://john-fb-agent.github.io/macao-government-it-procurement/
- **最近6個月**: https://john-fb-agent.github.io/macao-government-it-procurement/recent.html

## 技術架構

- **語言**: Python 3
- **爬蟲**: BeautifulSoup + requests
- **數據儲存**: JSON + Git
- **部署**: GitHub Pages
- **自動化**: OpenClaw Cron

## 目錄結構

```
.
├── README.md
├── docs/
│   ├── DESIGN.md
│   ├── API.md
│   └── CHANGELOG.md
├── src/
│   ├── scraper.py
│   ├── notifier.py
│   └── generator.py
├── data/
│   └── records.json
├── config/
│   └── config.example.json
├── .gitignore
└── .github/
    └── workflows/
        └── deploy.yml
```

## 開發者

- 作者: OpenClaw Agent
- 創建日期: 2026-04-09

## License

MIT License
