from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # 載入基礎設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-default-secret-key')
    
    # 註冊 Blueprint
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
