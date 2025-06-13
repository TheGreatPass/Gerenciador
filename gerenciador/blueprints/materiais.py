from flask import Blueprint, request, jsonify
from db import buscarNoBanco, mexerNoBanco
from flask_cors import CORS

mat = Blueprint("materiais", __name__)
CORS(mat) 

# -------------------MATERIAIS--------------------------------------------------------------------------------------------
@mat.route("/materiais", methods=['GET'])
def buscarMateriais():
    try:
        consulta = """
        SELECT 
            m.nome AS nome_material,
            m.imagem,
            m.id,
            GROUP_CONCAT(e.espessura_mm ORDER BY e.espessura_mm SEPARATOR ', ') AS espessuras
        FROM materiais m
        JOIN espessuras_materiais e ON m.id = e.material_id
        GROUP BY m.id, m.nome, m.imagem
        ORDER BY m.nome;
        """
        lista_de_materiais = buscarNoBanco(consulta)
        return jsonify(lista_de_materiais)
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao buscar materiais: {e}"})
#-------------------------------------------------------------------------------------------------------------------
@mat.route("/materiais/<int:id>", methods=['GET'])
def buscarMateriaisId(id):
    try:
        consulta = """
        SELECT 
            m.id,
            m.nome AS nome_material,
            m.imagem,
            GROUP_CONCAT(e.espessura_mm ORDER BY e.espessura_mm SEPARATOR ', ') AS espessuras
        FROM materiais m
        JOIN espessuras_materiais e ON m.id = e.material_id
        WHERE m.id = %s
        GROUP BY m.id, m.nome, m.imagem;
        """
        resultado = buscarNoBanco(consulta, (id,))
        if resultado:
            return jsonify(resultado[0])
        else:
            return jsonify({"mensagem": "Material nao encontrado"}), 404
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao buscar material: {e}"}), 500
#--------------------------------------------------------------------------------------------------------------------
@mat.route("/materiais/<int:id>", methods=['PUT'])
def atualizar_material(id):
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        imagem = dados.get("imagem")
        espessuras = dados.get("espessuras", [])

        if not nome or not isinstance(espessuras, list):
            return jsonify({"mensagem": "Dados inválidos"}), 400

        consulta_material = "UPDATE materiais SET nome = %s, imagem = %s WHERE id = %s"
        mexerNoBanco(consulta_material, (nome, imagem, id))

        remover_espessuras = "DELETE FROM espessuras_materiais WHERE material_id = %s"
        mexerNoBanco(remover_espessuras, (id,))

        for esp in espessuras:
            if esp in [15, 18, 25, 50]:
                inserir_espessura = "INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES (%s, %s)"
                mexerNoBanco(inserir_espessura, (id, esp))

        return jsonify({"mensagem": "Material atualizado com sucesso"})

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao atualizar material: {e}"}), 500
#--------------------------------------------------------------------------------------------------------------
@mat.route("/materiais", methods=['POST'])
def criar_material():
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        imagem = dados.get("imagem")
        espessuras = dados.get("espessuras", [])

        if not nome or not isinstance(espessuras, list):
            return jsonify({"mensagem": "Dados inválidos"}), 400

        consulta_inserir_material = "INSERT INTO materiais (nome, imagem) VALUES (%s, %s)"
        novo_id = mexerNoBanco(consulta_inserir_material, (nome, imagem), retornar_id=True)

        for esp in espessuras:
            if esp in [15, 18, 25, 50]:
                inserir_espessura = "INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES (%s, %s)"
                mexerNoBanco(inserir_espessura, (novo_id, esp))

        return jsonify({"mensagem": "Material criado com sucesso", "id": novo_id}), 201

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao criar material: {e}"}), 500
#-------------------------------------------------------------------------------------------------------------------
@mat.route("/materiais/<int:id>", methods=['DELETE'])
def deletar_material(id):
    try:
        consulta = "DELETE FROM materiais WHERE id = %s"
        resultado = mexerNoBanco(consulta, (id,))
        return jsonify({"mensagem": f"Material com ID {id} deletado com sucesso!"})
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao deletar material: {e}"}), 500
