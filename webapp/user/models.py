from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    nick = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    superuser = db.Column(db.Integer)
    photo = db.Column(db.String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 5 # Администратор

    @property
    def is_user(self):
        return 1 < self.role < 5 # Для авторизованных пользователей, но не юристов

    @property
    def is_lawyer(self):
        return self.role == 3 # Юрист

    @property
    def is_simple_user(self):
        return self.role == 2 # Пользователь

    def __repr__(self):
        return "<Пользователь: {}, ID: {}>".format(self.login, self.id)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Integer, nullable=False)

    user = relationship('User', backref='role_name')

    def __repr__(self):
        return f'<Роль: {self.role}, ID: {self.id}>'
