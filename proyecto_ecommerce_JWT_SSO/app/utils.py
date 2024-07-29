# app/utils.py
from functools import wraps
from flask import request, redirect, url_for

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return redirect(url_for('auth.login'))
        request.headers = {'Authorization': f'Bearer {token}'}
        return f(*args, **kwargs)
    return decorated_function
