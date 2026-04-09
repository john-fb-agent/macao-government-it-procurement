# 澳門政府 IT 採購監控系統

監控澳門政府部門資訊科技、軟件、硬件及網絡安全相關的採購公告。

## 資料來源

- **網址**: https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13
- **內容**: 澳門政府各部門採購公告
- **檢查頻率**: 每週四早上 8:30

## 監控關鍵詞

### 明確 IT 關鍵詞
- 資訊科技 / Information Technology
- 軟件 / Software / 軟體
- 硬件 / Hardware / 硬體
- 電腦 / Computer
- 伺服器 / Server
- 網絡 / Network / 網路
- 資訊安全 / Information Security
- 防火牆 / Firewall
- 數據庫 / Database
- 數據中心 / Data Center
- 雲端 / Cloud
- 人工智能 / AI / Artificial Intelligence
- 大數據 / Big Data
- 平台 / Platform

### AI 智能判斷
除關鍵詞匹配外，系統還使用 **AI 智能過濾** (`src/ai_filter.py`)：
- 分析公告摘要的 IT 相關性
- 識別隱含的 IT 採購需求
- 排除非 IT 系統（消防、空調、電梯等）
- 判斷 IT 設備類型（電腦、伺服器、網絡設備等）

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
- **智能過濾**: 兩階段（關鍵詞 + AI 判斷）
- **數據儲存**: JSON + Git
- **部署**: GitHub Pages
- **自動化**: OpenClaw Cron (每週三 14:30)

## 目錄結構

```
.
├── README.md
├── docs/
│   ├── DESIGN.md          # 系統設計文檔
│   ├── API.md             # 網站結構分析
│   └── CHANGELOG.md       # 更新日誌
├── src/
│   ├── main.py            # 主程式
│   ├── scraper.py         # 爬蟲模組
│   ├── ai_filter.py       # AI 智能過濾
│   ├── storage.py         # 數據儲存
│   ├── generator.py       # HTML 生成
│   └── notifier.py        # 通知模組
├── data/
│   └── records.json       # 記錄數據
├── config/
│   ├── config.json        # 配置文件（實際使用）
│   └── config.example.json # 配置範例
├── logs/                   # 執行日誌
├── index.html             # 所有記錄頁面
├── recent.html            # 最近6個月頁面
└── .github/workflows/
    └── deploy.yml         # GitHub Pages 部署
```

## 執行記錄

| 日期 | 找到記錄 | 備註 |
|------|----------|------|
| 2026-04-09 | 1 條 | 澳門大學 - 量子材料平台 |

## 開發者

- 作者: OpenClaw Agent
- 創建日期: 2026-04-09
- 版本: v1.1.0

## License

MIT License
