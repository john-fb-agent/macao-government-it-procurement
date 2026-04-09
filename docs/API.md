# 網站結構分析

## 目標網站

**URL**: https://www.bo.dsaj.gov.mo/cn/news/list/b/?d=13

## 網頁結構

### 公告列表

每條公告包含以下資訊：

```html
<div class="news-item">
  <div class="news-title">
    <a href="/cn/news/detail/xxx">【部門名稱】採購摘要內容</a>
  </div>
  <div class="news-meta">
    <span class="bulletin">《公報》第 XX 期</span>
    <span class="date">YYYY-MM-DD</span>
  </div>
</div>
```

### 欄位對應

| 欄位 | 選擇器 | 說明 |
|------|--------|------|
| 部門 | 標題中 `【】` 內的文字 | 發佈部門名稱 |
| 摘要 | 標題中 `【】` 後的文字 | 採購內容摘要 |
| 公報編號 | `.bulletin` | 《公報》期數 |
| 日期 | `.date` | 發佈日期 |
| 連結 | `a[href]` | 詳情頁面 URL |

## HTTP 請求

### 請求方法

```
GET /cn/news/list/b/?d=13 HTTP/1.1
Host: www.bo.dsaj.gov.mo
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html
```

### 回應

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
```

## 數據提取流程

1. 發送 GET 請求到目標 URL
2. 使用 BeautifulSoup 解析 HTML
3. 查找所有公告項目
4. 提取每個項目的欄位
5. 過濾 IT 相關公告

## 注意事項

- 網站使用 UTF-8 編碼
- 需要設置適當的 User-Agent
- 建議添加請求間隔，避免過度請求
