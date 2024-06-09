import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Defina uma chave secreta para as sessões

# Diretórios de templates e estáticos
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'estoque-app', 'templates')
static_dir = os.path.join(base_dir, 'estoque-app', 'static')
assets_dir = os.path.join(base_dir, 'estoque-app', 'assets')
app.template_folder = template_dir
app.static_folder = static_dir

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT full_name FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user:
        first_name = user['full_name'].split()[0]
        session['first_name'] = first_name
    else:
        flash('Usuário não encontrado. Por favor, faça login novamente.')
        return redirect(url_for('login'))

    return render_template('index.html', first_name=first_name)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form['email']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, full_name, email) VALUES (?, ?, ?, ?)', 
                         (username, hashed_password, full_name, email))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username or email already exists.')
            return redirect(url_for('register'))
        conn.close()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']

            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and/or password.')

    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return render_template('admin_dashboard.html', users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        is_admin = int(request.form.get('is_admin', 0))
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') if password else user['password']

        conn.execute('UPDATE users SET full_name = ?, email = ?, password = ?, is_admin = ? WHERE id = ?',
                     (full_name, email, hashed_password, is_admin, user_id))
        conn.commit()
        conn.close()

        flash('User updated successfully.')
        return redirect(url_for('admin_dashboard'))

    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    flash('User deleted successfully.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_manage_estoque/<int:user_id>')
def admin_manage_estoque(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    items = conn.execute('SELECT * FROM estoque WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return render_template('admin_manage_estoque.html', items=items, user_id=user_id)

@app.route('/admin_edit_item/<int:id>', methods=['GET', 'POST'])
def admin_edit_item(id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    item = conn.execute('SELECT * FROM estoque WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        tipo = request.form['tipo']
        tamanho = request.form['tamanho']
        genero = request.form['genero']
        quantidade = request.form['quantidade']

        conn.execute('UPDATE estoque SET tipo = ?, tamanho = ?, genero = ?, quantidade = ? WHERE id = ?',
                     (tipo, tamanho, genero, quantidade, id))
        conn.commit()
        conn.close()

        flash('Item atualizado com sucesso.')
        return redirect(url_for('admin_manage_estoque', user_id=item['user_id']))

    conn.close()
    return render_template('admin_edit_item.html', item=item)

@app.route('/admin_remove_item/<int:id>', methods=['POST'])
def admin_remove_item(id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    item = conn.execute('SELECT * FROM estoque WHERE id = ?', (id,)).fetchone()
    user_id = item['user_id']
    conn.execute('DELETE FROM estoque WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Item removido com sucesso.')
    return redirect(url_for('admin_manage_estoque', user_id=user_id))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') if password else user['password']

        conn.execute('UPDATE users SET full_name = ?, email = ?, password = ? WHERE id = ?',
                     (full_name, email, hashed_password, user_id))
        conn.commit()
        conn.close()

        flash('Profile updated successfully.')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_profile.html', user=user)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            reset_token = generate_password_hash(email + os.urandom(24).hex(), method='pbkdf2:sha256')
            conn.execute('UPDATE users SET reset_token = ? WHERE email = ?', (reset_token, email))
            conn.commit()
            send_recovery_email(user['email'], reset_token)
            flash('A recovery email has been sent to your email address.')
            return redirect(url_for('login'))
        else:
            flash('Email not found.')
        conn.close()

    return render_template('forgot_password.html')


def send_recovery_email(email, token):
    sender_email = "your-email@gmail.com"
    sender_password = "your-email-password"
    subject = "Password Recovery"
    recovery_url = url_for('reset_password', token=token, _external=True)
    body = f"Click the link to reset your password: {recovery_url}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

        conn = get_db_connection()
        # Você precisa obter o email do usuário correspondente ao token
        email = conn.execute('SELECT email FROM users WHERE reset_token = ?', (token,)).fetchone()

        if email:
            conn.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email['email']))
            conn.commit()
            conn.close()
            flash('Password has been reset. Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired token.')
            return redirect(url_for('forgot_password'))

    return render_template('reset_password.html', token=token)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/novo_estoque', methods=['GET', 'POST'])
def novo_estoque():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    first_name = session.get('first_name', 'Usuário')

    if request.method == 'POST':
        tipo = request.form['tipo']
        tamanho = request.form['tamanho']
        genero = request.form['genero']
        quantidade = request.form['quantidade']
        user_id = session['user_id']

        conn = get_db_connection()
        conn.execute('INSERT INTO estoque (tipo, tamanho, genero, quantidade, user_id) VALUES (?, ?, ?, ?, ?)',
                     (tipo, tamanho, genero, quantidade, user_id))
        conn.commit()
        conn.close()
        mensagem = "Item adicionado com sucesso!"
        return render_template('novo_estoque.html', mensagem=mensagem)

    return render_template('novo_estoque.html', first_name=first_name)

@app.route('/gerenciar_estoque')
def gerenciar_estoque():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    first_name = session.get('first_name', 'Usuário')

    user_id = session['user_id']
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM estoque WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return render_template('gerenciar_estoque.html', items=items, first_name=first_name)

@app.route('/ajuda')
def ajuda():
    first_name = session.get('first_name', 'Usuário')
    return render_template('ajuda.html', first_name=first_name)

@app.route('/quem_somos')
def quem_somos():
    first_name = session.get('first_name', 'Usuário')
    return render_template('quem_somos.html', first_name=first_name)

@app.route('/remove_item/<int:id>', methods=['POST'])
def remove_item(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM estoque WHERE id = ? AND user_id = ?', (id, user_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/edit_item/<int:id>', methods=['POST'])
def edit_item(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    tipo = data['tipo']
    tamanho = data['tamanho']
    genero = data['genero']
    quantidade = data['quantidade']
    user_id = session['user_id']

    conn = get_db_connection()
    conn.execute('UPDATE estoque SET tipo = ?, tamanho = ?, genero = ?, quantidade = ? WHERE id = ? AND user_id = ?',
                 (tipo, tamanho, genero, quantidade, id, user_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/assets/images/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(assets_dir, 'images'), filename)


if __name__ == '__main__':
    app.run(debug=True)
