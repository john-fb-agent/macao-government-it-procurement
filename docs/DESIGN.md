# 系統設計文檔

## 系統概述

自動監控澳門政府採購公告網站，識別與 IT 相關的採購項目，並通過 GitHub Pages 展示。

## 系統架構

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│   OpenClaw Cron │────▶│   Scraper   │────▶│   Parser    │
│  (每週四 8:30)  │     │  (Python)   │     │  (Python)   │
└─────────────────┘     └─────────────┘     └──────┬──────┘
                                                   │
                          ┌─────────────┐         │
                          │   Notifier  │◀────────┘
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

### 3. Filter (src/scraper.py)

**功能**: 過濾 IT 相關公告
**關鍵詞**:
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
1. Cron 觸發
   │
   ▼
2. Scraper 爬取網頁
   │
   ▼
3. Parser 解析 HTML
   │
   ▼
4. Filter 過濾 IT 公告
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
