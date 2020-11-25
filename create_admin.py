from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()
with app.app_context():
    login = input('Введите логин: ')
    password = input('Введите пароль: ')
    first_name = input('Введите имя администратора: ')
    last_name = input('Введите фамилию администратора: ')
    if User.query.filter(User.login == login).count():
        print(f'{login} already exists')
        sys.exit(0)
    new_user = User(login=login, nick='admin', first_name=first_name, last_name=last_name, middle_name='', superuser=0, role=5)
    new_user.set_password(password)
    db.session.add(new_user) 
    db.session.commit()
    print(f'Create user {login} with id={new_user.id}')
