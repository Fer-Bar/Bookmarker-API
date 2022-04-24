import pytest

from src.database import User
from src.database import Bookmark


@pytest.fixture(scope='module')
def new_user():
    user = User(username='FlaskUser',
                email='email007@gmail.com',
                password='StrongPass')   
    return user

@pytest.fixture(scope='module')
def new_bookmark():
    bookmark = Bookmark(
                url='www.mysite.com',
                body='This is my website',
                visits= 0   
            )
    return bookmark

