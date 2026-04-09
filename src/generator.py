#!/usr/bin/env python3
"""
澳門政府 IT 採購監控系統 - HTML 生成器
"""

import json
import os
from datetime import datetime, timedelta


class HTMLGenerator:
    """生成 HTML 頁面"""
    
    def __init__(self, data_path='data/records.json', output_dir='.'):
        self.data_path = data_path
        self.output_dir = output_dir
        
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def _get_base_template(self):
        """基礎 HTML 模板 - 暗黑模式"""
        return """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: #f0f6fc;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 10px;
            border: 1px solid #30363d;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #58a6ff;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
            color: #8b949e;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            text-align: center;
            border: 1px solid #30363d;
        }}
        
        .stat-card h3 {{
            color: #58a6ff;
            font-size: 2em;
            margin-bottom: 5px;
        }}
        
        .stat-card p {{
            color: #8b949e;
        }}
        
        .filters {{
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            border: 1px solid #30363d;
        }}
        
        .filters input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #30363d;
            border-radius: 8px;
            font-size: 16px;
            background: #0d1117;
            color: #c9d1d9;
        }}
        
        .filters input::placeholder {{
            color: #6e7681;
        }}
        
        .record {{
            background: #161b22;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #30363d;
        }}
        
        .record:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            border-color: #58a6ff;
        }}
        
        .record-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }}
        
        .department {{
            background: #1f6feb;
            color: #f0f6fc;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .date {{
            color: #8b949e;
            font-size: 0.9em;
        }}
        
        .summary {{
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #c9d1d9;
        }}
        
        .keywords {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .keyword {{
            background: #238636;
            color: #f0f6fc;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }}
        
        .bulletin {{
            color: #8b949e;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .link {{
            color: #58a6ff;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .link:hover {{
            text-decoration: underline;
            color: #79c0ff;
        }}
        
        footer {{
            text-align: center;
            padding: 40px 20px;
            color: #8b949e;
            border-top: 1px solid #30363d;
            margin-top: 40px;
        }}
        
        footer a {{
            color: #58a6ff;
        }}
        
        .nav {{
            background: #161b22;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            border: 1px solid #30363d;
        }}
        
        .nav a {{
            color: #58a6ff;
            text-decoration: none;
            margin-right: 20px;
            font-weight: 500;
        }}
        
        .nav a:hover {{
            text-decoration: underline;
            color: #79c0ff;
        }}
        
        .nav a.active {{
            color: #f0f6fc;
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏛️ 澳門政府 IT 採購監控</h1>
            <p>自動追蹤資訊科技、軟件、硬件及網絡安全相關的政府採購公告</p>
        </header>
        
        {nav}
        
        <div class="stats">
            <div class="stat-card">
                <h3>{total_records}</h3>
                <p>總記錄數</p>
            </div>
            <div class="stat-card">
                <h3>{last_check}</h3>
                <p>最後更新</p>
            </div>
            <div class="stat-card">
                <h3>{departments}</h3>
                <p>涉及部門</p>
            </div>
        </div>
        
        <div class="filters">
            <input type="text" id="search" placeholder="🔍 搜索部門、摘要或關鍵詞..." onkeyup="filterRecords()">
        </div>
        
        <div id="records">
            {records}
        </div>
        
        <footer>
            <p>數據來源: <a href="https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13" target="_blank">澳門政府採購公告</a></p>
            <p>最後更新: {update_time}</p>
            <p>自動生成 by OpenClaw</p>
        </footer>
    </div>
    
    <script>
        function filterRecords() {{
            const input = document.getElementById('search');
            const filter = input.value.toLowerCase();
            const records = document.getElementsByClassName('record');
            
            for (let i = 0; i < records.length; i++) {{
                const text = records[i].textContent.toLowerCase();
                records[i].style.display = text.includes(filter) ? '' : 'none';
            }}
        }}
    </script>
</body>
</html>"""
    
    def _format_record(self, record):
        """格式化單條記錄為 HTML"""
        keywords_html = ''.join([
            f'<span class="keyword">{kw}</span>'
            for kw in record.get('keywords_matched', [])
        ])
        
        bulletin = record.get('bulletin_number', '')
        bulletin_html = f'<div class="bulletin">📰 {bulletin}</div>' if bulletin else ''
        
        url = record.get('url', '')
        summary = record.get('summary', '')
        if url:
            summary = f'<a href="{url}" target="_blank" class="link">{summary}</a>'
        
        return f"""
        <div class="record">
            <div class="record-header">
                <span class="department">{record.get('department', '未知部門')}</span>
                <span class="date">{record.get('date', '')}</span>
            </div>
            <div class="summary">{summary}</div>
            <div class="keywords">{keywords_html}</div>
            {bulletin_html}
        </div>
        """
    
    def generate_all_records_page(self):
        """生成所有記錄頁面"""
        records = self.data.get('records', [])
        # 按日期倒序排列
        records = sorted(records, key=lambda x: x.get('date', ''), reverse=True)
        
        records_html = ''.join([self._format_record(r) for r in records])
        
        # 統計
        total = len(records)
        departments = len(set(r.get('department', '') for r in records))
        last_check = self.data.get('last_check', '從未')[:10] if self.data.get('last_check') else '從未'
        
        nav = '''<div class="nav">
            <a href="index.html" class="active">📋 所有記錄</a>
            <a href="recent.html">📅 最近6個月</a>
        </div>'''
        
        html = self._get_base_template().format(
            title='澳門政府 IT 採購監控 - 所有記錄',
            nav=nav,
            total_records=total,
            last_check=last_check,
            departments=departments,
            records=records_html,
            update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        output_path = os.path.join(self.output_dir, 'index.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"已生成: {output_path} ({total} 條記錄)")
        return output_path
    
    def generate_recent_page(self, months=6):
        """生成最近6個月記錄頁面"""
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        
        recent_records = []
        for record in self.data.get('records', []):
            try:
                record_date = datetime.strptime(record.get('date', ''), '%Y-%m-%d')
                if record_date >= cutoff_date:
                    recent_records.append(record)
            except:
                # 如果無法解析日期，檢查 found_at
                if 'found_at' in record:
                    try:
                        found_date = datetime.fromisoformat(record['found_at'])
                        if found_date >= cutoff_date:
                            recent_records.append(record)
                    except:
                        pass
        
        # 按日期倒序排列
        recent_records = sorted(recent_records, key=lambda x: x.get('date', ''), reverse=True)
        
        records_html = ''.join([self._format_record(r) for r in recent_records])
        
        if not records_html:
            records_html = '<div class="record"><p style="text-align:center;color:#999;">暫無記錄</p></div>'
        
        # 統計
        total = len(recent_records)
        departments = len(set(r.get('department', '') for r in recent_records))
        last_check = self.data.get('last_check', '從未')[:10] if self.data.get('last_check') else '從未'
        
        nav = '''<div class="nav">
            <a href="index.html">📋 所有記錄</a>
            <a href="recent.html" class="active">📅 最近6個月</a>
        </div>'''
        
        html = self._get_base_template().format(
            title='澳門政府 IT 採購監控 - 最近6個月',
            nav=nav,
            total_records=total,
            last_check=last_check,
            departments=departments,
            records=records_html,
            update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        output_path = os.path.join(self.output_dir, 'recent.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"已生成: {output_path} ({total} 條記錄)")
        return output_path
    
    def generate(self):
        """生成所有頁面"""
        print("=" * 60)
        print("生成 HTML 頁面")
        print("=" * 60)
        
        self.generate_all_records_page()
        self.generate_recent_page()
        
        print("\n頁面生成完成!")


if __name__ == '__main__':
    generator = HTMLGenerator()
    generator.generate()