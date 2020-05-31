from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class':'validate'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class':'validate'})
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Отправить', render_kw={'class':'btn waves-effect waves-light'})


# class RegistrationForm(FlaskForm):
#     username = StringField('Имя пользователя', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Пароль', validators=[DataRequired()])
#     password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Отправить')

#     def validate_username(self, username):
#         user = User.query.filter_by(login=username.data).first()
#         if user is not None:
#             raise ValidationError('Пользователь с таким именем уже существует')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Пользователь с таким email уже существует')
