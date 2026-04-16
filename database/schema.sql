-- 任務管理系統：SQLite 初始建表腳本

-- 若要重新建表可考慮取消註解下一行
-- DROP TABLE IF EXISTS tasks;

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- 狀態: pending, completed
    due_date TEXT,                          -- 格式: YYYY-MM-DD
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
