import sqlite3
import datetime
from pathlib import Path

# 根據架構設計，資料庫存放在 instance/database.db
# 計算專案根目錄 (BASE_DIR) 以動態取得正確路徑
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "instance" / "database.db"

def get_db_connection():
    """建立並回傳 SQLite 資料庫連線"""
    # 確保 instance 資料夾存在，避免找不到目錄的錯誤
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 將 row_factory 設為 sqlite3.Row，讓回傳的資料可以用 dict 的方式存取欄位 (例如 row['amount'])
    conn.row_factory = sqlite3.Row
    return conn

class RecordModel:
    @staticmethod
    def init_db():
        """初始化資料庫：讀取 schema.sql 並建立資料表"""
        schema_path = BASE_DIR / "database" / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            conn = get_db_connection()
            conn.executescript(schema_sql)
            conn.commit()
            conn.close()

    @staticmethod
    def create(record_type, amount, category, date, description=""):
        """新增一筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        now_iso = datetime.datetime.now().isoformat()
        
        cursor.execute(
            """
            INSERT INTO records (type, amount, category, date, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (record_type, amount, category, date, description, now_iso)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def get_all():
        """取得所有收支紀錄（依據日期從新到舊排序）"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records ORDER BY date DESC, created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(record_id, record_type, amount, category, date, description=""):
        """更新特定 ID 的收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE records 
            SET type = ?, amount = ?, category = ?, date = ?, description = ?
            WHERE id = ?
            """,
            (record_type, amount, category, date, description, record_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    @staticmethod
    def delete(record_id):
        """刪除特定 ID 的收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
