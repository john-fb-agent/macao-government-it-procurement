# 遷移指南 - Macao Government IT Procurement Monitor

## 📦 已 Clone Repo 後的步驟

### 1️⃣ 安裝依賴

```bash
cd macao-government-it-procurement

# Python 依賴
pip3 install beautifulsoup4 requests

# 如果需要 Playwright（推薦用於解決連接問題）
pip3 install playwright
playwright install chromium
```

### 2️⃣ 配置 Telegram（用於通知）

**獲取 Bot Token**：
1. 在 Telegram 找 @BotFather
2. 創建新 bot 或獲取現有 bot token
3. 獲取你的 Chat ID（找 @userinfobot）

**更新配置**：
```bash
# 編輯 config/config.json
{
  "telegram": {
    "bot_token": "你的實際_TOKEN",
    "chat_id": "你的實際_CHAT_ID"
  },
  "target_url": "https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13",
  "keywords": [...],
  "exclude_keywords": [...]
}
```

### 3️⃣ 測試運行

```bash
# 測試澳門採購監控
python3 src/main.py
```

---

## 🤖 定期任務說明

### Macao Government IT Procurement Monitor

| 項目 | 內容 |
|------|------|
| **執行頻率** | 每週三 14:30 (Asia/Shanghai) |
| **超時時間** | 1 小時 (3600 秒) |
| **執行模式** | Isolated Agent Turn |
| **模型** | qwencode/kimi-k2.5 |
| **通知渠道** | Telegram |

---

## 📋 指導其他 Agent 的說明

請將以下內容給新 agent：

### 任務：Macao Government IT Procurement Monitor

```markdown
## 任務說明：Macao Government IT Procurement Monitor

**執行頻率**：每週三 14:30 (Asia/Shanghai)
**超時**：1 小時

### 步驟：

1. **爬取網頁**
   - 目標：https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13
   - 注意：可能需要 Playwright 或代理
   - 如果直接請求失敗，使用備用方案

2. **解析公告列表**
   - 提取：部門名稱、摘要內容、公報編號、日期、URL
   - 使用 BeautifulSoup 解析 HTML

3. **過濾 IT 相關公告**
   - 關鍵詞匹配（軟件、硬件、系統、平台等）
   - AI 智能判斷（使用 ai_filter.py）

4. **保存數據**
   - 新記錄保存到 data/records.json
   - 避免重複記錄

5. **生成 HTML 頁面**
   - index.html（所有記錄）
   - recent.html（最近6個月）

6. **推送到 GitHub**
   ```bash
   git add data/records.json index.html recent.html
   git commit -m "Update: $(date)"
   git push origin main
   ```

7. **發送執行摘要到 Telegram**

### 關鍵詞配置（config/config.json）：

**包含**：
- 資訊科技、Information Technology
- 軟件/軟體、Software
- 硬件/硬體、Hardware
- 電腦、Computer
- 伺服器、Server
- 網絡/網路、Network
- 系統、System
- 平台、Platform
- 雲端、Cloud
- AI、人工智能
- 數據庫、Database

**排除**：
- 清潔、保安、餐飲、消防系統等

### 注意事項：

- 網站可能有反爬蟲機制
- 連接超時時使用 Playwright
- 確保 GitHub Pages 已啟用
- 檢查 Telegram Token 有效性
```

---

## 🛠️ 環境要求

### 必需：
- Python 3.8+
- Git
- 網絡連接（可能需澳門代理）

### Python 包：
```
beautifulsoup4
requests
playwright（推薦）
```

### 配置文件：
- `config/config.json` - Telegram Token 和 Chat ID

### GitHub：
- 倉庫需啟用 GitHub Pages
- 需要寫權限

---

## 📁 項目結構

```
macao-government-it-procurement/
├── src/
│   ├── main.py              # 主程式
│   ├── scraper.py           # 基礎爬蟲
│   ├── scraper_v2.py        # 增強版爬蟲
│   ├── scraper_playwright.py # Playwright 爬蟲
│   ├── ai_filter.py         # AI 智能過濾
│   ├── storage.py           # 數據儲存
│   ├── generator.py         # HTML 生成
│   └── notifier.py          # Telegram 通知
├── config/
│   └── config.json          # 配置文件
├── data/
│   └── records.json         # 記錄數據
├── docs/
│   ├── DESIGN.md
│   ├── API.md
│   └── CHANGELOG.md
└── .github/workflows/
    └── deploy.yml           # GitHub Pages 部署
```

---

## 🔧 故障排除

### 問題：網站連接超時

**解決方案**：
1. 使用 Playwright 版本：
   ```bash
   python3 src/scraper_playwright.py
   ```

2. 或使用代理（如果在澳門本地）：
   ```python
   proxies = {
       'http': 'http://proxy:port',
       'https': 'http://proxy:port'
   }
   response = requests.get(url, proxies=proxies)
   ```

### 問題：Telegram 通知失敗

**檢查**：
- Bot Token 是否正確
- Chat ID 是否正確
- Bot 是否已添加到對話

### 問題：GitHub 推送失敗

**檢查**：
- Git 憑證是否配置
- 是否有寫權限
- 遠程倉庫 URL 是否正確
