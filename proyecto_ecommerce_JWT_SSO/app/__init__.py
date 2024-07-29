# app/__init__.py en ecommerce
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from access_log import get_logs  # Importar la función para obtener logs

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

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.categorias import categorias_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.reportes import reportes_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/access_report', methods=['GET'])
    def view_logs():
        logs = get_logs()
        return render_template('access_report.html', logs=logs)

    return app
