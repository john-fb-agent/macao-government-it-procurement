#!/usr/bin/env python3
"""
澳門政府 IT 採購監控系統 - 爬蟲模組
"""

import requests
import json
import hashlib
import re
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class ProcurementScraper:
    """爬取澳門政府採購公告"""
    
    def __init__(self, config_path='config/config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.target_url = self.config['target_url']
        self.keywords = [k.lower() for k in self.config['keywords']]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        })
    
    def fetch_page(self, url=None, retries=3):
        """獲取網頁內容"""
        url = url or self.target_url
        
        for attempt in range(retries):
            try:
                print(f"正在獲取: {url} (嘗試 {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"請求失敗: {e}")
                if attempt < retries - 1:
                    import time
                    time.sleep(5)
                else:
                    raise
    
    def parse_announcements(self, html):
        """解析公告列表"""
        soup = BeautifulSoup(html, 'html.parser')
        announcements = []
        
        # 查找所有公告項目
        # 根據實際網頁結構調整選擇器
        news_items = soup.find_all('div', class_='news-item') or \
                     soup.find_all('div', class_='item') or \
                     soup.find_all('tr') or \
                     soup.find_all('div', class_=re.compile('news|item|list'))
        
        print(f"找到 {len(news_items)} 個項目")
        
        for item in news_items:
            try:
                announcement = self._extract_announcement(item)
                if announcement:
                    announcements.append(announcement)
            except Exception as e:
                print(f"解析項目失敗: {e}")
                continue
        
        return announcements
    
    def _extract_announcement(self, item):
        """從單個項目中提取公告資訊"""
        # 嘗試多種選擇器
        title_elem = (item.find('a', class_='title') or 
                     item.find('a', class_='news-title') or
                     item.find('a') or
                     item.find('div', class_='title'))
        
        if not title_elem:
            return None
        
        title_text = title_elem.get_text(strip=True)
        
        # 提取部門（【】內的文字）
        dept_match = re.search(r'【(.+?)】', title_text)
        department = dept_match.group(1) if dept_match else '未知部門'
        
        # 提取摘要（【】後的文字）
        summary = re.sub(r'【.+?】', '', title_text).strip()
        
        # 提取連結
        link = title_elem.get('href', '') if title_elem.name == 'a' else ''
        if link and not link.startswith('http'):
            link = urljoin(self.target_url, link)
        
        # 提取日期
        date_elem = (item.find('span', class_='date') or
                    item.find('td', class_='date') or
                    item.find('div', class_='date'))
        date = date_elem.get_text(strip=True) if date_elem else ''
        
        # 提取公報編號
        bulletin_elem = (item.find('span', class_='bulletin') or
                        item.find('span', class_=re.compile('bulletin|公報')) or
                        item.find('td', string=re.compile('《公報》')))
        bulletin_number = bulletin_elem.get_text(strip=True) if bulletin_elem else ''
        
        # 生成唯一 ID
        content = f"{department}{summary}{date}"
        record_id = hashlib.md5(content.encode()).hexdigest()[:12]
        
        return {
            'id': record_id,
            'department': department,
            'summary': summary,
            'bulletin_number': bulletin_number,
            'date': date,
            'url': link,
            'title': title_text
        }
    
    def filter_it_related(self, announcements):
        """過濾 IT 相關公告"""
        it_announcements = []
        
        for ann in announcements:
            text = f"{ann['department']} {ann['summary']}".lower()
            matched_keywords = []
            
            for keyword in self.keywords:
                if keyword in text:
                    matched_keywords.append(keyword)
            
            if matched_keywords:
                ann['keywords_matched'] = matched_keywords
                ann['found_at'] = datetime.now().isoformat()
                it_announcements.append(ann)
                print(f"✓ IT 相關: {ann['department']} - {ann['summary'][:50]}...")
        
        return it_announcements
    
    def scrape(self):
        """執行完整爬取流程"""
        print("=" * 60)
        print("開始爬取澳門政府採購公告")
        print("=" * 60)
        
        # 獲取網頁
        html = self.fetch_page()
        
        # 解析公告
        all_announcements = self.parse_announcements(html)
        print(f"\n總共找到 {len(all_announcements)} 條公告")
        
        # 過濾 IT 相關
        it_announcements = self.filter_it_related(all_announcements)
        print(f"\nIT 相關公告: {len(it_announcements)} 條")
        
        return it_announcements


if __name__ == '__main__':
    scraper = ProcurementScraper()
    results = scraper.scrape()
    
    print("\n" + "=" * 60)
    print("爬取結果")
    print("=" * 60)
    for item in results[:5]:  # 只顯示前5條
        print(f"\n部門: {item['department']}")
        print(f"摘要: {item['summary'][:80]}...")
        print(f"日期: {item['date']}")
        print(f"關鍵詞: {', '.join(item.get('keywords_matched', []))}")
