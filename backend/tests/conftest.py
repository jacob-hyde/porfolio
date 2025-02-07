"""Test configuration and fixtures for the application."""
import os
import tempfile

import pytest
from app import create_app
from app.models.models import db as _db


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-key',
        'JWT_SECRET_KEY': 'jwt-test-key'
    })

    with app.app_context():
        _db.create_all()
        yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Create a test database."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
