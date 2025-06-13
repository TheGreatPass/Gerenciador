from flask import Blueprint, request, jsonify
from db import buscarNoBanco, mexerNoBanco
from flask_cors import CORS

proj = Blueprint('projetos', __name__)
CORS(proj)

def get_usuario_logado():
    return 1  # Substitua por lógica real de autenticação

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos', methods=['GET'])
def listar_projetos():
    try:
        projetos = buscarNoBanco("""
            SELECT p.*, u.nome AS nome_criador
            FROM projetos p
            JOIN usuarios u ON p.usuario_criador_id = u.id
        """)

        for projeto in projetos:
            projeto_id = projeto['id']

            projeto['equipe'] = buscarNoBanco("""
                SELECT e.usuario_id, u.nome, e.cargo
                FROM equipe_projeto e
                JOIN usuarios u ON u.id = e.usuario_id
                WHERE e.projeto_id = %s
            """, (projeto_id,))

            ambientes = buscarNoBanco("""
                SELECT a.*, u.nome AS tecnico_nome
                FROM ambientes_projeto a
                LEFT JOIN usuarios u ON u.id = a.tecnico_responsavel_id
                WHERE a.projeto_id = %s
            """, (projeto_id,))

            for ambiente in ambientes:
                ambiente_id = ambiente['id']

                ambiente['materiais'] = buscarNoBanco("""
                    SELECT m.*, am.espessura_mm
                    FROM ambientes_materiais am
                    JOIN materiais m ON am.material_id = m.id
                    WHERE am.ambiente_id = %s
                """, (ambiente_id,))

                ambiente['mobiliarios'] = buscarNoBanco("""
                    SELECT mob.*, am.quantidade
                    FROM ambientes_mobiliario am
                    JOIN mobiliario mob ON am.mobiliario_id = mob.id
                    WHERE am.ambiente_id = %s
                """, (ambiente_id,))

            projeto['ambientes'] = ambientes

        return jsonify(projetos)
    
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao listar projetos: {e}"}), 500

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos/<int:id>', methods=['GET'])



