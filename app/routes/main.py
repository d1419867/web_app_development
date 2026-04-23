from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.record import RecordModel

# 建立 Blueprint 以模組化路由，之後會在 app.py 中註冊這個 blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁路由
    處理邏輯：取得所有收支紀錄，計算總收入、總支出與餘額。
    輸出：渲染 index.html
    """
    pass

@main_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    顯示新增收支紀錄的表單頁面
    處理邏輯：無特殊邏輯，單純回傳頁面供使用者填寫。
    輸出：渲染 record_form.html
    """
    pass

@main_bp.route('/records', methods=['POST'])
def create_record():
    """
    接收新增表單並儲存至資料庫
    輸入：表單資料 (type, amount, category, date, description)
    處理邏輯：驗證資料後，呼叫 RecordModel.create() 儲存，最後重導向至首頁。
    """
    pass

@main_bp.route('/records/<int:id>/edit', methods=['GET'])
def edit_record(id):
    """
    顯示編輯收支紀錄的表單頁面
    輸入：紀錄的 ID
    處理邏輯：利用 ID 查詢單筆紀錄，若存在則傳遞給模板。
    輸出：渲染 record_form.html，並預設填入原有資料。
    """
    pass

@main_bp.route('/records/<int:id>/update', methods=['POST'])
def update_record(id):
    """
    接收編輯表單並更新資料庫
    輸入：紀錄的 ID 以及修改後的表單資料
    處理邏輯：驗證資料後，呼叫 RecordModel.update() 更新資料庫，然後重導向至首頁。
    """
    pass

@main_bp.route('/records/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    刪除指定的收支紀錄
    輸入：紀錄的 ID
    處理邏輯：呼叫 RecordModel.delete(id) 刪除該紀錄，然後重導向至首頁。
    """
    pass

@main_bp.route('/chart')
def chart():
    """
    顯示支出分類統計圓餅圖
    處理邏輯：取得所有紀錄並依照分類統計各項目總額，整理好後傳遞給模板使用。
    輸出：渲染 chart.html
    """
    pass
