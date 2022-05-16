from flask import session
from blog.models import Blog, db
def test_index(client, auth):

    response = client.get('/')
    page = response.get_data(as_text=True)

    assert 'Entrar' in page
    assert 'Cadastre-se' in page

    auth.register()
    assert 'user_id' not in session

    auth.login()
    response = client.get('/')

    page_logged = response.get_data(as_text=True)

    assert 'user_id' in session
    assert 'Sair' in page_logged
    assert 'admin' in page_logged
    assert  'post' in page_logged



def test_login_requerid(post):
    assert post.create().headers['Location'] == '/auth/login'
    assert post.update().headers['Location'] == '/auth/login'
    assert post.delete().headers['Location'] == '/auth/login'

def test_author_change_other_post(client, auth, post):
    """Testa se um usuario pode modificar ou deletar um post de outro usuário"""

    user1 = { 'username': 'user1', 'password': '123', 'confirm': '123'}
    user2 = { 'username': 'user2', 'password': '123', 'confirm': '123'}

    auth.register(**user1)
    auth.register(**user2)

    user1 = dict(list(user1.items())[:-1])
    user2 = dict(list(user2.items())[:-1])

    # user1 cria um post
    auth.login(**user1)
    response = post.create('post')

    assert response.headers['Location'] == '/'
    # Verifica se o post foi persistido no banco de dados
    assert Blog.query.filter_by(title='post').first()

    auth.logout()

    # user2 faz o login
    auth.login(**user2)

    # user2 tenta faz uma request para ATUALIZAR o post do user1
    response = post.update()
    # O servidor verifica a requisição, mas não autoriza o pedido
    assert response.status_code == 403

    # user2 tenta faz uma request para DELETAR o post do user1
    response = post.delete()
    assert response.status_code == 403
    # verifica o se user2, tem esse recurso de editar o post em tela
    assert b'href="/1/update"' not in client.get('/').data


def test_exists_requerid(auth, post):

    auth.login()

    assert post.update(id=2).status_code == 404
    assert post.delete(id=2).status_code == 404

def test_create(client, auth, post):

    auth.login()

    assert client.get('/create').status_code == 200

    post.create('created')
    p = Blog.query.all()
    assert len(p) == 2

def test_update(client, auth, post):

    auth.login()

    assert client.get('/2/update').status_code == 200

    assert post.update(id=2).status_code == 302

    assert Blog.query.filter_by(title='updated').first()

def test_update_validade_required_title(auth, post):
    auth.login()

    response = post.update(title='', body='', id=2)
    assert 'Um titulo é requerido' in response.get_data(as_text=True)

    response = post.create(title='', body='',  id=2)
    assert 'Um titulo é requerido' in response.get_data(as_text=True)


def test_delete(auth, post):

    auth.login()
    response =  post.delete(id=2)
    assert response.status_code == 302

    assert Blog.query.count() == 1
    assert response.headers['Location'] == '/'

