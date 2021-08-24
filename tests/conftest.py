import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from hash_retail import database
from hash_retail.app import create_app


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


@pytest.fixture
def db_session_mock(mocker):
    session_mock = mocker.Mock(Session)

    def session_mock_factory():
        return session_mock

    mocker.patch.object(database, "SessionLocal", session_mock_factory)

    yield session_mock
