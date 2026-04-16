from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.task import Task

# 定義 Blueprint
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/')
def index():
    """
    任務列表首頁
    GET /
    取得所有任務清單 (可透過 ?status= 進行過濾)，並渲染 index.html 畫面
    """
    status_filter = request.args.get('status')
    
    # 確保 status 的選項合規
    if status_filter not in ['completed', 'pending']:
        status_filter = None

    tasks = Task.get_all(status=status_filter)
    
    # 渲染模板，雖然還沒有模板檔案，但先寫好對應
    return render_template('index.html', tasks=tasks, current_status=status_filter)

@task_bp.route('/tasks/create', methods=['POST'])
def create_task():
    """
    建立新任務
    POST /tasks/create
    接收表單的 title 與 due_date，存入資料庫後重導回首頁
    """
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip()
    
    if not title:
        flash('任務名稱為必填欄位', 'error')
        return redirect(url_for('tasks.index'))
    
    # 如果有輸入但為空字串，我們視為未設定期限
    if not due_date:
        due_date = None
        
    task_id = Task.create(title=title, due_date=due_date)
    if task_id:
        flash('任務建立成功', 'success')
    else:
        flash('建立任務失敗，請稍後再試', 'error')
        
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    編輯任務頁面
    GET /tasks/<id>/edit
    取得單筆任務資料，若存在則渲染 edit.html 顯示編輯表單；否則回傳 404
    """
    task = Task.get_by_id(id)
    if not task:
        abort(404, description="找不到該任務")
        
    return render_template('edit.html', task=task)

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    更新任務
    POST /tasks/<id>/update
    接收修改表單資料 (title, due_date, status) 並更新該筆錄，完成後重導回首頁
    """
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip()
    status = request.form.get('status')
    
    if not title:
        flash('修改失敗：任務名稱不得為空', 'error')
        return redirect(url_for('tasks.edit_task', id=id))

    if not due_date:
        due_date = None
        
    if status not in ['pending', 'completed']:
        status = 'pending'

    Task.update(task_id=id, title=title, due_date=due_date, status=status)
    flash('任務更新成功', 'success')
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task_status(id):
    """
    切換任務完成狀態
    POST /tasks/<id>/toggle
    將指定任務在 pending/completed 之間切換，完成後重導回首頁
    """
    Task.toggle_status(id)
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除單一任務
    POST /tasks/<id>/delete
    移除指定任務，完成後重導回首頁
    """
    Task.delete(id)
    flash('任務已刪除', 'success')
    return redirect(url_for('tasks.index'))
