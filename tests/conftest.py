import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def postgres_container():
    """
    Cria um container PostgreSQL temporário, uma única vez,
    partilhado por todos os testes desta sessão.
    """
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    """
    Cria a 'engine' do SQLAlchemy apontada para o container temporário,
    e cria todas as tabelas nele.
    """
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture()
def db_session(test_engine):
    """
    Cria uma sessão nova para CADA teste individual, e desfaz
    (rollback) tudo o que esse teste fez, no final.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    """
    Fornece um TestClient da FastAPI, com a dependência get_db
    substituída para usar a base de dados de teste.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()