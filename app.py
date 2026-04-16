from flask import Flask
import os

def create_app():
    # 由於 app.py 位在根目錄，需手動指定 template 與 static 指向 app 資料夾內
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 載入基礎設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-default-secret-key')
    
    # 註冊 Blueprint
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
