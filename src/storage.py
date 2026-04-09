#!/usr/bin/env python3
"""
澳門政府 IT 採購監控系統 - 數據儲存模組
"""

import json
import os
from datetime import datetime


class DataStorage:
    """管理數據儲存和檢索"""
    
    def __init__(self, data_path='data/records.json'):
        self.data_path = data_path
        self.data = self._load_data()
    
    def _load_data(self):
        """載入現有數據"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"警告: {self.data_path} 格式錯誤，創建新文件")
        
        return {
            'last_check': None,
            'total_records': 0,
            'records': []
        }
    
    def _save_data(self):
        """保存數據到文件"""
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_existing_ids(self):
        """獲取所有已存在的記錄 ID"""
        return {r['id'] for r in self.data['records']}
    
    def add_records(self, new_records):
        """添加新記錄"""
        existing_ids = self.get_existing_ids()
        added = []
        
        for record in new_records:
            if record['id'] not in existing_ids:
                self.data['records'].append(record)
                added.append(record)
                existing_ids.add(record['id'])
        
        if added:
            self.data['total_records'] = len(self.data['records'])
            self._save_data()
        
        return added
    
    def update_last_check(self, timestamp=None):
        """更新最後檢查時間"""
        self.data['last_check'] = timestamp or datetime.now().isoformat()
        self._save_data()
    
    def get_all_records(self):
        """獲取所有記錄"""
        return self.data['records']
    
    def get_recent_records(self, months=6):
        """獲取最近 N 個月的記錄"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        recent = []
        
        for record in self.data['records']:
            try:
                # 嘗試解析日期
                record_date = datetime.strptime(record['date'], '%Y-%m-%d')
                if record_date >= cutoff_date:
                    recent.append(record)
            except (ValueError, KeyError):
                # 如果日期無法解析，根據 found_at 判斷
                if 'found_at' in record:
                    try:
                        found_date = datetime.fromisoformat(record['found_at'])
                        if found_date >= cutoff_date:
                            recent.append(record)
                    except:
                        pass
        
        return recent
    
    def get_stats(self):
        """獲取統計資訊"""
        return {
            'total_records': self.data['total_records'],
            'last_check': self.data['last_check'],
            'by_department': self._count_by_department(),
            'by_keyword': self._count_by_keyword()
        }
    
    def _count_by_department(self):
        """按部門統計"""
        counts = {}
        for record in self.data['records']:
            dept = record.get('department', '未知')
            counts[dept] = counts.get(dept, 0) + 1
        return counts
    
    def _count_by_keyword(self):
        """按關鍵詞統計"""
        counts = {}
        for record in self.data['records']:
            for keyword in record.get('keywords_matched', []):
                counts[keyword] = counts.get(keyword, 0) + 1
        return counts


if __name__ == '__main__':
    storage = DataStorage()
    
    print("儲存統計:")
    stats = storage.get_stats()
    print(f"總記錄數: {stats['total_records']}")
    print(f"最後檢查: {stats['last_check']}")
    print(f"\n按部門分類:")
    for dept, count in sorted(stats['by_department'].items(), key=lambda x: -x[1]):
        print(f"  {dept}: {count}")
    print(f"\n按關鍵詞分類:")
    for kw, count in sorted(stats['by_keyword'].items(), key=lambda x: -x[1]):
        print(f"  {kw}: {count}")
