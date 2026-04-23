# 個人記帳簿系統 - 流程圖文件

## 1. 使用者流程圖 (User Flow)

這張圖展示了使用者進入網站後，可以進行的各項操作路徑：

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁 - 收支總覽與歷史明細]
    B --> C{想要做什麼？}
    
    C -->|紀錄花費或收入| D[前往新增收支表單]
    D -->|填寫金額與分類並送出| E[儲存成功，自動返回首頁]
    
    C -->|查看花費比例| F[前往統計圖表頁面]
    F -->|檢視支出圓餅圖| F
    F -->|返回| B
    
    E --> B
```

---

## 2. 系統序列圖 (Sequence Diagram)

這張圖以「使用者新增一筆支出」為例，展示了系統內部前端（瀏覽器）與後端（Flask、SQLite）是如何溝通傳遞資料的：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Route as Flask (Controller)
    participant Model as Model (資料模型)
    participant DB as SQLite 資料庫
    
    User->>Browser: 填寫支出表單 (金額、分類) 並點擊送出
    Browser->>Route: POST /record/new (傳送表單資料)
    Route->>Model: 呼叫新增紀錄的函式
    Model->>DB: 執行 SQL (INSERT INTO records ...)
    DB-->>Model: 寫入成功
    Model-->>Route: 回傳執行結果
    Route-->>Browser: HTTP 302 重導向 (Redirect) 至首頁
    Browser->>Route: GET / (重新要求首頁)
    Route->>Model: 撈取最新餘額與明細
    Model->>DB: 執行 SQL (SELECT ...)
    DB-->>Model: 回傳資料
    Model-->>Route: 回傳 Python 物件
    Route->>Browser: 渲染最新的 HTML 頁面
    Browser->>User: 看到剛才新增的紀錄與更新後的餘額
```

---

## 3. 功能清單與路由對照表

根據上述流程，初步規劃出以下 URL 路徑與對應的操作：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :---: | :--- |
| 首頁 (總覽與明細) | `/` | GET | 顯示目前總餘額以及歷史收支明細列表。 |
| 新增收支頁面 | `/record/new` | GET | 顯示用來填寫新增收入或支出的 HTML 表單。 |
| 處理新增收支 | `/record/new` | POST | 接收表單送出的資料，存入資料庫後重導向回首頁。 |
| 查看圓餅圖 | `/chart` | GET | 顯示支出分類比例的圓餅圖畫面。 |
