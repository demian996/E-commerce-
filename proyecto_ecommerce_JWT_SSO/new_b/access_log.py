import datetime

access_logs = []

def add_log(user_id, access_type):
    access_logs.append({
        'user_id': user_id,
        'access_type': access_type,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

def get_logs():
    return access_logs
