import os
from flask import Flask
from app.routes.main import main_bp
from app.models.record import RecordModel

def create_app():
    """建立並設定 Flask 應用程式實例"""
    # 指定 template 與 static 的資料夾路徑，以符合架構設計
    app = Flask(__name__, 
                template_folder='app/templates', 
                static_folder='app/static')
    
    # 設定 SECRET_KEY (供 flash messages 與 session 使用)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_12345')

    # 註冊我們設計好的路由 Blueprint
    app.register_blueprint(main_bp)

    # 啟動時自動檢查並初始化資料庫
    try:
        RecordModel.init_db()
        print("資料庫初始化檢查完成。")
    except Exception as e:
        print(f"資料庫初始化發生錯誤: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    # 啟動開發伺服器
    app.run(debug=True)
