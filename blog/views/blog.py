
from flask import Blueprint, render_template, \
    request, redirect, g, abort, url_for
from blog.models import db, Blog, User
from blog.forms import BlogForm
from blog.views.auth import  login_requerid

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    blogs = Blog.query.all()

    return render_template('blog/index.html', blogs=blogs )


@bp.route('/create', methods=['GET', 'POST'])
@login_requerid
def create():
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        blog = Blog(title=title, body=body, blog_id=g.user.id)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('blog/create.html', form=form)



def get_post(id):
    blog = Blog.query.filter_by(id=id).first_or_404()
    if blog.blog_id != g.user.id:
        abort(403)

    return blog


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_requerid
def update(id):

    blog = get_post(id)

    form = BlogForm(request.form, blog)

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        form.populate_obj(blog)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('blog/update.html', form=form, blog=blog)

@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_requerid
def delete(id):
    blog = get_post(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('index'))






