#!/usr/bin/env python3
"""
澳門政府 IT 採購監控系統 - AI 智能過濾模組
使用 AI 判斷摘要是否與 IT 相關
"""

import json
import os
from typing import List, Dict, Any


class AIFilter:
    """使用 AI 判斷公告是否與 IT 相關"""
    
    def __init__(self):
        self.it_categories = [
            "資訊科技設備",
            "電腦硬件",
            "伺服器設備",
            "網絡設備",
            "軟件系統",
            "應用程式開發",
            "數據庫系統",
            "資訊安全",
            "網絡安全",
            "防火牆",
            "雲端服務",
            "數據中心",
            "IT 顧問服務",
            "系統整合",
            "軟件開發",
            "硬件維護",
            "資訊系統",
            "電子化系統",
            "數碼化系統",
            "智能系統",
            "AI 系統",
            "人工智能",
            "大數據分析",
            "物聯網",
            "網絡基礎設施",
            "通訊設備",
            "視訊系統",
            "會議系統",
            "投影設備",
            "顯示設備",
            "打印設備",
            "掃描設備",
            "儲存設備",
            "備份系統",
            "虛擬化",
            "容器化",
            "DevOps",
        ]
    
    def analyze_relevance(self, department: str, summary: str) -> tuple[bool, str, List[str]]:
        """
        分析公告是否與 IT 相關
        
        Returns:
            (is_relevant, reason, matched_categories)
        """
        text = f"{department} {summary}".lower()
        
        # 明確的 IT 關鍵詞（直接判定為相關）
        direct_it_keywords = [
            "資訊科技", "information technology", "it 系統", "資訊系統",
            "電腦", "computer", "伺服器", "server",
            "軟件", "software", "軟體", "應用程式",
            "硬件", "hardware", "硬體",
            "網絡", "network", "網路", "網絡安全", "network security",
            "防火牆", "firewall",
            "數據庫", "database", "資料庫",
            "雲端", "cloud", "雲服務",
            "數據中心", "data center",
            "人工智能", "ai ", "artificial intelligence",
            "大數據", "big data",
            "平台", "platform",
            "系統開發", "系統建設", "系統採購",
            "虛擬化", "virtualization",
            "備份", "backup",
            "網站", "website", "網頁", "web ",
            "軟件開發", "系統開發", "程式開發",
            "資訊安全", "information security", "cybersecurity",
            "數碼化", "數字化", "digitalization",
            "電子化", "electronic",
            "智能", "智慧", "intelligent", "smart ",
            "物聯網", "iot", "internet of things",
        ]
        
        # 檢查明確 IT 關鍵詞
        for keyword in direct_it_keywords:
            if keyword.lower() in text:
                return True, f"包含明確 IT 關鍵詞: {keyword}", ["明確 IT 關鍵詞"]
        
        # 可能是 IT 相關的關鍵詞（需要進一步判斷）
        possible_it_keywords = [
            "系統", "system",
            "設備", "equipment",
            "技術", "technology",
            "服務", "service",
            "採購", "procurement",
        ]
        
        has_possible_keyword = any(kw in text for kw in possible_it_keywords)
        
        if not has_possible_keyword:
            return False, "無 IT 相關關鍵詞", []
        
        # 排除明確非 IT 的項目
        non_it_keywords = [
            "清潔", "保安", "餐飲", "膳食", "餐飲",
            "綠化", "園藝",
            "搬運", "運輸", "物流",
            "維修", "修理", "保養",
            "消防", "滅火",
            "醫療", "醫院", "診所",
            "教學", "培訓", "教育",
            "印刷", "影印",
            "租賃", "租賃", "rental",
            "租車", "車輛",
            "制服", "服裝",
            "家具", "傢俱", "辦公桌", "椅子",
            "裝修", "裝潢", "裝飾",
            "電梯", "升降機",
            "冷氣", "空調", "hvac",
            "電力", "電工", "電氣",
            "水電", "管道",
            "土木", "建築", "工程",
            "測量", "勘測",
            "保險", "insurance",
            "會計", "審計", "audit",
            "法律", "legal",
            "翻譯", "傳譯",
            "活動", "event", "典禮",
            "旅遊", "旅行",
            "酒店", "住宿",
        ]
        
        for keyword in non_it_keywords:
            if keyword in text:
                return False, f"明確非 IT 項目: {keyword}", []
        
        # 如果包含"系統"，進一步判斷是什麼系統
        if "系統" in summary or "system" in summary.lower():
            # 檢查是否為 IT 系統
            it_system_indicators = [
                "資訊", "信息", "information",
                "管理", "management",
                "數據", "data",
                "電子", "electronic",
                "數碼", "數字", "digital",
                "智能", "智慧", "intelligent",
                "自動", "automatic",
                "網絡", "網路", "network",
                "軟件", "軟體", "software",
                "應用", "application",
                "平台", "platform",
                "資料庫", "數據庫", "database",
                "雲端", "cloud",
                "虛擬", "virtual",
                "整合", "integration",
                "升級", "upgrade",
                "開發", "development",
                "建設", "construction",
                "採購", "procurement",
            ]
            
            for indicator in it_system_indicators:
                if indicator in text:
                    return True, f"IT 系統相關: {indicator}", ["IT 系統"]
            
            # 如果是其他類型的系統（如消防系統、空調系統），排除
            non_it_systems = [
                "消防", "fire",
                "空調", "冷氣", "air conditioning",
                "通風", "ventilation",
                "電梯", "升降機", "elevator",
                "電力", "供電", "electrical",
                "照明", "lighting",
                "給水", "排水", "plumbing",
                "保安", "security",
                "監控", "cctv",
                "門禁", "access control",
            ]
            
            for non_it in non_it_systems:
                if non_it in text:
                    return False, f"非 IT 系統: {non_it}", []
        
        # 如果包含"設備"或"硬件"，判斷是否為 IT 設備
        if "設備" in summary or "equipment" in summary.lower() or "硬件" in summary or "硬體" in summary:
            it_equipment_indicators = [
                "電腦", "computer",
                "伺服器", "server",
                "網絡", "network",
                "通訊", "communication",
                "資訊", "information",
                "數據", "data",
                "電子", "electronic",
                "數碼", "digital",
                "智能", "smart",
                "終端", "terminal",
                "工作站", "workstation",
                "儲存", "storage",
                "備份", "backup",
                "打印", "print",
                "掃描", "scan",
                "投影", "projector",
                "顯示", "display",
                "視訊", "video",
                "會議", "conference",
            ]
            
            for indicator in it_equipment_indicators:
                if indicator in text:
                    return True, f"IT 設備相關: {indicator}", ["IT 設備"]
        
        # 默認：不相關
        return False, "無法確定為 IT 相關", []
    
    def filter_announcements(self, announcements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        過濾公告，使用 AI 判斷是否與 IT 相關
        """
        it_announcements = []
        
        print(f"\n開始 AI 智能過濾 {len(announcements)} 條公告...")
        
        for i, ann in enumerate(announcements, 1):
            department = ann.get('department', '')
            summary = ann.get('summary', '')
            
            is_relevant, reason, categories = self.analyze_relevance(department, summary)
            
            if is_relevant:
                ann['ai_matched'] = True
                ann['ai_reason'] = reason
                ann['ai_categories'] = categories
                it_announcements.append(ann)
                print(f"  ✓ AI 判斷相關 [{i}/{len(announcements)}]: {department} - {summary[:50]}...")
                print(f"    原因: {reason}")
            else:
                if i <= 10 or i % 20 == 0:  # 只顯示前10條和每20條的排除信息
                    print(f"  ✗ AI 判斷不相關 [{i}/{len(announcements)}]: {department}")
                    print(f"    原因: {reason}")
        
        print(f"\nAI 判斷完成: {len(it_announcements)}/{len(announcements)} 條相關")
        
        return it_announcements