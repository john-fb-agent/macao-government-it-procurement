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
        
        # 查找所有公告項目 - 根據實際網頁結構
        # 網頁使用 dl > dt/dd 結構
        news_items = soup.find_all('dl') or \
                     soup.find_all('div', class_=re.compile('news|item|list|result')) or \
                     soup.find_all('tr') or \
                     soup.find_all('article')
        
        print(f"找到 {len(news_items)} 個項目")
        
        # 如果沒有找到項目，嘗試直接解析整個內容區域
        if not news_items:
            content_div = soup.find('div', id='content') or \
                         soup.find('div', class_='content') or \
                         soup.find('main') or \
                         soup.body
            if content_div:
                # 嘗試查找所有包含鏈接的段落
                news_items = content_div.find_all(['p', 'div', 'li'])
                print(f"從內容區找到 {len(news_items)} 個項目")
        
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
        # 獲取所有文本內容
        text = item.get_text(strip=True)
        
        # 查找所有鏈接
        links = item.find_all('a')
        
        # 嘗試找到部門鏈接（通常是第一個鏈接）
        dept_link = None
        bulletin_link = None
        
        for link in links:
            href = link.get('href', '')
            link_text = link.get_text(strip=True)
            
            # 檢查是否是部門鏈接（包含 /link/ 或部門名稱）
            if '/link/' in href and not dept_link:
                dept_link = link
            # 檢查是否是公報鏈接
            elif 'bo.dsaj.gov.mo/bo/' in href or '《公報》' in link_text:
                bulletin_link = link
        
        if not dept_link:
            return None
        
        # 提取部門名稱
        department = dept_link.get_text(strip=True)
        
        # 提取摘要 - 在部門鏈接之後的文本
        # 移除所有鏈接文本，保留純文本內容
        summary = text
        for link in links:
            summary = summary.replace(link.get_text(strip=True), '', 1)
        
        # 清理摘要
        summary = re.sub(r'^\s*[,，]?\s*', '', summary)  # 移除開頭的標點
        summary = re.sub(r'\s+', ' ', summary)  # 規範化空白
        
        # 提取公報編號
        bulletin_number = ''
        if bulletin_link:
            bulletin_number = bulletin_link.get_text(strip=True)
        else:
            # 嘗試從文本中提取
            bulletin_match = re.search(r'《公報》[^\n]+', text)
            if bulletin_match:
                bulletin_number = bulletin_match.group(0).strip()
        
        # 提取日期
        date = ''
        date_match = re.search(r'(\d{4}/\d{2}/\d{2})', text)
        if date_match:
            date = date_match.group(1)
        
        # 提取連結
        link = dept_link.get('href', '')
        if link and not link.startswith('http'):
            link = urljoin(self.target_url, link)
        
        # 生成唯一 ID
        content = f"{department}{summary}{date}"
        record_id = hashlib.md5(content.encode()).hexdigest()[:12]
        
        return {
            'id': record_id,
            'department': department,
            'summary': summary[:200],  # 限制長度
            'bulletin_number': bulletin_number,
            'date': date,
            'url': link,
            'title': f"【{department}】{summary[:100]}"
        }
    
    def filter_it_related(self, announcements):
        """過濾 IT 相關公告 - 結合關鍵詞和 AI 判斷"""
        from ai_filter import AIFilter
        
        it_announcements = []
        exclude_keywords = [k.lower() for k in self.config.get('exclude_keywords', [])]
        ai_filter = AIFilter()
        
        print(f"\n第一階段：關鍵詞過濾 {len(announcements)} 條公告...")
        
        # 第一階段：關鍵詞過濾
        keyword_matched = []
        remaining = []
        
        for ann in announcements:
            text = f"{ann['department']} {ann['summary']}".lower()
            matched_keywords = []
            
            # 檢查是否包含排除關鍵詞
            excluded = False
            for exclude_kw in exclude_keywords:
                if exclude_kw in text:
                    excluded = True
                    print(f"✗ 排除 (包含 '{exclude_kw}'): {ann['department']} - {ann['summary'][:50]}...")
                    break
            
            if excluded:
                continue
            
            # 檢查是否包含 IT 關鍵詞
            for keyword in self.keywords:
                if keyword in text:
                    matched_keywords.append(keyword)
            
            if matched_keywords:
                ann['keywords_matched'] = matched_keywords
                ann['found_at'] = datetime.now().isoformat()
                ann['match_type'] = 'keyword'
                keyword_matched.append(ann)
                print(f"✓ IT 相關（關鍵詞）: {ann['department']} - {ann['summary'][:50]}...")
            else:
                remaining.append(ann)
        
        print(f"\n關鍵詞匹配: {len(keyword_matched)} 條")
        print(f"待 AI 判斷: {len(remaining)} 條")
        
        # 第二階段：AI 智能判斷
        if remaining:
            print(f"\n第二階段：AI 智能判斷...")
            ai_matched = ai_filter.filter_announcements(remaining)
            
            for ann in ai_matched:
                ann['match_type'] = 'ai'
                keyword_matched.append(ann)
        
        it_announcements = keyword_matched
        
        print(f"\n{'='*60}")
        print(f"過濾完成：關鍵詞 {len([a for a in it_announcements if a.get('match_type')=='keyword'])} 條 + AI {len([a for a in it_announcements if a.get('match_type')=='ai'])} 條 = {len(it_announcements)} 條")
        print(f"{'='*60}")
        
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
