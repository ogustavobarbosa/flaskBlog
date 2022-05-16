from wtforms import Form, StringField, validators, \
    PasswordField, SubmitField, ValidationError, TextAreaField

from blog.validators.validate import check_username_already_registered,\
                                        check_user_password

class UserLoginForm(Form):
    username = StringField('Usuário',[validators.DataRequired(message='Uma usuário é requerido'), check_user_password])
    password = PasswordField('Senha', [validators.DataRequired(message='Uma senha é requerida')])
    submit = SubmitField('Enviar')


class UserRegisterForm(UserLoginForm):
    username = StringField('Usuário', [validators.Length(min=4,
                                                         max=20,
                                                         message='O campo de usuário deve ter entre %(min)d e %(max)d caracteres'),
                                       check_username_already_registered, validators.DataRequired(message='Uma usuário é requerido')
                                       ])
    password = PasswordField('Senha', [validators.DataRequired(message='Uma senha é requerida'),
                                        validators.EqualTo('confirm', message='As senhas devem ser iguais'),
                                        ])
    confirm = PasswordField('Corfirme sua senha')

class BlogForm(Form):
    title = StringField('Título', [validators.DataRequired(message='Um titulo é requerido')])
    body = TextAreaField('Corpo')
    submit = SubmitField('Salvar')







