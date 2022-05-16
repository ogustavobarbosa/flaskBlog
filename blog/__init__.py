from flask import Flask
from blog.models import db, User
from flask_migrate import Migrate

migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "pyhton"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    if test_config:
        app.config.from_mapping(test_config)
    #Inicia o banco de dados
    from blog.models import db
    db.init_app(app)
    migrate.init_app(app, db)

    from blog.views import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app