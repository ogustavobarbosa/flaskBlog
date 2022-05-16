import pytest

from blog.models import db, User, Blog
from flask import session, g





def test_register_user(client):
    """ Teste o registro de novos usuários """

    response = client.get('/auth/register')
    assert response.status_code == 200

    data = {
        'username': 'João',
        'password': '123',
        'confirm': '123'
    }
    response = client.post('/auth/register', data=data)
    assert response.headers['Location'] == '/auth/login'

    # with app.app_context():
    assert User.query.filter_by(username='João').first()


@pytest.mark.parametrize(
    ('username', 'password', 'confirm', 'message'),
    (
            ('', 'admin', 'admin', 'Uma usuário é requerido'),
            ('admin', '', '', 'Uma senha é requerida'),
            ('admin', '123', '321', 'As senhas devem ser iguais'),
            ('admin', 'admin', 'admin', ''),
            ('admin', 'admin', '', 'Usuário já cadastrado!'),
    )
)
def test_register_validate_input(auth, client, username, password, confirm,  message):

    response = auth.register(username, password, confirm)
    # response = client.post('/auth/register', data=data)
    assert message in response.get_data(as_text=True)


def test_login(client, auth):
    response = auth.register()


    response = client.get('/auth/login')
    assert response.status_code == 200

    response = auth.login()


    client.get('/')

    user = User.query.filter_by(username='admin').first()
    assert user

    assert session.get('user_id') == user.id
    assert g.user.id == user.id


@pytest.mark.parametrize(
    ('username', 'password', 'message'),(
            ('123', 'admin', 'Usuário não registrado!'),
            ('admin', '123', 'Senha incorreta!'),
    )

)
def test_login_validate_input(client, auth, username, password, message):
    client.post(
        '/auth/register',
        data={'username': 'admin',
              'password': 'admin',
              'confirm': 'admin'})

    response = auth.login(username=username, password=password)
    assert message in response.get_data(as_text=True)

def test_logout(app, client, auth):

    response = auth.register()
    assert 'user_id' not in session

    response = auth.login()
    assert 'user_id' in session

    auth.logout()
    assert 'user_id' not in session


