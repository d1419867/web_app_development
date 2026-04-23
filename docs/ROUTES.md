# 路由與頁面設計文件 (Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (收支總覽與列表) | GET | `/` | `index.html` | 顯示餘額、總收入/支出、以及所有歷史明細 |
| 新增紀錄頁面 | GET | `/records/new` | `record_form.html` | 顯示新增收支的 HTML 表單 |
| 建立紀錄 | POST | `/records` | — | 接收新增表單，存入資料庫，完成後重導向至首頁 |
| 編輯紀錄頁面 | GET | `/records/<int:id>/edit` | `record_form.html` | 顯示編輯特定收支的表單（自動帶入舊有資料） |
| 更新紀錄 | POST | `/records/<int:id>/update` | — | 接收編輯表單，更新資料庫，完成後重導向至首頁 |
| 刪除紀錄 | POST | `/records/<int:id>/delete` | — | 刪除特定收支紀錄，完成後重導向至首頁 |
| 查看圓餅圖 | GET | `/chart` | `chart.html` | 顯示支出/收入的分類比例統計圖表 |

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **處理邏輯**：呼叫 `RecordModel.get_all()` 撈取所有紀錄。計算全部紀錄的「總收入」、「總支出」並算出「當前餘額」。
- **輸出**：渲染 `index.html`，並把資料（`records`, `total_income`, `total_expense`, `balance`）傳遞給 Jinja2。

### `GET /records/new` (新增頁面)
- **處理邏輯**：無需特殊邏輯。
- **輸出**：渲染 `record_form.html`。

### `POST /records` (建立紀錄)
- **輸入**：表單內的 `type`, `amount`, `category`, `date`, `description` 欄位值。
- **處理邏輯**：檢查必填欄位。若驗證成功，呼叫 `RecordModel.create()` 寫入資料庫。
- **輸出**：成功後 HTTP 302 重導向回 `/`（首頁）。

### `GET /records/<id>/edit` (編輯頁面)
- **輸入**：URL 中的 `id` 參數。
- **處理邏輯**：呼叫 `RecordModel.get_by_id(id)` 取得這筆紀錄的詳細資料。
- **輸出**：渲染 `record_form.html`，將取得的舊資料填入 `<input>` 的 `value` 中供修改。若找不到該筆資料，則回傳 404 錯誤或回首頁。

### `POST /records/<id>/update` (更新紀錄)
- **輸入**：URL 中的 `id` 以及表單內的新值。
- **處理邏輯**：檢查必填欄位。若成功，呼叫 `RecordModel.update()` 覆寫資料庫。
- **輸出**：成功後重導向回 `/`（首頁）。

### `POST /records/<id>/delete` (刪除紀錄)
- **輸入**：URL 中的 `id`。
- **處理邏輯**：呼叫 `RecordModel.delete(id)` 進行刪除。
- **輸出**：成功後重導向回 `/`（首頁）。

### `GET /chart` (圖表頁面)
- **處理邏輯**：呼叫 `RecordModel.get_all()` 取得所有紀錄，並根據 `category`（分類）分組加總金額。
- **輸出**：渲染 `chart.html`，傳遞分組加總後的資料給前端（以便讓 Chart.js 畫出圓餅圖）。

## 3. Jinja2 模板清單

我們將會在 `app/templates/` 建立以下檔案：

| 檔案名稱 | 繼承關係 | 說明 |
| :--- | :--- | :--- |
| `base.html` | (無) | 全站共用的佈景主題母版（包含 Navbar、引入 Bootstrap / Tailwind 樣式表）。 |
| `index.html` | 繼承 `base.html` | 首頁總覽，畫面包含上方的餘額區塊與下方的歷史明細表格。 |
| `record_form.html` | 繼承 `base.html` | 共用的表單頁。透過傳入的變數判斷目前是「新增」還是「編輯」模式。 |
| `chart.html` | 繼承 `base.html` | 包含用來繪製圓餅圖的 HTML Canvas 元素。 |

## 4. 路由骨架程式碼

路由的 Python 骨架已建立在 `app/routes/main.py` 中。
