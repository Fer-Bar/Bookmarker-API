# Rutas de autenticación(auth)
import json
import validators
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from werkzeug.security import check_password_hash, generate_password_hash

from src.constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                             HTTP_400_BAD_REQUEST,
                                             HTTP_401_UNAUTHORIZED,
                                             HTTP_409_CONFLICT,
                                             HTTP_404_NOT_FOUND)
from src.database import User, db
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, get_jwt_identity)

auth = Blueprint('auth', __name__,
                url_prefix='/api/v1/auth')

@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    pwd_hash = generate_password_hash(password)

    if len(password) < 6:
        return jsonify({
            'error': 'The password must be at least 6 characters'
            }), HTTP_400_BAD_REQUEST
    
    if len(password) < 3:
        return jsonify({
            'error': 'The username and password must be at least 3 characters'
            }), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({
            'error': "Username must be alphanumeric, also don't have spaces"
            }), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': "The email address is already in use"
            }), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            'error': "The username is already in use"
            }), HTTP_409_CONFLICT

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
@swag_from('./docs/auth/login.yaml')
def login(): 
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:

        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:

            access_tk = create_access_token(identity=user.id)
            refresh_tk = create_refresh_token(identity=user.id)
            
            return jsonify({
                'username': user.username,
                'email': user.email,       
                'access_tk': access_tk,
                'refresh_tk': refresh_tk
                }), HTTP_200_OK

        return jsonify({
            'error': 'Wrong password'
        }), HTTP_401_UNAUTHORIZED  

    else:
        return jsonify({"msg": "User/Email not found"}), HTTP_404_NOT_FOUND

 
@auth.get('/me')
@jwt_required()
@swag_from('./docs/auth/profile.yaml')
def me():
    # Access the identity of the current user with get_jwt_identity
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'username': user.username,
        'email': user.email
        }), HTTP_200_OK



@auth.get('/token/refresh')
@jwt_required(refresh=True)
@swag_from('./docs/auth/refresh_token.yaml')
def refresh_users_token():
    # Access the identity of the current user with get_jwt_identity
    identity = get_jwt_identity()
    access_tk = create_access_token(identity=identity)

    return jsonify({
        'access_tk': access_tk
    }), HTTP_200_OK
    
