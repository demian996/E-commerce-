from werkzeug.security import generate_password_hash

# Genera el nuevo hash de la contraseña
new_password_hash = generate_password_hash('hash', method='pbkdf2:sha256')
print(new_password_hash)
