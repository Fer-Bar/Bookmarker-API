"""
This file (test_models.py) contains the unit tests for the database.py file.
"""

def test_new_user(new_user):
    """
    GIVEN a User model \n
    WHEN a new User is created \n
    THEN check the user, email, password, authenticated, and active fields are defined correctly
    """
             
    assert new_user.email == 'email007@gmail.com'
    assert new_user.password == 'StrongPass'
    assert new_user.__repr__() == 'User>>>FlaskUser'

def test_app_is_created(fixture_create_app):
    assert fixture_create_app.name == "src"



