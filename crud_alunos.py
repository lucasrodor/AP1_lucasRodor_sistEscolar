from sqlalchemy import text
from database import engine
import pandas as pd


def cadastrar_endereco(params: dict):
    sql = text("""
        INSERT INTO tb_enderecos (cep, endereco, cidade, estado)
        VALUES (:cep, :endereco, :cidade, :estado)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

def validar_cep(cep):
    """Remove traços, pontos, espaços e valida se tem 8 dígitos numéricos."""
    if not cep:
        return None
    cep_limpo = cep.replace("-", "").replace(".", "").replace(" ", "")
    return cep_limpo if cep_limpo.isdigit() and len(cep_limpo) == 8 else None

def verificar_cep_existe(cep):
    sql = text("SELECT 1 FROM tb_enderecos WHERE cep = :cep LIMIT 1")
    with engine.connect() as conn:
        result = conn.execute(sql, {"cep": cep}).fetchone()
    return result is not None


def cadastrar_alunos(params: dict):
    sql = text("""
        INSERT INTO tb_alunos (nome_aluno, email, cep, carro_id)
        VALUES (:nome_aluno, :email, :cep, :carro_id)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)


def buscar_todos_alunos():
    sql = text("SELECT id, nome_aluno FROM tb_alunos")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return result


def buscar_aluno(aluno_id):
    sql = text("SELECT nome_aluno, email, cep, carro_id FROM tb_alunos WHERE id = :aluno_id")
    with engine.connect() as conn:
        result = conn.execute(sql, {"aluno_id": aluno_id}).fetchone()
    return result


def editar_alunos(aluno_id, novo_nome=None, novo_email=None, novo_cep=None, novo_carro_id=None):
    query_parts = []
    params = {"aluno_id": aluno_id}

    if novo_nome:
        query_parts.append("nome_aluno = :novo_nome")
        params["novo_nome"] = novo_nome
    if novo_email:
        query_parts.append("email = :novo_email")
        params["novo_email"] = novo_email
    if novo_cep:
        query_parts.append("cep = :novo_cep")
        params["novo_cep"] = novo_cep
    if novo_carro_id:
        query_parts.append("carro_id = :novo_carro_id")
        params["novo_carro_id"] = novo_carro_id

    if not query_parts:
        return

    sql = text(f"UPDATE tb_alunos SET {', '.join(query_parts)} WHERE id = :aluno_id")
    with engine.begin() as conn:
        conn.execute(sql, params)

def buscar_disciplinas():
    sql = text("SELECT id, nome_disciplina FROM tb_disciplinas")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return result


def cadastrar_nota(aluno_id, disciplina_id, nota):
    sql = text("""
        INSERT INTO tb_notas (aluno_id, disciplina_id, nota)
        VALUES (:aluno_id, :disciplina_id, :nota)
    """)
    with engine.begin() as conn:
        conn.execute(sql, {
            "aluno_id": aluno_id,
            "disciplina_id": disciplina_id,
            "nota": nota
        })


def editar_nota(aluno_id, disciplina_id, nova_nota):
    sql = text("""
        UPDATE tb_notas SET nota = :nota
        WHERE aluno_id = :aluno_id AND disciplina_id = :disciplina_id
    """)
    with engine.begin() as conn:
        conn.execute(sql, {
            "aluno_id": aluno_id,
            "disciplina_id": disciplina_id,
            "nota": nova_nota
        })


def buscar_notas_por_aluno(aluno_id):
    sql = text("""
        SELECT d.nome_disciplina, n.nota
        FROM tb_notas n
        JOIN tb_disciplinas d ON n.disciplina_id = d.id
        WHERE n.aluno_id = :aluno_id
    """)
    with engine.connect() as conn:
        result = conn.execute(sql, {"aluno_id": aluno_id})
        df = pd.DataFrame(result.fetchall(), columns=["Disciplina", "Nota"])
    return df


def nota_existe(aluno_id, disciplina_id):
    sql = text("""
        SELECT 1 FROM tb_notas
        WHERE aluno_id = :aluno_id AND disciplina_id = :disciplina_id
        LIMIT 1
    """)
    with engine.connect() as conn:
        result = conn.execute(sql, {"aluno_id": aluno_id, "disciplina_id": disciplina_id}).fetchone()
    return result is not None


def buscar_nota_especifica(aluno_id, disciplina_id):
    sql = text("""
        SELECT nota FROM tb_notas
        WHERE aluno_id = :aluno_id AND disciplina_id = :disciplina_id
    """)
    with engine.connect() as conn:
        result = conn.execute(sql, {"aluno_id": aluno_id, "disciplina_id": disciplina_id}).fetchone()
    return float(result[0]) if result else None