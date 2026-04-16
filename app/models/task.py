import sqlite3
import os

# DB_PATH 預設使用 instance/database.db (若部署於 app 目錄上一層)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')

def get_db_connection():
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    # 將回傳結果轉為 dict-like API，方便直接透過欄位名稱取值
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    def __init__(self, id, title, status, due_date, created_at):
        self.id = id
        self.title = title
        self.status = status
        self.due_date = due_date
        self.created_at = created_at

    @staticmethod
    def create(title, due_date=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, due_date) VALUES (?, ?)',
            (title, due_date)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all(status=None):
        conn = get_db_connection()
        if status:
            tasks = conn.execute(
                'SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', 
                (status,)
            ).fetchall()
        else:
            tasks = conn.execute(
                'SELECT * FROM tasks ORDER BY created_at DESC'
            ).fetchall()
        conn.close()
        
        # 可回傳 Row objects 的 list
        return tasks

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute(
            'SELECT * FROM tasks WHERE id = ?',
            (task_id,)
        ).fetchone()
        conn.close()
        return task

    @staticmethod
    def update(task_id, title, due_date, status):
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET title = ?, due_date = ?, status = ? WHERE id = ?',
            (title, due_date, status, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def toggle_status(task_id):
        conn = get_db_connection()
        task = conn.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task:
            new_status = 'completed' if task['status'] == 'pending' else 'pending'
            conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
            conn.commit()
        conn.close()
