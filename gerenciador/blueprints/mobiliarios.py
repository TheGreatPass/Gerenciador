from flask import Blueprint, request, jsonify
from db import buscarNoBanco, mexerNoBanco
from flask_cors import CORS

mob = Blueprint("mobiliario", __name__)
CORS(mob) 

#--------------------MOBILIARIO--------------------------------------------------------------------------------------
@mob.route("/mobiliario", methods=['GET'])
def buscarMobiliario():
    try:
        lista_de_mobiliario = buscarNoBanco("SELECT * FROM mobiliario")
        return jsonify(lista_de_mobiliario)
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao buscar mobiliario: {e}"})
#--------------------------------------------------------------------------------------------------------------------
@mob.route("/mobiliario/<int:id>", methods=['GET'])
def buscarUmMobiliario(id):
    try:
        mobiliario = buscarNoBanco(f"SELECT * FROM mobiliario WHERE id = {id}")
        return jsonify(mobiliario[0]) if mobiliario else jsonify({"mensagem": "mobiliario nao encontrado."}),404
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao buscar mobiliario: {e}"}),500
#--------------------------------------------------------------------------------------------------------------------
@mob.route("/mobiliario", methods=['POST'])
def criarMobiliario():
    try:
        informacoes = request.get_json()
        nome = informacoes.get("nome")
        imagem = informacoes.get("imagem")

        if not nome or not imagem:
            return jsonify({"mensagem": "Dados incompletos para cadastro."}), 400

        consulta = """
            INSERT INTO mobiliario (nome, imagem)
            VALUES (%s, %s)
        """
        parametros = (nome, imagem)
        mexerNoBanco(consulta, parametros)

        return jsonify({"mensagem": "Mobiliário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao cadastrar mobiliário: {e}"}), 500
#--------------------------------------------------------------------------------------------------------------------
@mob.route("/mobiliario/<int:id>", methods=["PUT"])
def atualizarMobiliario(id):
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        imagem = dados.get("imagem")

        if not nome or not imagem:
            return jsonify({"mensagem": "Dados incompletos para atualização."}), 400

        consulta = """
            UPDATE mobiliario
            SET nome = %s, imagem = %s
            WHERE id = %s
        """
        parametros = (nome, imagem, id)
        mexerNoBanco(consulta, parametros)

        return jsonify({"mensagem": "Mobiliário atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao atualizar mobiliário: {e}"}), 500
#--------------------------------------------------------------------------------------------------------------------
@mob.route("/mobiliario/<int:id>", methods=["DELETE"])
def deletarMobiliario(id):
    try:
        consulta = "DELETE FROM mobiliario WHERE id = %s"
        parametros = (id,)
        mexerNoBanco(consulta, parametros)

        return jsonify({"mensagem": "Mobiliário removido com sucesso!"}), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao remover mobiliário: {e}"}), 500
