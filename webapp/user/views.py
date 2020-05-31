from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from webapp.user.forms import LoginForm
from webapp.user.models import User
from webapp import db

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login/', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('dashboard.dashboard_index'))
    flash('Неправильное имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('dashboard.dashboard_index'))


# @blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard.dashboard_index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(login=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('user.login'))
#     return render_template('user/register.html', title='Register', form=form)
