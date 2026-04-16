import sqlite3
import os

# DB_PATH 預設使用 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')

def get_db_connection():
    """
    建立與 SQLite 資料庫的連線。
    預設啟用 sqlite3.Row 以便透過欄位名稱存取資料。
    """
    try:
        if not os.path.exists(INSTANCE_DIR):
            os.makedirs(INSTANCE_DIR)
            
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"資料庫連線失敗: {e}")
        raise

class Task:
    def __init__(self, id, title, status, due_date, created_at):
        self.id = id
        self.title = title
        self.status = status
        self.due_date = due_date
        self.created_at = created_at

    @staticmethod
    def create(title, due_date=None):
        """
        新增一筆任務記錄。
        參數：
            title (str): 任務標題
            due_date (str, optional): 截止日期字串
        回傳：
            int: 新紀錄的 id
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tasks (title, due_date) VALUES (?, ?)',
                (title, due_date)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except Exception as e:
            print(f"建立任務失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all(status=None):
        """
        取得所有任務記錄。
        參數：
            status (str, optional): 根據任務狀態過濾 ('pending' 或 'completed')
        回傳：
            list[sqlite3.Row]: 任務記錄清單
        """
        try:
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
            return tasks
        except Exception as e:
            print(f"取得任務列表失敗: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(task_id):
        """
        取得單筆任務記錄。
        參數：
            task_id (int): 任務 ID
        回傳：
            sqlite3.Row 或 None: 任務資料或查無資料
        """
        try:
            conn = get_db_connection()
            task = conn.execute(
                'SELECT * FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            return task
        except Exception as e:
            print(f"取得單一任務失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(task_id, title, due_date, status):
        """
        更新指定的任務記錄。
        參數：
            task_id (int): 任務 ID
            title (str): 新的任務標題
            due_date (str): 新的截止日期
            status (str): 新的任務狀態
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE tasks SET title = ?, due_date = ?, status = ? WHERE id = ?',
                (title, due_date, status, task_id)
            )
            conn.commit()
        except Exception as e:
            print(f"更新任務資料失敗: {e}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(task_id):
        """
        刪除指定的任務記錄。
        參數：
            task_id (int): 任務 ID
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
        except Exception as e:
            print(f"刪除任務失敗: {e}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def toggle_status(task_id):
        """
        切換指定任務的完成狀態 (pending ⇄ completed)。
        參數：
            task_id (int): 任務 ID
        """
        try:
            conn = get_db_connection()
            task = conn.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
            if task:
                new_status = 'completed' if task['status'] == 'pending' else 'pending'
                conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
                conn.commit()
        except Exception as e:
            print(f"切換任務狀態失敗: {e}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()
