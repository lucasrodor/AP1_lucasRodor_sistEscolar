import streamlit as st
import pandas as pd
from fpdf import FPDF
from streamlit_option_menu import option_menu
from crud_alunos import (
    cadastrar_endereco,
    cadastrar_alunos,
    buscar_aluno,
    buscar_todos_alunos,
    editar_alunos,
    verificar_cep_existe,
    buscar_disciplinas,
    cadastrar_nota,
    editar_nota,
    buscar_notas_por_aluno,
    nota_existe,
    buscar_nota_especifica,
    validar_cep
)

st.set_page_config(page_title="Sistema Escolar", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #1e1e1e;
            color: #f0f0f0;
        }
        .stButton>button {
            background-color: #3a3a3a;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 16px;
        }
        .stButton>button:hover {
            background-color: #505050;
        }
        .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div>div {
            background-color: #2c2c2c;
            color: white;
        }
        .stMultiSelect>div>div>div, .stDataFrameContainer {
            background-color: #2c2c2c;
        }
    </style>
""", unsafe_allow_html=True)

with st.container():
    selected = option_menu(
        menu_title=None,
        options=[
            "Cadastro de endereço",
            "Cadastro de aluno",
            "Edição de aluno",
            "Cadastro de nota",
            "Edição de nota",
            "Relatório de notas",
            "Importar Excel"
        ],
        icons=["box-arrow-in-down", "person-plus", "pencil-square", "file-earmark-plus", "arrow-repeat", "file-earmark-text"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#2a2a2a"},
            "icon": {"color": "#cccccc", "font-size": "16px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "0px",
                "color": "#cccccc",
                "padding": "10px"
            },
            "nav-link-selected": {
                "background-color": "#444444",
                "color": "#ffffff"
            },
        }
    )

menu = selected
st.title("📚 Sistema Escolar")

if menu == "Cadastro de endereço":
    st.header("🏠 Cadastro de Endereço")
    st.write("Preencha os campos abaixo para adicionar um novo endereço ao sistema.")
    with st.form("form_endereco"):
        cep_input = st.text_input("CEP")
        endereco = st.text_input("Endereço")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            cep = validar_cep(cep_input)
            if not cep:
                st.error("CEP inválido. Digite exatamente 8 números.")
            else:
                cadastrar_endereco({"cep": cep, "endereco": endereco, "cidade": cidade, "estado": estado})
                st.success("Endereço cadastrado com sucesso!")


elif menu == "Cadastro de aluno":
    st.header("🧑‍🎓 Cadastro de Aluno")
    st.write("Cadastre um novo aluno. Se o CEP informado não estiver no sistema, inclua também o endereço.")
    with st.form("form_aluno"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        cep_input = st.text_input("CEP")
        carro_id = st.text_input("ID do carro (opcional)")

        cep = validar_cep(cep_input)
        mostrar_endereco = False
        if cep:
            mostrar_endereco = not verificar_cep_existe(cep)
        elif cep_input:
            st.warning("CEP inválido. Digite exatamente 8 números.")

        if mostrar_endereco:
            st.warning("CEP não encontrado. Preencha os dados para cadastrar o endereço junto.")
            endereco = st.text_input("Endereço")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado")

        submitted = st.form_submit_button("Cadastrar Aluno")
        if submitted:
            if not cep:
                st.error("CEP inválido. Corrija o campo antes de cadastrar.")
            else:
                if mostrar_endereco:
                    cadastrar_endereco({"cep": cep, "endereco": endereco, "cidade": cidade, "estado": estado})
                cadastrar_alunos({
                    "nome_aluno": nome,
                    "email": email,
                    "cep": cep,
                    "carro_id": int(carro_id) if carro_id else None
                })
                st.success("Aluno cadastrado com sucesso!")


elif menu == "Edição de aluno":
    st.header("✏️ Edição de Aluno")
    st.write("Selecione um aluno cadastrado para editar suas informações.")
    alunos = buscar_todos_alunos()
    if alunos:
        alunos_dict = {aluno[1]: aluno[0] for aluno in alunos}
        aluno_nome = st.selectbox("Escolha o aluno para editar:", list(alunos_dict.keys()))
        aluno_id = alunos_dict[aluno_nome]
        dados = buscar_aluno(aluno_id)

        if dados:
            nome, email, cep_atual, carro_id = dados
            with st.form("form_edicao_aluno"):
                novo_nome = st.text_input("Nome", nome)
                novo_email = st.text_input("Email", email)
                novo_cep_input = st.text_input("CEP", cep_atual or "")
                novo_carro_id = st.text_input("ID do carro", str(carro_id) if carro_id else "")

                endereco = cidade = estado = None
                novo_cep = None
                mostrar_endereco = False

                submitted = st.form_submit_button("Atualizar")

                if submitted:
                    if novo_cep_input != cep_atual:
                        novo_cep = validar_cep(novo_cep_input) if novo_cep_input else None

                        if not novo_cep:
                            st.error("CEP inválido. Corrija antes de atualizar.")
                            st.stop()

                        if not verificar_cep_existe(novo_cep):
                            st.warning("CEP não encontrado. Preencha os dados do novo endereço.")
                            endereco = st.text_input("Endereço")
                            cidade = st.text_input("Cidade")
                            estado = st.text_input("Estado")

                            if not (endereco and cidade and estado):
                                st.error("Preencha todos os dados do novo endereço antes de atualizar.")
                                st.stop()

                            cadastrar_endereco({
                                "cep": novo_cep,
                                "endereco": endereco,
                                "cidade": cidade,
                                "estado": estado
                            })

                    editar_alunos(
                        aluno_id,
                        novo_nome if novo_nome != nome else None,
                        novo_email if novo_email != email else None,
                        novo_cep if novo_cep and novo_cep != cep_atual else None,
                        int(novo_carro_id) if novo_carro_id and novo_carro_id != str(carro_id) else None
                    )
                    st.success("Aluno atualizado com sucesso!")
    else:
        st.warning("Nenhum aluno cadastrado.")




elif menu == "Cadastro de nota":
    st.header("📝 Cadastro de Nota")
    st.write("Registre uma nota para um aluno em uma disciplina específica.")
    alunos = buscar_todos_alunos()
    disciplinas = buscar_disciplinas()
    if alunos and disciplinas:
        alunos_dict = {a[1]: a[0] for a in alunos}
        disciplinas_dict = {d[1]: d[0] for d in disciplinas}

        with st.form("form_nota"):
            aluno_nome = st.selectbox("Aluno", list(alunos_dict.keys()))
            disciplina_nome = st.selectbox("Disciplina", list(disciplinas_dict.keys()))
            nota = st.number_input("Nota", 0.0, 10.0, 7.0, 0.1)
            submitted = st.form_submit_button("Cadastrar Nota")
            if submitted:
                aluno_id = alunos_dict[aluno_nome]
                disciplina_id = disciplinas_dict[disciplina_nome]
                if nota_existe(aluno_id, disciplina_id):
                    st.warning("Este aluno já possui nota para essa disciplina.")
                else:
                    cadastrar_nota(aluno_id, disciplina_id, nota)
                    st.success("Nota cadastrada com sucesso!")

elif menu == "Edição de nota":
    st.header("🔁 Edição de Nota")
    st.write("Altere uma nota já existente de um aluno para uma determinada disciplina.")
    alunos = buscar_todos_alunos()
    disciplinas = buscar_disciplinas()
    if alunos and disciplinas:
        alunos_dict = {a[1]: a[0] for a in alunos}
        disciplinas_dict = {d[1]: d[0] for d in disciplinas}

        col1, col2 = st.columns(2)
        with col1:
            aluno_nome = st.selectbox("Aluno", list(alunos_dict.keys()))
        with col2:
            disciplina_nome = st.selectbox("Disciplina", list(disciplinas_dict.keys()))

        aluno_id = alunos_dict[aluno_nome]
        disciplina_id = disciplinas_dict[disciplina_nome]
        nota_atual = buscar_nota_especifica(aluno_id, disciplina_id)

        if nota_atual is not None:
            nova_nota = st.number_input("Nova Nota", 0.0, 10.0, nota_atual, 0.1)
            if st.button("Atualizar Nota"):
                editar_nota(aluno_id, disciplina_id, nova_nota)
                st.success("Nota atualizada com sucesso!")
        else:
            st.warning("Esse aluno não possui nota nesta disciplina.")

elif menu == "Relatório de notas":
    st.header("📄 Relatório de Notas")
    alunos = buscar_todos_alunos()
    if alunos:
        alunos_dict = {a[1]: a[0] for a in alunos}
        filtro_nome = st.text_input("🔍 Filtrar aluno por nome:")
        #filtra os nomes com um list comprehension para verificar se o nome digitado ta no dicionario de alunos,
        #se tiver, apareça esse nome ou nomes que contenham parte dele, se não, lista todos os nomes e mostra eles
        nomes_filtrados = [nome for nome in alunos_dict if filtro_nome.lower() in nome.lower()] if filtro_nome else list(alunos_dict.keys())
        selecionados = st.multiselect("Selecione os alunos:", nomes_filtrados)

        for nome in selecionados:
            aluno_id = alunos_dict[nome]
            st.subheader(f"📘 {nome}")
            df = buscar_notas_por_aluno(aluno_id)

            disciplina_filtro = st.text_input(f"Filtrar disciplinas para {nome}:", key=nome)
            if disciplina_filtro:
                # pega as colunas do DataFrame que contei o que foi escrito no filtro da discplina
                df = df[df['Disciplina'].str.lower().str.contains(disciplina_filtro.lower())]

            st.dataframe(df, use_container_width=True)
            if st.button(f"Exportar PDF - {nome}"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Relatório de Notas - {nome}", ln=True, align="C")
                pdf.ln(5)
                for _, row in df.iterrows():
                    pdf.cell(200, 10, txt=f"{row['Disciplina']}: {row['Nota']}", ln=True)
                caminho = f"relatorio_notas_{nome}.pdf"
                pdf.output(caminho)
                st.success(f"PDF gerado: {caminho}")
    else:
        st.warning("Nenhum aluno encontrado para gerar relatório.")

# Importação de planilha Excel
elif menu == "Importar Excel":
    st.header("📥 Importar Alunos por Excel")
    arquivo = st.file_uploader("Envie um arquivo .xlsx com as colunas: nome_aluno, email, cep, carro_id", type=["xlsx"])
    if arquivo:
        try:
            df = pd.read_excel(arquivo)
            st.write("Pré-visualização dos dados:")
            st.dataframe(df)
            if st.button("Importar alunos"):
                inseridos = 0
                for i, row in df.iterrows():
                    try:
                        cep_formatado = validar_cep(str(row['cep']))
                        if not cep_formatado:
                            st.warning(f"Linha {i + 2}: CEP inválido.")
                            continue
                        if not verificar_cep_existe(cep_formatado):
                            cadastrar_endereco({"cep": cep_formatado, "endereco": "Importado", "cidade": "Importado", "estado": "XX"})
                        cadastrar_alunos({
                            "nome_aluno": row['nome_aluno'],
                            "email": row['email'],
                            "cep": cep_formatado,
                            "carro_id": int(row['carro_id']) if not pd.isna(row['carro_id']) else None
                        })
                        inseridos += 1
                    except Exception as e:
                        st.warning(f"Erro ao importar linha {i + 2}: {e}")
                st.success(f"Importação finalizada! {inseridos} alunos cadastrados.")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
