import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.deps import get_db
from app.database.session import Base
from app.main import app


engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    with engine.begin() as connection:
        connection.exec_driver_sql("DELETE FROM users")


def test_register():
    response = client.post(
        "/api/auth/register",
        json={"name": "  Test Student  ", "email": "Student@Example.com", "password": "password123"},
    )
    assert response.status_code == 201
    assert response.json()["user"]["name"] == "Test Student"
    assert response.json()["user"]["email"] == "student@example.com"
    assert "password_hash" not in response.json()["user"]


def test_duplicate_email():
    payload = {"name": "Test Student", "email": "student@example.com", "password": "password123"}
    assert client.post("/api/auth/register", json=payload).status_code == 201
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


def test_short_password():
    response = client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": "student@example.com", "password": "short"},
    )
    assert response.status_code == 422


def test_correct_login():
    client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": "student@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login", json={"email": "STUDENT@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_wrong_password():
    client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": "student@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/login", json={"email": "student@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_me_without_token():
    assert client.get("/api/auth/me").status_code == 401


def test_me_with_valid_token():
    register = client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": "student@example.com", "password": "password123"},
    )
    token = register.json()["access_token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "student@example.com"


def test_me_with_tampered_token():
    register = client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": "student@example.com", "password": "password123"},
    )
    token = register.json()["access_token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}tampered"})
    assert response.status_code == 401
