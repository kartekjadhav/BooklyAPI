from src.db.db import get_session
from unittest.mock import Mock
from src.app import app
import pytest
from fastapi.testclient import TestClient
from src.dependencies.bearer import AccessTokenBearer
from src.dependencies.role_checker import RoleChecker



mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()

access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(allowed_roles=['admin'])

def get_mock_session():
    yield mock_session

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[access_token_bearer] = Mock()
app.dependency_overrides[role_checker] = Mock()

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_book_service():
    return Mock()

@pytest.fixture
def test_client():
    return TestClient(app)