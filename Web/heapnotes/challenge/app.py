from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import string
import os
import json
import zlib

FLAG = open("flag.txt").read().strip()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.secret_key = os.urandom(16)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.String(32), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

def encrypt(pt, key):
    ct = []
    for i in range(len(pt)):
        ct.append(pt[i] ^ key[i % len(key)])
    return bytes(ct)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.errorhandler(Exception)
def all_exception_handler(error):
   print(error)
   return render_template("index.html"), 200

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists! <a href=/>Return home</a>', 409

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return 'Registration successful! <a href=/login>Log in</a>'

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect("/")
        else:
            return 'Invalid credentials. <a href=/>Return home</a>', 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        key = os.urandom(16).hex()
        if "key" in request.form:
            key = request.form["key"]
        note_id = ''.join(random.choices(string.ascii_letters, k=32))
        content = request.form["content"]
        new_note = Note(note_id=note_id, user_id=current_user.username, content=content, key=key)
        db.session.add(new_note)
        db.session.commit()
        return note_id
    return render_template('create.html')

@app.route('/note/<note_id>')
@login_required
def view_note(note_id):
    note = Note.query.filter_by(note_id=note_id).first()
    key = note.key
    data = encrypt(zlib.compress(json.dumps({"username": current_user.username, "content": note.content}).encode()), bytes.fromhex(key)).hex()
    print(len(data))
    return redirect(url_for('render_note', data=data, key=key))

@app.route('/render/<data>/<key>')
@login_required
def render_note(data, key):
    if not data:
        return 'Invalid note', 404
    try:
        data = json.loads(zlib.decompress(encrypt(bytes.fromhex(data), bytes.fromhex(key))).decode())
    except:
        data = {"username": current_user.username, "content": "Error"}
    return render_template('note.html', note=data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        new_user = User(username=FLAG, password=FLAG)
        db.session.add(new_user)
        db.session.commit()
    app.run('0.0.0.0', port=443, ssl_context=('ssl/cert.pem', 'ssl/key.pem'))
