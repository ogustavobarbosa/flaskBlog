from functools import wraps
from flask  import Blueprint, render_template, request, \
    redirect, url_for, session, g
from blog.models import db, User
from  blog.forms import UserLoginForm, UserRegisterForm
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm(request.form)

    if request.method =='POST' and form.validate():
        username = request.form['username']
        password = request.form['password']

        user  = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',  form=form)

@bp.route('/login' , methods=['GET', 'POST'])
def login():
    form = UserLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username =  request.form['username']

        user =  User.query.filter_by(username=username).first()
        session['user_id'] = user.id
        return redirect(url_for('index'))

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Antes de executar qualquer requisição, verifica id do usuario está armazenado na sessão
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


# Um 'decorator' que é usado para verificar se um usuário está logado.
# Criar, editar e excluir postagens de blog exigirá que um usuário esteja conectado.
def login_requerid(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view








