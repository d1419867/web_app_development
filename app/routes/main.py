from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.record import RecordModel

# 建立 Blueprint 以模組化路由，之後會在 app.py 中註冊這個 blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁路由
    處理邏輯：取得所有收支紀錄，計算總收入、總支出與餘額。
    輸出：渲染 index.html
    """
    records = RecordModel.get_all()
    
    # 計算總收入、總支出與餘額
    total_income = sum(r['amount'] for r in records if r['type'] == 'income')
    total_expense = sum(r['amount'] for r in records if r['type'] == 'expense')
    balance = total_income - total_expense
    
    return render_template('index.html', records=records, total_income=total_income, total_expense=total_expense, balance=balance)

@main_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    顯示新增收支紀錄的表單頁面
    處理邏輯：無特殊邏輯，單純回傳頁面供使用者填寫。
    輸出：渲染 record_form.html
    """
    return render_template('record_form.html', action="new")

@main_bp.route('/records', methods=['POST'])
def create_record():
    """
    接收新增表單並儲存至資料庫
    輸入：表單資料 (type, amount, category, date, description)
    處理邏輯：驗證資料後，呼叫 RecordModel.create() 儲存，最後重導向至首頁。
    """
    record_type = request.form.get('type')
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description', '')

    # 簡易欄位驗證
    if not record_type or not amount_str or not category or not date:
        flash("請填寫所有必填欄位！", "danger")
        return redirect(url_for('main.new_record'))

    try:
        amount = float(amount_str)
    except ValueError:
        flash("金額格式不正確，必須是數字！", "danger")
        return redirect(url_for('main.new_record'))

    record_id = RecordModel.create(record_type, amount, category, date, description)
    
    if record_id:
        flash("新增紀錄成功！", "success")
    else:
        flash("新增紀錄時發生錯誤，請稍後再試。", "danger")
        
    return redirect(url_for('main.index'))

@main_bp.route('/records/<int:id>/edit', methods=['GET'])
def edit_record(id):
    """
    顯示編輯收支紀錄的表單頁面
    輸入：紀錄的 ID
    處理邏輯：利用 ID 查詢單筆紀錄，若存在則傳遞給模板。
    輸出：渲染 record_form.html，並預設填入原有資料。
    """
    record = RecordModel.get_by_id(id)
    if not record:
        flash("找不到該筆紀錄！", "danger")
        return redirect(url_for('main.index'))
        
    return render_template('record_form.html', action="edit", record=record)

@main_bp.route('/records/<int:id>/update', methods=['POST'])
def update_record(id):
    """
    接收編輯表單並更新資料庫
    輸入：紀錄的 ID 以及修改後的表單資料
    處理邏輯：驗證資料後，呼叫 RecordModel.update() 更新資料庫，然後重導向至首頁。
    """
    record_type = request.form.get('type')
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description', '')

    # 簡易欄位驗證
    if not record_type or not amount_str or not category or not date:
        flash("請填寫所有必填欄位！", "danger")
        return redirect(url_for('main.edit_record', id=id))

    try:
        amount = float(amount_str)
    except ValueError:
        flash("金額格式不正確，必須是數字！", "danger")
        return redirect(url_for('main.edit_record', id=id))

    success = RecordModel.update(id, record_type, amount, category, date, description)
    
    if success:
        flash("紀錄更新成功！", "success")
    else:
        flash("更新失敗或資料沒有任何變動。", "warning")
        
    return redirect(url_for('main.index'))

@main_bp.route('/records/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    刪除指定的收支紀錄
    輸入：紀錄的 ID
    處理邏輯：呼叫 RecordModel.delete(id) 刪除該紀錄，然後重導向至首頁。
    """
    success = RecordModel.delete(id)
    if success:
        flash("紀錄已成功刪除！", "success")
    else:
        flash("刪除失敗，找不到該筆紀錄。", "danger")
        
    return redirect(url_for('main.index'))

@main_bp.route('/chart')
def chart():
    """
    顯示支出分類統計圓餅圖
    處理邏輯：取得所有紀錄並依照分類統計各項目總額，整理好後傳遞給模板使用。
    輸出：渲染 chart.html
    """
    records = RecordModel.get_all()
    
    # 我們通常比較關心「支出」的去向，所以只撈出支出的紀錄來計算分類
    expense_records = [r for r in records if r['type'] == 'expense']
    
    # 計算每個分類的總額
    category_totals = {}
    for r in expense_records:
        cat = r['category']
        category_totals[cat] = category_totals.get(cat, 0) + r['amount']
        
    return render_template('chart.html', category_totals=category_totals)