def obter_projeto(id):
    projeto = buscarNoBanco("SELECT * FROM projetos WHERE id = %s", (id,))
    if projeto:
        projeto = projeto[0]
    else:
        return jsonify({"mensagem": "Projeto não encontrado"}), 404
    try:
        resultado = buscarNoBanco("""
        SELECT p.*, u.nome AS nome_criador
        FROM projetos p
        JOIN usuarios u ON p.usuario_criador_id = u.id
        WHERE p.id = %s
""", (id,))

        if resultado:
            projeto = resultado[0]
        else:
            return jsonify({"mensagem": "Projeto não encontrado"}), 404
            if not projeto:
                return jsonify({"mensagem": "Projeto não encontrado"}), 404

        projeto['equipe'] = buscarNoBanco("""
            SELECT e.usuario_id, u.nome, e.cargo
            FROM equipe_projeto e
            JOIN usuarios u ON u.id = e.usuario_id
            WHERE e.projeto_id = %s
        """, (id,))

        ambientes = buscarNoBanco("""
            SELECT a.*, u.nome AS tecnico_nome
            FROM ambientes_projeto a
            LEFT JOIN usuarios u ON u.id = a.tecnico_responsavel_id
            WHERE a.projeto_id = %s
        """, (id,))

        for ambiente in ambientes:
            ambiente_id = ambiente['id']

            ambiente['materiais'] = buscarNoBanco("""
                SELECT m.*, am.espessura_mm
                FROM ambientes_materiais am
                JOIN materiais m ON am.material_id = m.id
                WHERE am.ambiente_id = %s
            """, (ambiente_id,))

            ambiente['mobiliarios'] = buscarNoBanco("""
                SELECT mob.*, am.quantidade
                FROM ambientes_mobiliario am
                JOIN mobiliario mob ON am.mobiliario_id = mob.id
                WHERE am.ambiente_id = %s
            """, (ambiente_id,))

        projeto['ambientes'] = ambientes

        return jsonify(projeto)

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao obter projeto: {e}"}), 500

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos', methods=['POST'])
def criar_projeto():
    try:
        data = request.get_json()
        usuario_id = get_usuario_logado()

        nome_cliente = data.get('nome_cliente')
        nome_arquiteto = data.get('nome_arquiteto')
        equipe = data.get('equipe', [])
        ambientes = data.get('ambientes', [])

        if not nome_cliente or not nome_arquiteto:
            return jsonify({"mensagem": "Dados obrigatórios ausentes"}), 400

        projeto_id = mexerNoBanco("""
            INSERT INTO projetos (nome_cliente, nome_arquiteto, usuario_criador_id)
            VALUES (%s, %s, %s)
        """, (nome_cliente, nome_arquiteto, usuario_id))

        for membro in equipe:
            mexerNoBanco("""
                INSERT INTO equipe_projeto (projeto_id, usuario_id, cargo)
                VALUES (%s, %s, %s)
            """, (projeto_id, membro['usuario_id'], membro['cargo']))

        for amb in ambientes:
            ambiente_id = mexerNoBanco("""
                INSERT INTO ambientes_projeto (projeto_id, nome_ambiente, tecnico_responsavel_id)
                VALUES (%s, %s, %s)
            """, (projeto_id, amb['nome_ambiente'], amb.get('tecnico_responsavel_id')))

            for mat in amb.get('materiais', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_materiais (ambiente_id, material_id, espessura_mm)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mat['material_id'], mat['espessura_mm']))

            for mob in amb.get('mobiliarios', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_mobiliario (ambiente_id, mobiliario_id, quantidade)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mob['mobiliario_id'], mob.get('quantidade', 1)))

        return jsonify({'mensagem': 'Projeto criado com sucesso', 'projeto_id': projeto_id}), 201

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao criar projeto: {e}"}), 500

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos/<int:projeto_id>', methods=['PUT'])
def atualizar_projeto(projeto_id):
    try:
        data = request.get_json()
        nome_cliente = data.get('nome_cliente')
        nome_arquiteto = data.get('nome_arquiteto')
        novo_criador_id = data.get('usuario_criador_id')
        equipe = data.get('equipe', [])
        ambientes = data.get('ambientes', [])

        if not nome_cliente or not nome_arquiteto or not novo_criador_id:
            return jsonify({"mensagem": "Dados obrigatórios ausentes"}), 400

        mexerNoBanco("""
            UPDATE projetos
            SET nome_cliente = %s, nome_arquiteto = %s, usuario_criador_id = %s
            WHERE id = %s
        """, (nome_cliente, nome_arquiteto, novo_criador_id, projeto_id))

        mexerNoBanco("DELETE FROM equipe_projeto WHERE projeto_id = %s", (projeto_id,))
        for membro in equipe:
            mexerNoBanco("""
                INSERT INTO equipe_projeto (projeto_id, usuario_id, cargo)
                VALUES (%s, %s, %s)
            """, (projeto_id, membro['usuario_id'], membro['cargo']))

        mexerNoBanco("DELETE FROM ambientes_projeto WHERE projeto_id = %s", (projeto_id,))
        for amb in ambientes:
            ambiente_id = mexerNoBanco("""
                INSERT INTO ambientes_projeto (projeto_id, nome_ambiente, tecnico_responsavel_id)
                VALUES (%s, %s, %s)
            """, (projeto_id, amb['nome_ambiente'], amb.get('tecnico_responsavel_id')))

            for mat in amb.get('materiais', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_materiais (ambiente_id, material_id, espessura_mm)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mat['material_id'], mat['espessura_mm']))

            for mob in amb.get('mobiliarios', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_mobiliario (ambiente_id, mobiliario_id, quantidade)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mob['mobiliario_id'], mob.get('quantidade', 1)))

        return jsonify({'mensagem': 'Projeto atualizado com sucesso'}), 200

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao atualizar projeto: {e}'}), 500

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos/<int:projeto_id>', methods=['DELETE'])
def deletar_projeto(projeto_id):
    try:
        mexerNoBanco("DELETE FROM projetos WHERE id = %s", (projeto_id,))
        return jsonify({'mensagem': 'Projeto deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao deletar projeto: {e}'}), 500

