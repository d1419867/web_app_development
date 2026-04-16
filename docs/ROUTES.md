# API 路由與模板設計 (Routes & Templates)

本文件依據 PRD 與資料庫設計 (DB_DESIGN)，定義任務管理系統的前後端互動介面。為符合單純的 SSR (伺服器端渲染) 架構，所有涉及資料變更的請求都會透過 `POST` 操作，並在結束後利用 HTTP 302 重導向回列表頁面。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **任務列表** | `GET` | `/` | `index.html` | 顯示所有任務，可帶入 `?status=` 進行過濾 |
| **建立任務** | `POST` | `/tasks/create` | — | 接收新增表單，存入 DB，完成後重導向至首頁 |
| **編輯任務頁面** | `GET` | `/tasks/<id>/edit` | `edit.html` | 顯示針對特定任務的編輯表單頁面 |
| **更新任務** | `POST` | `/tasks/<id>/update` | — | 接收編輯表單，更新 DB，完成後重導向至首頁 |
| **標記任務狀態** | `POST` | `/tasks/<id>/toggle` | — | 翻轉狀態 (pending ⇄ completed)，完成後重導向至首頁 |
| **刪除任務** | `POST` | `/tasks/<id>/delete` | — | 刪除指定任務，完成後重導向至首頁 |

---

## 2. 路由詳細說明

### 2.1 任務列表 `/`
- **輸入**: 
  - URL Query Parameter: `status` (選項: `completed`, `pending`，非必填)
- **處理邏輯**: 
  - 呼叫 `Task.get_all(status)`。
- **輸出**: 
  - 渲染 `index.html`，並將取得的任務清單 `tasks` 傳入。

### 2.2 建立任務 `/tasks/create`
- **輸入**: 
  - Form Data: `title` (文字，必填), `due_date` (日期字串，非必填)
- **處理邏輯**: 
  - 驗證 `title` 是否有值。呼叫 `Task.create(title, due_date)` 新增進資料庫。
- **輸出**: 
  - Http 302 Redirect，重導向至 `/`。

### 2.3 編輯任務頁面 `/tasks/<id>/edit`
- **輸入**: 
  - URL Path Parameter: `id` (任務唯一識別碼)
- **處理邏輯**: 
  - 呼叫 `Task.get_by_id(id)`，若找不到該任務則回傳 404 Not Found。
- **輸出**: 
  - 渲染 `edit.html`，並將取得的任務資料 `task` 傳入。

### 2.4 更新任務 `/tasks/<id>/update`
- **輸入**: 
  - URL Path Parameter: `id` (任務唯一識別碼)
  - Form Data: `title` (文字，必填), `due_date` (日期字串，非必填), `status` (狀態字串，必填)
- **處理邏輯**: 
  - 檢查資料格式。呼叫 `Task.update(id, title, due_date, status)`。
- **輸出**: 
  - Http 302 Redirect，重導向至 `/`。

### 2.5 標記任務狀態 `/tasks/<id>/toggle`
- **輸入**: 
  - URL Path Parameter: `id` (任務唯一識別碼)
- **處理邏輯**: 
  - 呼叫 `Task.toggle_status(id)` 來反轉目前該任務的狀態。
- **輸出**: 
  - Http 302 Redirect，重導向至 `/`。

### 2.6 刪除任務 `/tasks/<id>/delete`
- **輸入**: 
  - URL Path Parameter: `id` (任務唯一識別碼)
- **處理邏輯**: 
  - 呼叫 `Task.delete(id)` 從資料庫移除該任務。
- **輸出**: 
  - Http 302 Redirect，重導向至 `/`。

---

## 3. Jinja2 模板清單

所有的模板將集中放置於 `app/templates/` 資料夾內。

- **`base.html`**
  - **說明**: 共用的 HTML 骨架基底檔案。包含共同的 Header、Footer 以及掛載 `/static/css/style.css`。
  - **用途**: 其他模板皆透過 `{% extends 'base.html' %}` 繼承。
- **`index.html`**
  - **說明**: 任務清單主畫面。
  - **繼承**: 繼承自 `base.html`。
  - **包含區塊**: 
    - 頂部的新增任務表單 (`<form action="/tasks/create" method="POST">`)
    - 過濾區域的按鈕連結
    - 透過迴圈 (`{% for task in tasks %}`) 產生的單筆任務清單項目，包含刪除、狀態切換的按鈕及編輯連結。
- **`edit.html`**
  - **說明**: 編輯單一任務的獨立頁面。
  - **繼承**: 繼承自 `base.html`。
  - **包含區塊**:
    - 一個 `<form action="/tasks/<id>/update" method="POST">`，表單內預設填好該任務原有的 `title`, `due_date`, 及 `status`。
    - 一個可放棄修改，返回首頁的「取消」連結。
