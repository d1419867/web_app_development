from flask import Blueprint, render_template, request, redirect, url_for
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
    pass

@task_bp.route('/tasks/create', methods=['POST'])
def create_task():
    """
    建立新任務
    POST /tasks/create
    接收表單的 title 與 due_date，存入資料庫後重導回首頁
    """
    pass

@task_bp.route('/tasks/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    編輯任務頁面
    GET /tasks/<id>/edit
    取得單筆任務資料，若存在則渲染 edit.html 顯示編輯表單；否則回傳 404
    """
    pass

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    更新任務
    POST /tasks/<id>/update
    接收修改表單資料 (title, due_date, status) 並更新該筆錄，完成後重導回首頁
    """
    pass

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task_status(id):
    """
    切換任務完成狀態
    POST /tasks/<id>/toggle
    將指定任務在 pending/completed 之間切換，完成後重導回首頁
    """
    pass

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除單一任務
    POST /tasks/<id>/delete
    移除指定任務，完成後重導回首頁
    """
    pass
