#!/usr/bin/env python3
"""
澳門政府 IT 採購監控系統 - 主程式
"""

import sys
import os
import json
import subprocess
import traceback
from datetime import datetime

# 添加 src 到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper import ProcurementScraper
from storage import DataStorage
from notifier import TelegramNotifier
from generator import HTMLGenerator


def setup_logging():
    """設置日誌"""
    log_dir = '../logs'
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    class Logger:
        def __init__(self, filepath):
            self.terminal = sys.stdout
            self.log = open(filepath, 'w', encoding='utf-8')
        
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
            self.log.flush()
        
        def flush(self):
            self.terminal.flush()
            self.log.flush()
    
    sys.stdout = Logger(log_file)
    sys.stderr = sys.stdout
    
    return log_file


def git_commit_and_push():
    """提交並推送到 GitHub"""
    try:
        print("\n" + "=" * 60)
        print("提交到 GitHub")
        print("=" * 60)
        
        # 配置 git
        subprocess.run(['git', 'config', 'user.email', 'openclaw@bot.local'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'OpenClaw Bot'], check=True)
        
        # 添加文件
        subprocess.run(['git', 'add', 'data/records.json', 'index.html', 'recent.html'], check=True)
        
        # 提交
        result = subprocess.run(
            ['git', 'commit', '-m', f'Update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("提交成功")
            # 推送
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print("推送到 GitHub 成功")
            return True
        else:
            if 'nothing to commit' in result.stdout or 'nothing to commit' in result.stderr:
                print("沒有變更需要提交")
                return True
            print(f"提交失敗: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失敗: {e}")
        return False
    except Exception as e:
        print(f"Git 操作異常: {e}")
        return False


def main():
    """主程式"""
    print("=" * 60)
    print("澳門政府 IT 採購監控系統")
    print(f"開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 設置日誌
    log_file = setup_logging()
    print(f"日誌文件: {log_file}")
    
    try:
        # 初始化組件
        scraper = ProcurementScraper('../config/config.json')
        storage = DataStorage('../data/records.json')
        notifier = TelegramNotifier('../config/config.json')
        
        # 1. 爬取網頁
        print("\n" + "=" * 60)
        print("步驟 1: 爬取網頁")
        print("=" * 60)
        new_records = scraper.scrape()
        
        # 2. 儲存數據
        print("\n" + "=" * 60)
        print("步驟 2: 儲存數據")
        print("=" * 60)
        added_records = storage.add_records(new_records)
        storage.update_last_check()
        
        print(f"新增記錄: {len(added_records)} 條")
        
        # 3. 發送通知（新記錄）
        if added_records:
            print("\n" + "=" * 60)
            print("步驟 3: 發送新記錄通知")
            print("=" * 60)
            stats = storage.get_stats()
            notifier.notify_new_records(added_records, stats)
        
        # 4. 生成 HTML
        print("\n" + "=" * 60)
        print("步驟 4: 生成 HTML 頁面")
        print("=" * 60)
        generator = HTMLGenerator('../data/records.json', '..')
        generator.generate()
        
        # 5. 提交到 GitHub
        git_commit_and_push()
        
        # 6. 發送成功通知
        print("\n" + "=" * 60)
        print("步驟 5: 發送成功通知")
        print("=" * 60)
        stats = storage.get_stats()
        notifier.notify_success(stats, len(added_records))
        
        print("\n" + "=" * 60)
        print("執行完成!")
        print(f"結束時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print("\n" + "=" * 60)
        print("❌ 執行失敗!")
        print(f"錯誤: {error_msg}")
        print("=" * 60)
        
        traceback.print_exc()
        
        # 發送失敗通知
        try:
            notifier = TelegramNotifier('../config/config.json')
            notifier.notify_error(error_msg)
        except:
            pass
        
        return 1


if __name__ == '__main__':
    exit(main())
