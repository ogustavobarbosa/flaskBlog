import pytest


from blog import create_app
from blog.models import db, Blog
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture(scope='module')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + BASE_DIR + '/test.db'
    })


    with app.app_context():
        # other setup can go here
        db.create_all()

        yield app

        # clean up / reset resources here
        db.drop_all()

class AuthActions():
    def __init__(self, client):
        self._client = client

    def register(self, username='admin', password='admin', confirm='admin'):
        return self._client.post('/auth/register', data=
                                {
                                'username': username,
                                'password': password,
                                'confirm': confirm
                                },
                                 follow_redirects=True
                                 )

    def login(self, username='admin', password='admin'):
        return self._client.post('/auth/login',
                                 data={'username': username, 'password': password},
                                 follow_redirects=True
                                 )

    def logout(self):
        return self._client.get('/auth/logout', follow_redirects=True)



@pytest.fixture
def auth(client):

    return AuthActions(client)


class BlogActions():
    def __init__(self, client):
        self._client = client

    def create(self, title='post', body='post', id=1):
        return self._client.post('/create', data={'title': title, 'body': body })

    def update(self, title='updated', body='change', id=1):
        return self._client.post(f'/{id}/update', data={'title': title, 'body': body })

    def delete(self, id=1):
        return self._client.get(f'/{id}/delete')

@pytest.fixture
def post(client):
    return BlogActions(client)








