"""
This file (test_models.py) contains the unit tests for the database.py file.
"""
from src.database import User, Bookmark

def test_new_user(new_user):
    """
    GIVEN a User model \n
    WHEN a new User is created \n
    THEN check the user, email, password, authenticated, and active fields are defined correctly
    """
             
    assert new_user.email == 'email007@gmail.com'
    assert new_user.password == 'StrongPass'
    assert new_user.__repr__() == 'User>>>FlaskUser'


def test_new_bookmark(new_bookmark):
    """
    GIVEN a bookmark model \n
    WHEN a new bookmark is created \n
    THEN check the url, body fields are defined correctly
    """
    assert new_bookmark.url == 'www.mysite.com'
    assert new_bookmark.body == 'This is my website'
    assert new_bookmark.__repr__() == 'Bookmark>>>www.mysite.com'



