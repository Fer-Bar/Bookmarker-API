import pytest

from src.database import User
from src.database import Bookmark
from src import create_app

@pytest.fixture(scope='module')
def new_user():
    user = User(username='FlaskUser',
                email='email007@gmail.com',
                password='StrongPass')   
    return user


@pytest.fixture(scope="function")
def fixture_create_app():
    """Instance of main flask app"""
    return create_app()

