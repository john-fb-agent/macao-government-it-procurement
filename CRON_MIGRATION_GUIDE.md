# Cron 任務遷移指南

## 📋 原始 Cron 任務詳情

### 基本資訊
| 項目 | 值 |
|------|-----|
| **Job ID** | `91af5fe0-2711-49ad-b007-4925f5c2c3a8` |
| **名稱** | Macao Government IT Procurement Monitor |
| **執行頻率** | 每週三 14:30 (Asia/Shanghai) |
| **超時時間** | 3600 秒 (1 小時) |
| **模型** | qwencode/kimi-k2.5 |

### 執行內容 (Payload)
```json
{
  "kind": "agentTurn",
  "message": "Execute the Macao Government IT Procurement monitoring script:\n\ncd ~/gh-repo/macao-government-it-procurement && python3 src/main.py\n\nThis script:\n1. Scrapes https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13\n2. Filters IT-related procurements (software, hardware, network, security, etc.)\n3. Saves new records to data/records.json\n4. Generates GitHub Pages (index.html and recent.html)\n5. Pushes to GitHub\n\nTimeout: 1 hour (3600 seconds)\nLog all output.\nNotify user on success or failure with summary.",
  "model": "qwencode/kimi-k2.5",
  "timeoutSeconds": 3600
}
```

### 通知設定
| 項目 | 值 |
|------|-----|
| **模式** | announce |
| **渠道** | telegram |
| **目標** | 190623454 |

---

## 🚀 遷移選項

### 選項 1: Linux Cron (crontab)

**適用於**: 有 Linux 服務器或本地機器

```bash
# 編輯 crontab
crontab -e

# 添加以下行（每週三 14:30 執行）
30 14 * * 3 cd ~/macao-government-it-procurement && python3 src/main.py >> logs/cron.log 2>&1
```

**需要**: 
- Python 3.8+
- 安裝依賴: `pip3 install beautifulsoup4 requests`
- Telegram Bot Token 和 Chat ID 配置

---

### 選項 2: GitHub Actions (推薦)

**適用於**: 使用 GitHub 托管

創建 `.github/workflows/scheduled.yml`:

```yaml
name: Scheduled IT Procurement Monitor

on:
  schedule:
    # 每週三 14:30 UTC+8 (06:30 UTC)
    - cron: '30 6 * * 3'
  workflow_dispatch:  # 允許手動觸發

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install beautifulsoup4 requests
      
      - name: Run monitor
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          cd src && python3 main.py
      
      - name: Commit and push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/records.json index.html recent.html
          git diff --quiet && git diff --staged --quiet || git commit -m "Update: $(date)"
          git push
```

**需要設置 Secrets**:
- `TELEGRAM_BOT_TOKEN`: 你的 Telegram Bot Token
- `TELEGRAM_CHAT_ID`: 你的 Chat ID

---

### 選項 3: Docker + Cron

**適用於**: 容器化部署

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製代碼
COPY . .

# 設置 cron
RUN apt-get update && apt-get install -y cron
RUN echo "30 14 * * 3 cd /app && python3 src/main.py >> logs/cron.log 2>&1" | crontab -

# 啟動 cron
CMD ["cron", "-f"]
```

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  monitor:
    build: .
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
```

---

### 選項 4: 雲服務 (AWS Lambda / Google Cloud Functions)

**適用於**: 無服務器架構

**AWS Lambda 示例**:
```python
import json
import subprocess
import os

def lambda_handler(event, context):
    # 設置環境變數
    os.environ['TELEGRAM_BOT_TOKEN'] = 'your_token'
    os.environ['TELEGRAM_CHAT_ID'] = 'your_chat_id'
    
    # 執行腳本
    result = subprocess.run(
        ['python3', 'src/main.py'],
        capture_output=True,
        text=True
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    }
```

**EventBridge 規則**:
- 類型: Schedule
- 表達式: `cron(30 6 ? * 3 *)`  # 每週三 06:30 UTC

---

## 📦 遷移檢查清單

### 1. 環境準備
- [ ] Python 3.8+ 已安裝
- [ ] 安裝依賴: `beautifulsoup4`, `requests`
- [ ] Git 已配置
- [ ] 網絡連接正常

### 2. 配置文件
- [ ] `config/config.json` 已更新 Telegram Token
- [ ] `data/records.json` 已複製歷史數據
- [ ] `.gitignore` 已配置（忽略敏感文件）

### 3. GitHub 設定
- [ ] 倉庫已創建
- [ ] GitHub Pages 已啟用
- [ ] Secrets 已設置（如使用 GitHub Actions）

### 4. 測試
- [ ] 手動執行 `python3 src/main.py` 成功
- [ ] Telegram 通知正常接收
- [ ] GitHub Pages 更新正常

---

## 🔧 故障排除

### 問題: 403 Forbidden
**解決**: 使用 Playwright 或代理
```bash
pip install playwright
playwright install chromium
# 使用 src/scraper_playwright.py
```

### 問題: Connection Timeout
**解決**: 增加超時時間或使用代理
```python
response = requests.get(url, timeout=60)
```

### 問題: Telegram 通知失敗
**解決**: 檢查 Token 和 Chat ID
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>&text=Test"
```

---

## 📊 執行記錄對比

| 日期 | 原始 Cron | 新環境 |
|------|-----------|--------|
| 2026-04-09 | ✅ 成功 | 待測試 |
| 2026-04-15 | ✅ 成功 | 待測試 |
| 2026-04-22 | ✅ 成功 | 待測試 |
| 2026-04-29 | ❌ Timeout | 待測試 |
| 2026-05-06 | ❌ 403 Forbidden | 待測試 |

---

## 📝 重要提醒

1. **備份數據**: 遷移前備份 `data/records.json`
2. **測試執行**: 遷移後手動測試一次
3. **監控狀態**: 前幾次執行密切關注
4. **保留原 Cron**: 確認新環境穩定後再刪除原 Cron

---

需要我幫你設置特定的遷移方案嗎？
