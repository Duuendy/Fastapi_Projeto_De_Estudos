from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , Session, DeclarativeBase

DATABASE_URL = 'postgresql://postgres:123456@localhost:5432/fastapi_estudos'
DB_Engine = create_engine(DATABASE_URL, echo=True)
DB_Session_Pool = sessionmaker(autocommit=False, autoflush=False, bind=DB_Engine)

class DBModel(DeclarativeBase):
    """
    Classe que herda de `sqlalchemy.DeclarativeBase`.
    Todas as classes que herdarem esta classe, serão mapeadas com tabelas no banco de dados.
    """
    pass


def get_db_connection() -> Session:

    db_connection = DB_Session_Pool()
    
    try:
        yield db_connection

    finally:
        db_connection.close()