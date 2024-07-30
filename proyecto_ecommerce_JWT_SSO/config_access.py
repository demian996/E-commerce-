import jwt
import datetime
from invalid_tokens import add_invalid_token, is_token_invalid

SECRET_KEY = 'your_jwt_secret_key'

def create_access_token(identity):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
        'iat': datetime.datetime.utcnow(),
        'sub': {
            'user_id': identity['user_id'],
            'user_role': identity['user_role']
        }
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def generate_token(identity):
    return create_access_token(identity)

def verify_token(token):
    try:
        if is_token_invalid(token):
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return {
            'user_id': payload['sub']['user_id'],
            'user_role': payload['sub']['user_role']
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
