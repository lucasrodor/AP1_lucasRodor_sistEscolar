from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da conexão
host = 'localhost'
port = '3306'
user = os.getenv("MYSQL_USER")
senha = quote_plus(os.getenv("MYSQL_PASSWORD"))
database_name = 'db_escola'

DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)