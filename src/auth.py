# Rutas de autenticación(auth)
import validators
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from src.constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                             HTTP_400_BAD_REQUEST,
                                             HTTP_401_UNAUTHORIZED,
                                             HTTP_409_CONFLICT)
from src.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token


auth = Blueprint('auth', __name__,
                url_prefix='/api/v1/auth')

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    pwd_hash = generate_password_hash(password)

    if len(password) < 6:
        return jsonify({
            'error': 'The password must be at least 6 characters'}), HTTP_400_BAD_REQUEST
    
    if len(password) < 3:
        return jsonify({
            'error': 'The username and password must be at least 3 characters'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username must be alphanumeric, also don't have spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "The email address is already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "The username is already in use"}), HTTP_409_CONFLICT

    """ Create a new user """  
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User was created",
        'user': {
            'username': username, "email": email
        }
    }), HTTP_201_CREATED


@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:

        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:

            refresh_tk = create_refresh_token(identity=user.id)
            access_tk = create_access_token(identity=user.id)
            
            return jsonify({
                'access_tk': access_tk,
                'refresh_tk': refresh_tk,
                'username': user.username,
                'email': user.email       
                })

    return jsonify({
        'error': 'Wrong credentials'
    })            

 
@auth.get('/me')
def me():
    return {'username': 'me'}
