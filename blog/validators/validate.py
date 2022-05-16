from blog.models import User
from wtforms import ValidationError
from werkzeug.security import check_password_hash

def check_username_already_registered(form, username_field):
    user = User.query.filter_by(username=username_field.data).first()
    if user:
        raise ValidationError('Usuário já cadastrado!')

def check_user_password(form, username_field):
    user = User.query.filter_by(username=username_field.data).first()
    password = form.password.data
    if not user:
        raise ValidationError('Usuário não registrado!')
    elif not check_password_hash(user.password, password):
        raise ValidationError('Senha incorreta!')