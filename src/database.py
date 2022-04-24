from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark', backref='user')
    
    def __repr__(self):
        return f'User>>>{self.username}'

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3))
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def generate_short_character(self):
        characters = string.digits + string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=3))
        
        link = self.query.filter_by(short_url=picked_chars).first()
        # Si el link o el short url existe en la db, debemos generar otro hasta encontrarlo.
        if link: 
            self.generate_short_character()
        else:
            return picked_chars #Devolvemos una combinacion de caracteres como short url

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs) # Traemos todas las cosas de la clase db.Model, heredanlos a nuestra clase actual
    #     self.short_url = self.generate_short_character()

    def __repr__(self):
        return f'Bookmark>>>{self.url}'