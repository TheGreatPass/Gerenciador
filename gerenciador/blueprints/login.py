from flask import Blueprint, render_template, request, redirect, session, url_for
import bcrypt
from db import db_config
from flask_cors import CORS

auth = Blueprint('auth', __name__)
CORS(auth)
# -------------------LOGIN--------------------------------------------------------------------------------------------
@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        cargo = request.form['cargo']

        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = db_config()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, senha, cargo) VALUES (%s, %s, %s)",
                        (nome, senha_hash.decode('utf-8'), cargo))
            conn.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            return f"Erro ao cadastrar: {e}"
        finally:
            cursor.close()
            conn.close()

    return render_template('cadastro.html')
#--------------------------------------------------------------------------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conn = db_config()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
            session['usuario'] = usuario['nome']
            return f"Bem-vindo, {usuario['nome']}! Cargo: {usuario['cargo']}"
        else:
            return "Login inválido!"
    return render_template('login.html')
#--------------------------------------------------------------------------------------------------------
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
