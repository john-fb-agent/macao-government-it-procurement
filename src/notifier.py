#!/usr/bin/env python3
"""
澳門政府 IT 採購監控系統 - 通知模組
"""

import json
import os
import requests
from datetime import datetime


class TelegramNotifier:
    """Telegram 通知器"""
    
    def __init__(self, config_path='config/config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.bot_token = self.config['telegram']['bot_token']
        self.chat_id = self.config['telegram']['chat_id']
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message, parse_mode='HTML'):
        """發送消息"""
        url = f"{self.api_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"發送通知失敗: {e}")
            return False
    
    def notify_new_records(self, records, stats):
        """通知新記錄"""
        if not records:
            return
        
        message = f"""🆕 <b>發現 {len(records)} 條新的 IT 採購公告</b>

📊 <b>統計</b>
• 總記錄數: {stats['total_records']}
• 本次新增: {len(records)}

📋 <b>新增記錄</b>
"""
        
        for i, record in enumerate(records[:10], 1):  # 最多顯示10條
            message += f"""
{i}. <b>{record['department']}</b>
   {record['summary'][:80]}...
   📅 {record['date']}
   🏷 {', '.join(record.get('keywords_matched', [])[:3])}
"""
        
        if len(records) > 10:
            message += f"\n... 還有 {len(records) - 10} 條記錄\n"
        
        message += f"\n🔗 <a href='https://john-fb-agent.github.io/macao-government-it-procurement/'>查看完整列表</a>"
        
        return self.send_message(message)
    
    def notify_success(self, stats, new_count=0):
        """通知執行成功"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"""✅ <b>檢查完成</b>

🕐 時間: {now}
📊 總記錄數: {stats['total_records']}
🆕 本次新增: {new_count}

<b>按部門分類:</b>
"""
        
        # 顯示前5個部門
        sorted_depts = sorted(stats['by_department'].items(), key=lambda x: -x[1])[:5]
        for dept, count in sorted_depts:
            message += f"• {dept}: {count}\n"
        
        message += f"\n🔗 <a href='https://john-fb-agent.github.io/macao-government-it-procurement/'>查看完整列表</a>"
        
        return self.send_message(message)
    
    def notify_error(self, error_message):
        """通知執行失敗"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"""❌ <b>檢查失敗</b>

🕐 時間: {now}
🔴 錯誤: {error_message[:200]}

請檢查日誌獲取詳細信息。
"""
        
        return self.send_message(message)


if __name__ == '__main__':
    notifier = TelegramNotifier()
    
    # 測試通知
    test_stats = {
        'total_records': 10,
        'by_department': {'部門A': 5, '部門B': 3, '部門C': 2},
        'by_keyword': {'軟件': 8, '硬件': 5}
    }
    
    notifier.notify_success(test_stats, 2)
