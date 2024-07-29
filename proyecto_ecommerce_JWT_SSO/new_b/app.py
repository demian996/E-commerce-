from flask import Flask, redirect, url_for, request, render_template
from config_access import verify_token

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from auth import auth_new_b_bp
from routes import new_b_bp  # Importar el nuevo blueprint para manejar rutas y logs de acceso

app.register_blueprint(auth_new_b_bp, url_prefix='/auth')
app.register_blueprint(new_b_bp, url_prefix='/new_b')

@app.route('/')
def index():
    token = request.args.get('token')
    if token:
        return render_template('index.html', token=token)
    return redirect(url_for('auth_new_b.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
