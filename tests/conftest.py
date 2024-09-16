import pytest
from app import create_app
from app.models import db as _db

@pytest.fixture(scope='module')
def app():
    app = create_app(config_name='testing')
    app.config['TESTING'] = True

    with app.app_context():
        _db.create_all()  # Create tables in the test database

    yield app

    with app.app_context():
        _db.drop_all()  # Clean up the database after tests

@pytest.fixture(scope='module')
def db(app):
    return _db

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
