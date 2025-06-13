from flask import Blueprint, request, jsonify
from db import buscarNoBanco, mexerNoBanco
from flask_cors import CORS
import bcrypt
import mysql.connector
user = Blueprint("usuarios", __name__)
CORS(user) 

#--------------------USUARIO--------------------------------------------------------------------------------------
@user.route('/usuarios', methods=['GET'])
def listar_usuarios():
    consulta = """
        SELECT u.id, u.nome, c.nome AS cargo
        FROM usuarios u
        JOIN cargos c ON u.cargo_id = c.id
    """
    usuarios = buscarNoBanco(consulta)
    return jsonify(usuarios)
#----------------------------------------------------------------------------------------------------------
@user.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    consulta = """
        SELECT u.id, u.nome, c.nome AS cargo
        FROM usuarios u
        JOIN cargos c ON u.cargo_id = c.id
        WHERE u.id = %s
    """
    resultado = buscarNoBanco(consulta, (usuario_id,))
    if resultado:
        return jsonify(resultado[0])
    return jsonify({'erro': 'Usuário não encontrado'}), 404
#----------------------------------------------------------------------------------------------------------
@user.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')
    cargo_id = dados.get('cargo_id')

    if not all([nome, senha, cargo_id]):
        return jsonify({'erro': 'Dados incompletos'}), 400

    try:
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        consulta = "INSERT INTO usuarios (nome, senha, cargo_id) VALUES (%s, %s, %s)"
        mexerNoBanco(consulta, (nome, senha_hash, cargo_id))
        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

    except mysql.connector.errors.IntegrityError as e:
        if "1062" in str(e):
            return jsonify({'erro': 'Nome de usuário já existe'}), 400
#--------------------------------------------------------------------------------------------------------------
@user.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')
    cargo_id = dados.get('cargo_id')

    if not all([nome, senha, cargo_id]):
        return jsonify({'erro': 'Dados incompletos'}), 400

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    consulta = """
        UPDATE usuarios
        SET nome = %s, senha = %s, cargo_id = %s
        WHERE id = %s
    """
    mexerNoBanco(consulta, (nome, senha_hash, cargo_id, usuario_id))
    return jsonify({'mensagem': 'Usuário atualizado com sucesso'})
#------------------------------------------------------------------------------------------------------------
@user.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    consulta = "DELETE FROM usuarios WHERE id = %s"
    mexerNoBanco(consulta, (usuario_id,))
    return jsonify({'mensagem': 'Usuário deletado com sucesso'})
