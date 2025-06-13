import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "@Al220497",
    "database": "gerenciador"
}

def buscarNoBanco(consulta: str, params: tuple = ()):
    conexao = mysql.connector.connect(**db_config)
    janelinha = conexao.cursor(dictionary=True)
    janelinha.execute(consulta, params)
    lista = janelinha.fetchall()
    janelinha.close()
    conexao.close()
    return lista

def mexerNoBanco(consulta: str, parametros=None, retornar_id=False):
    conexao = mysql.connector.connect(**db_config)
    janelinha = conexao.cursor()
    janelinha.execute(consulta, parametros or ())
    conexao.commit()
    last_id = janelinha.lastrowid
    janelinha.close()
    conexao.close()
    return last_id if retornar_id else "Operação realizada com sucesso"













