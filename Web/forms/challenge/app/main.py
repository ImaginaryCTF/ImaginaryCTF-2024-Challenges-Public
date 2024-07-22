import bcrypt
from flask import flash, Flask, redirect, render_template, request, Response
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import json
from secrets import token_bytes
from threading import Thread
from uuid import UUID, uuid4

from .bot import visit

app = Flask(__name__)
app.secret_key = token_bytes(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite3'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    forms = db.relationship('Form', backref='User')


class Form(db.Model):
    __tablename__ = 'Form'
    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid4()))
    author_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    author = db.relationship('User', backref='Form')
    title = db.Column(db.Text, nullable=False)
    questions = db.Relationship('FormQuestion', backref='Form')


class FormQuestion(db.Model):
    __tablename__ = 'FormQuestion'
    __table_args__ = (
        db.PrimaryKeyConstraint('form_id', 'number'),
    )
    form_id = db.Column(db.Text, db.ForeignKey('Form.id'), nullable=False)
    form = db.relationship('Form', backref='FormQuestion')
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    required = db.Column(db.Boolean, nullable=False, default=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


def login_required(route):
    @wraps(route)
    def f(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        return route(*args, **kwargs)
    return f


@app.get('/form/list')
@login_required
def list_forms():
    forms = Form.query.filter(Form.author == current_user)
    return render_template('list_forms.html', forms=forms)


@app.route('/form/create', methods=['GET', 'POST'])
@login_required
def create_form():
    if request.method == 'GET':
        return render_template('create_form.html')

    try:
        title = request.form.get('title')
        questions = json.loads(request.form.get('questions', ''))
    except:
        title = None
        questions = None

    if title is None or type(questions) is not list or any(type(q) is not list or len(q) != 2 or type(q[0]) is not str or type(q[1]) is not bool for q in questions):
        return fail('create_form.html', 'Invalid request')

    if len(questions) == 0:
        return fail('create_form.html', 'Your form must consist of at least one question')

    form = Form(author=current_user, title=title)
    questions = [FormQuestion(form=form, number=i, content=q[0], required=q[1]) for i, q in enumerate(questions)]
    db.session.add(form)
    db.session.add_all(questions)
    db.session.commit()

    flash(f'Form with id {form.id} created', 'info')
    return render_template('create_form.html')


@app.route('/form/fill/<formid>', methods=['GET', 'POST'])
def fill_form(formid):
    try:
        formid = str(UUID(formid))
        form = Form.query.filter(Form.id == formid).first()
    except ValueError:
        form = None
    
    if form is None:
        return fail('index.html', 'Invalid form id')

    if request.method == 'GET':
        return render_template('fill_form.html', form=form, answers={})
    
    required_questions = [f'q_{q.number:02}' for q in form.questions if q.required]
    answers = {f'q_{i:02}': request.form.get(f'q_{i:02}', '') for i in range(len(form.questions))}

    for q in required_questions:
        i = int(q[2:])
        if len(answers[q]) == 0:
            return fail('fill_form.html', f'The following question is required: {form.questions[i].content}', {'form': form, 'answers': answers})
    
    # TODO: save the answers
    return render_template('thank_you.html')


@app.post('/form/ask/<formid>')
@login_required
def ask_admin(formid):
    try:
        formid = str(UUID(formid))
        form = Form.query.filter(Form.id == formid).first()
    except ValueError:
        return fail('index.html', 'Invalid form id')

    questions_to_fill = [f'q_{i:02}' for i in range(len(form.questions)) if request.form.get(f'q_{i:02}', False)]

    Thread(target=visit, args=(formid, questions_to_fill)).start()
    return render_template('admin_confirmation.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username')
    password = request.form.get('password')
    context = {'username': username, 'password': password}
    
    if username is None or password is None:
        return fail('register.html', 'Invalid request')

    if len(username) < 4:
        return fail('register.html', 'Username is too short', context)

    if len(password) < 8:
        return fail('register.html', 'Password is too short', context)
    
    if not username.isalnum():
        return fail('register.html', 'Username is not valid', context)

    if User.query.filter(User.username == username).count() != 0:
        return fail('register.html', 'User already exists', context)

    user = User(username=username, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    db.session.add(user)
    db.session.commit()

    flash('User registered', 'info')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    context = {'username': username, 'password': password}

    if username is None or password is None:
        return fail('login.html', 'Invalid request')

    user = User.query.filter(User.username == username).first()

    if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return fail('login.html', 'Invalid credentials', context)

    login_user(user)
    return redirect('/')


@app.get('/logout')
def logout():
    logout_user()
    return redirect('/')


def fail(template, message, context={}):
    flash(message, 'error')
    resp = Response(render_template(template, **context))
    resp.status_code = 400
    resp.content_type = 'text/html'
    return resp


@app.get('/')
def index():
    return render_template('index.html')
