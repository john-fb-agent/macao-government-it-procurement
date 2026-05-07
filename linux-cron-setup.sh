#!/bin/bash
# Linux Cron 設置腳本
# Macao Government IT Procurement Monitor

set -e

echo "=========================================="
echo "Linux Cron 設置 - IT Procurement Monitor"
echo "=========================================="

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安裝"
    exit 1
fi

echo "✅ Python3 已安裝: $(python3 --version)"

# 檢查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安裝"
    exit 1
fi

echo "✅ pip3 已安裝"

# 安裝依賴
echo ""
echo "安裝 Python 依賴..."
pip3 install beautifulsoup4 requests --user

echo "✅ 依賴安裝完成"

# 獲取項目路徑
echo ""
read -p "請輸入項目路徑 (默認: ~/macao-government-it-procurement): " PROJECT_PATH
PROJECT_PATH=${PROJECT_PATH:-~/macao-government-it-procurement}

# 檢查項目目錄
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ 項目目錄不存在: $PROJECT_PATH"
    echo "請先 clone repo:"
    echo "  git clone https://github.com/john-fb-agent/macao-government-it-procurement.git $PROJECT_PATH"
    exit 1
fi

echo "✅ 項目目錄: $PROJECT_PATH"

# 獲取絕對路徑
PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)

# 檢查配置文件
echo ""
echo "檢查配置文件..."
if [ ! -f "$PROJECT_PATH/config/config.json" ]; then
    echo "❌ 配置文件不存在"
    echo "請創建 $PROJECT_PATH/config/config.json"
    exit 1
fi

echo "✅ 配置文件存在"

# 配置 Telegram
echo ""
echo "配置 Telegram 通知..."
read -p "請輸入 Telegram Bot Token (留空則不設置): " BOT_TOKEN
read -p "請輸入 Telegram Chat ID (留空則不設置): " CHAT_ID

if [ -n "$BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
    # 更新配置文件
    python3 << EOF
import json
import os

config_path = "$PROJECT_PATH/config/config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

config['telegram']['bot_token'] = "$BOT_TOKEN"
config['telegram']['chat_id'] = "$CHAT_ID"

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("✅ Telegram 配置已更新")
EOF
else
    echo "⚠️  跳過 Telegram 配置（將使用環境變數）"
fi

# 創建 logs 目錄
mkdir -p "$PROJECT_PATH/logs"

# 創建 cron 腳本
echo ""
echo "創建 cron 執行腳本..."

CRON_SCRIPT="$PROJECT_PATH/run-cron.sh"

cat > "$CRON_SCRIPT" << 'EOF'
#!/bin/bash
# Cron 執行腳本

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/logs/cron-$(date +%Y%m%d_%H%M%S).log"

# 設置環境變數（如需要）
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

cd "$PROJECT_DIR"

# 執行主腳本
python3 src/main.py >> "$LOG_FILE" 2>&1

# 檢查執行結果
if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ 執行成功" >> "$LOG_FILE"
else
    echo "[$(date)] ❌ 執行失敗" >> "$LOG_FILE"
fi

# 清理舊日誌（保留30天）
find "$PROJECT_DIR/logs" -name "cron-*.log" -mtime +30 -delete
EOF

chmod +x "$CRON_SCRIPT"

echo "✅ Cron 腳本已創建: $CRON_SCRIPT"

# 設置 cron
echo ""
echo "設置 cron 任務..."
echo "選擇執行頻率:"
echo "1) 每週三 14:30 (原始設定)"
echo "2) 每天 14:30"
echo "3) 自定義"
read -p "請選擇 (1-3): " CRON_CHOICE

case $CRON_CHOICE in
    1)
        CRON_EXPR="30 14 * * 3"
        ;;
    2)
        CRON_EXPR="30 14 * * *"
        ;;
    3)
        read -p "請輸入 cron 表達式 (例如: 30 14 * * 3): " CRON_EXPR
        ;;
    *)
        echo "無效選擇，使用默認: 每週三 14:30"
        CRON_EXPR="30 14 * * 3"
        ;;
esac

# 創建 cron 任務
CRON_JOB="$CRON_EXPR $CRON_SCRIPT"

# 添加到 crontab
(crontab -l 2>/dev/null | grep -v "macao-government-it-procurement"; echo "$CRON_JOB") | crontab -

echo ""
echo "✅ Cron 任務已設置: $CRON_EXPR"
echo ""
echo "當前 crontab:"
crontab -l | grep "macao-government-it-procurement"

# 測試執行
echo ""
echo "=========================================="
echo "設置完成！"
echo "=========================================="
echo ""
echo "項目路徑: $PROJECT_PATH"
echo "Cron 表達式: $CRON_EXPR"
echo "執行腳本: $CRON_SCRIPT"
echo "日誌位置: $PROJECT_PATH/logs/"
echo ""
echo "測試執行:"
echo "  $CRON_SCRIPT"
echo ""
echo "查看日誌:"
echo "  tail -f $PROJECT_PATH/logs/cron-*.log"
echo ""
echo "編輯 crontab:"
echo "  crontab -e"
echo ""
echo "刪除 cron 任務:"
echo "  crontab -l | grep -v macao-government-it-procurement | crontab -"
echo ""

# 詢問是否立即測試
read -p "是否立即測試執行? (y/n): " TEST_NOW

if [ "$TEST_NOW" = "y" ] || [ "$TEST_NOW" = "Y" ]; then
    echo ""
    echo "開始測試執行..."
    "$CRON_SCRIPT"
    echo ""
    echo "測試完成！查看最新日誌:"
    ls -la "$PROJECT_PATH/logs/" | tail -5
fi
