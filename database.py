import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')

def init_db():
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
