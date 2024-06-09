import sqlite3
from werkzeug.security import generate_password_hash

# Conecte-se ao banco de dados
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

# Dados do administrador
username = 'adminRichard1'
password = '9243'  # Escolha uma senha segura
full_name = 'Admin User'
email = 'richard1@gmail.com'
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
is_admin = 1  # Definindo este usuário como administrador

# Inserir o administrador no banco de dados
cursor.execute('INSERT INTO users (username, password, full_name, email, is_admin) VALUES (?, ?, ?, ?, ?)', 
               (username, hashed_password, full_name, email, is_admin))

# Salvar as alterações e fechar a conexão
connection.commit()
connection.close()

print('Administrador adicionado com sucesso!')
