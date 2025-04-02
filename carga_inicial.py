import pandas as pd
from sqlalchemy import text
from database import engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
excel_path = BASE_DIR / 'data' / 'cadastro_alunos.xlsx'

# Carga de alunos
df_alunos = pd.read_excel(excel_path, sheet_name='tb_alunos')
df_alunos.to_sql('tb_alunos', con=engine, if_exists='append', index=False)

# Carga de disciplinas
df_disciplinas = pd.read_excel(excel_path, sheet_name='tb_disciplinas', dtype=str)
df_disciplinas['carga'] = df_disciplinas['carga'].astype(int)
df_disciplinas['semestre'] = df_disciplinas['semestre'].astype(int)
df_disciplinas.to_sql('tb_disciplinas', con=engine, if_exists='append', index=False)

# Carga de carros
carros = [
    {"id": 1, "fabricante": "Toyota", "modelo": "Corolla", "especificacao": "Sedan 2.0 Flex"},
    {"id": 2, "fabricante": "Honda", "modelo": "Civic", "especificacao": "Sedan 1.5 Turbo"},
    {"id": 3, "fabricante": "Ford", "modelo": "Ka", "especificacao": "Hatch 1.0 Flex"},
    {"id": 4, "fabricante": "Chevrolet", "modelo": "Onix", "especificacao": "Hatch 1.4 LTZ"},
]
with engine.begin() as conn:
    sql = text("""
        insert into tb_carros (id, fabricante , modelo, especificacao)
        values (:id, :fabricante, :modelo, :especificacao)
    """)
    for carro in carros:
        conn.execute(sql, carro)

# Carga de endereços
enderecos = [
    {"cep": "01001-000", "endereco": "Avenida Paulista, 1000", "cidade": "São Paulo", "estado": "SP"},
    {"cep": "20031-140", "endereco": "Rua da Assembleia, 10", "cidade": "Rio de Janeiro", "estado": "RJ"},
    {"cep": "30140-000", "endereco": "Praça Sete, Centro", "cidade": "Belo Horizonte", "estado": "MG"},
    {"cep": "40020-010", "endereco": "Avenida Sete de Setembro, 200", "cidade": "Salvador", "estado": "BA"}
]
with engine.begin() as conn:
    sql = text("""
        insert into tb_enderecos (cep, endereco , cidade, estado)
        values (:cep, :endereco, :cidade, :estado)
    """)
    for endereco in enderecos:
        conn.execute(sql, endereco)

# Carga de notas
notas = [
    {"aluno": 1, "disciplina": 1, "nota": 8.5},
    {"aluno": 2, "disciplina": 2, "nota": 7.0},
    {"aluno": 3, "disciplina": 3, "nota": 6.5},
    {"aluno": 1, "disciplina": 2, "nota": 9.0},
    {"aluno": 2, "disciplina": 3, "nota": 7.8},
]
with engine.begin() as conn:
    sql = text("""
        insert into tb_notas (aluno_id, disciplina_id , nota)
        values (:aluno, :disciplina, :nota)
    """)
    for nota in notas:
        conn.execute(sql, nota)