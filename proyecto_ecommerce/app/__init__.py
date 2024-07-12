from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    app.config['SQLALCHEMY_BINDS'] = {
        'mysql': 'mysql+pymysql://root:root@db_mysql/ecommerce',
        'postgres': 'postgresql+psycopg2://postgres:root@db_postgres/ecommerce'
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.categorias import categorias_bp
    from .routes.pedidos import pedidos_bp
    from .routes.reportes import reportes_bp
    from .routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    app.register_blueprint(admin_bp)

    return app
