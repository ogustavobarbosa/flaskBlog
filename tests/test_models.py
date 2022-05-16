
from blog.models import User, db
def test_create_user_db(app):
    new_user = {
        'username': 'João',
        'password': '123'
    }
    user = User(**new_user)
    with app.app_context():
        db.session.add(user)
        assert User.query.filter_by(username='João').first().username  == 'João'

def test_user():
    u = User(username='João', password='123')

    db.session.add(u)
    db.session.commit()

    assert repr(u) == "<User 'João'>"