from flask import Flask
#앱 서버 인스턴스
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suff.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .models import FreightInfo, Bill
    with app.app_context():
        db.create_all()

    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)
        
    return app
#라우팅 - 데코레이터