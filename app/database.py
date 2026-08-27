import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Fornece uma sessão de base de dados a um endpoint, e garante
    que é sempre fechada no final, mesmo que ocorra um erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()