# 📚 Sistema Escolar com Python, MySQL e Streamlit

Este é um sistema escolar feito com Python, usando Streamlit como interface web e MySQL como banco de dados. O objetivo é gerenciar alunos, disciplinas, notas e endereços de forma simples e funcional.

Desenvolvido por - 
Lucas Rodor
   Linkedin: [Lucas Rodor](https://www.linkedin.com/in/lucasrodor/)
   Github: [Lucas Rodor](https://github.com/lucasrodor)

---

## 🚀 Funcionalidades

- Cadastro e edição de alunos
- Cadastro e edição de notas
- Cadastro e validação de endereços (por CEP)
- Relatório de notas com filtro por disciplina
- Exportação de boletim em PDF
- Importação de alunos por planilha Excel (`.xlsx`)

---

## 🧰 Tecnologias utilizadas

- Python
- Streamlit
- MySQL
- SQLAlchemy
- Pandas
- OpenPyXL
- FPDF
- Streamlit Option Menu

---

## 📁 Estrutura do Projeto

```
├── appteste.py              # Interface principal Streamlit
├── crud_alunos.py           # Funções de banco de dados (CRUD)
├── database.py              # Conexão com o banco de dados
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação do projeto
├── .env                     # Variáveis de ambiente (opcional)
└── data/                    # Pasta opcional para planilhas Excel
```

---

## ⚙️ Configuração do Banco de Dados

Edite o arquivo `database.py` com suas credenciais:

```python
user = 'root'
senha = 'SUA_SENHA'
host = 'localhost'
port = '3306'
database = 'db_escola'
```

---

## ▶️ Como rodar o projeto

1. Crie um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   streamlit run appteste.py
   ```

---

## ✅ Dependências

```txt
pandas==2.2.1
sqlalchemy==2.0.29
pymysql==1.1.0
streamlit==1.32.2
openpyxl==3.1.2
python-dotenv==1.0.1
fpdf==1.7.2
streamlit-extras==0.2.8
ipykernel==6.29.3
streamlit-option-menu==0.3.6
```

---

## 📄 Licença

Projeto desenvolvido para fins educacionais.
