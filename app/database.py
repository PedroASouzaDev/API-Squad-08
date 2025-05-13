from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import dotenv

dotenv.load_dotenv()

# Conexão com o banco de dados (substitua a URL conforme necessário)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Criação do engine de conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Criação da base para modelos
Base = declarative_base()

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
