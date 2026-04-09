# 系統設計文檔

## 系統概述

自動監控澳門政府採購公告網站，識別與 IT 相關的採購項目，並通過 GitHub Pages 展示。

## 系統架構

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│   OpenClaw Cron │────▶│   Scraper   │────▶│   Parser    │
│  (每週三 14:30) │     │  (Python)   │     │  (Python)   │
└─────────────────┘     └─────────────┘     └──────┬──────┘
                                                   │
                          ┌─────────────┐         │
                          │  AI Filter  │◀────────┘
                          │(智能判斷IT) │
                          └──────┬──────┘
                                 │
                          ┌─────────────┐
                          │   Notifier  │
                          │  (Telegram) │
                          └─────────────┘
                                   │
                          ┌─────────────┐
                          │   Storage   │
                          │  (JSON/Git) │
                          └──────┬──────┘
                                 │
                          ┌─────────────┐
                          │   GitHub    │
                          │   Pages     │
                          └─────────────┘
```

## 核心模組

### 1. Scraper (src/scraper.py)

**功能**: 爬取網頁內容
**輸入**: 目標 URL
**輸出**: HTML 內容

**流程**:
1. 發送 HTTP GET 請求
2. 設置 User-Agent 和 Headers
3. 處理重試機制
4. 返回 HTML

### 2. Parser (src/scraper.py)

**功能**: 解析 HTML，提取公告資訊
**輸入**: HTML 內容
**輸出**: 公告列表

**提取欄位**:
- 部門 (department)
- 摘要 (summary)
- 公報編號 (bulletin_number)
- 日期 (date)
- 連結 (url)

### 3. Filter (src/scraper.py + src/ai_filter.py)

**功能**: 兩階段智能過濾 IT 相關公告

**第一階段 - 關鍵詞過濾**:
- 資訊科技、Information Technology
- 軟件/軟體、Software
- 硬件/硬體、Hardware
- 電腦、Computer
- 伺服器、Server
- 網絡/網路、Network
- 安全、Security
- 防火牆、Firewall
- 系統、System
- 數據中心、Data Center
- 雲端、Cloud
- 人工智能、AI、Big Data
- 平台、Platform、Database

**第二階段 - AI 智能判斷** (src/ai_filter.py):
- 分析公告部門和摘要內容
- 識別隱含的 IT 相關性
- 排除非 IT 系統（消防、空調、電梯等）
- 判斷 IT 設備類型（電腦、伺服器、網絡設備等）
- 輸出判斷原因和分類

### 4. Storage (src/storage.py)

**功能**: 數據持久化
**格式**: JSON
**結構**:
```json
{
  "last_check": "2026-04-09T08:30:00",
  "records": [
    {
      "id": "hash",
      "department": "部門名稱",
      "summary": "摘要內容",
      "bulletin_number": "公報編號",
      "date": "2026-04-09",
      "url": "https://...",
      "found_at": "2026-04-09T08:30:00",
      "keywords_matched": ["軟件", "系統"]
    }
  ]
}
```

### 5. Notifier (src/notifier.py)

**功能**: 發送通知
**渠道**: Telegram
**觸發條件**:
- 發現新記錄
- 執行成功（帶統計）
- 執行失敗（帶錯誤信息）

### 6. Generator (src/generator.py)

**功能**: 生成 HTML 頁面
**輸出**:
- `index.html` - 所有記錄
- `recent.html` - 最近6個月記錄

## 數據流

```
1. Cron 觸發 (每週三 14:30)
   │
   ▼
2. Scraper 爬取網頁
   │
   ▼
3. Parser 解析 HTML
   │
   ▼
4. Filter 兩階段過濾
   │  ├─ 4a. 關鍵詞快速匹配
   │  └─ 4b. AI 智能判斷
   │
   ▼
5. Storage 比對新記錄
   │
   ├─▶ 有新記錄 ──▶ Notifier 發送通知
   │
   ▼
6. Storage 保存數據
   │
   ▼
7. Generator 生成 HTML
   │  ├─ index.html (所有記錄)
   │  └─ recent.html (最近6個月)
   │
   ▼
8. Git push 到 GitHub
   │
   ▼
9. GitHub Pages 自動更新
```

## 錯誤處理

| 錯誤類型 | 處理方式 |
|----------|----------|
| 網絡超時 | 重試 3 次，每次間隔 5 秒 |
| HTTP 錯誤 | 記錄錯誤，發送通知 |
| 解析失敗 | 記錄錯誤，發送通知 |
| Git 推送失敗 | 記錄錯誤，發送通知 |

## 安全考量

- 不儲存敏感資訊在代碼中
- 使用環境變數管理配置
- 遵守網站 robots.txt
- 控制請求頻率

## 擴展性

- 可添加更多關鍵詞
- 可擴展到多個網站
- 可添加更多通知渠道
- 可擴展 AI 判斷邏輯（如使用 LLM）
- 可添加更多數據分析功能

## 執行記錄

| 日期 | 版本 | 更新內容 |
|------|------|----------|
| 2026-04-09 | v1.0.0 | 初始版本，基礎爬蟲和關鍵詞過濾 |
| 2026-04-09 | v1.1.0 | 添加 AI 智能過濾模組，優化判斷邏輯 |

## 定時執行

- **頻率**: 每週三下午 2:30 (Asia/Shanghai)
- **超時**: 1 小時 (3600 秒)
- **通知**: Telegram (成功/失敗)
- **日誌**: `logs/run_YYYYMMDD_HHMMSS.log`
