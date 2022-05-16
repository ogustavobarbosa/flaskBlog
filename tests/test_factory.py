from blog import create_app

def test_conf():
    assert not create_app().testing
    assert create_app({'TESTING':True}).testing