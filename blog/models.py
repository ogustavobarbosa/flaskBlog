from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    blog = db.relationship('Blog', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class  Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(300), nullable=True)
    created_date = db.Column( db.DateTime, default=datetime.datetime.utcnow)
    blog_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Blog %r>' % self.title
