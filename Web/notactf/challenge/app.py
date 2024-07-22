from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, redirect
import pymongo
import flask_login
import hashlib
import requests
import flask
from httpcats import cat_by_code
from AesEverywhere import aes256
import binascii
import random
import ast
from base64 import decodebytes
from xorCryptPy import xorCrypt
from config import secret_key, aes_key, conn_string
#init flask app
app = Flask(__name__)
secretkey=secret_key
aeskey=aes_key
app.secret_key = str(secretkey)
#init mongodb
client = pymongo.MongoClient(conn_string)
db = client.Main
maindb = db["main"]
maindb.insert_one({"_id": "admin", "solved": [], "password": "fc894fcf8196a7366c758234902409ae83883096aa56717b436a23ed8af6d6f6", "points": "0"})
#variables
ctfname = "Not A CTF"
discordinvite = "https://discord.gg/wNnJKTtZGJ"
adminusername = "admin"
#init flask login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
class User(flask_login.UserMixin):
  pass

@login_manager.user_loader
def user_loader(username):

  users = []
  for doc in maindb.find():
    users.append(doc.get("_id"))
  if username not in users:
    return

  user = User()
  user.id = username
  return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    users = []
    for doc in maindb.find():
      users.append(doc.get("_id"))
    
    if username not in users:
      return

    user = User()
    user.id = username

    
    password = str(request.form['password']).encode()
    password = hashlib.sha256(password)
    password = password.hexdigest()
    password = str(password)

    for x in maindb.find({ "_id": str(username)}):
      userobj = x


    user.is_authenticated = password == str(userobj.get('password'))
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
  return redirect("/login")

#Start with flask
@app.route('/')
def tolink():
  #return render_template("post-login.html")
  return redirect('/home')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if flask.request.method == 'GET':
    return render_template("login.html")
  username = flask.request.form['username']
  users = []
  for doc in maindb.find():
    users.append(doc.get("_id"))

  if username not in users:
    return "That user does not exist. Create an account <a href='/register'>here</a>!"

  password = str(request.form['password']).encode()
  password = hashlib.sha256(password)
  password = password.hexdigest()
  password = str(password)

  for x in maindb.find({ "_id": str(username)}):
    userobj = x
    
    if password == userobj.get('password'):
      user = User()
      user.id = username
      flask_login.login_user(user)
      return flask.redirect(flask.url_for('home'))
    elif password != userobj.get('password'):
      return "Incorrect login information."
  return 'FATAL ERROR: CONTACT DEVELOPERS'


@app.route('/home')
@flask_login.login_required
def home():
  signed_id = hashlib.md5(flask_login.current_user.id.encode()).hexdigest() + flask_login.current_user.id
  authtoken = aes256.encrypt(signed_id, str(aeskey))
  authtoken = str(authtoken)
  authtoken = authtoken[:-1]
  authtoken = authtoken[2:]
  authtoken = xorCrypt(str(authtoken), 938123)
  authtoken = str(authtoken)
  authtoken = authtoken.encode("utf-8").hex()
  return render_template('home.html', username=flask_login.current_user.id, authtoken=authtoken)


@app.route('/logout')
@flask_login.login_required
def logout():
  flask_login.logout_user()
  return redirect('/')

@app.route('/register')
def register_render():
  return render_template('register.html')



@app.route('/register', methods=['POST'])
def register():
  username = request.form['username']
  passcheck = str(request.form['password'])
  
  if len(passcheck) > 20 or passcheck == "":
    return "Please use a supported browser! Supported browsers include the latest version of Firefox, Edge Chromium, Google Chrome, and Brave. If your using a supported browser, make sure JavaScript is enabled."

  password = str(request.form['password']).encode()
  password = hashlib.sha256(password)
  password = password.hexdigest()


  registerdata = {"_id": username, "solved": [], "password": password, "points": "0"}

  validchars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']

  for i in str(username):
    if not str(i) in validchars:
      return "Please use a supported browser! Supported browsers include the latest version of Firefox, Edge Chromium, Google Chrome, and Brave. If your using a supported browser, make sure JavaScript is enabled." 
    
  if len(username) > 20 or username == "":
    return "Please use a supported browser! Supported browsers include the latest version of Firefox, Edge Chromium, Google Chrome, and Brave. If your using a supported browser, make sure JavaScript is enabled."



  if 'success' == 'success':
    try:
      maindb.insert_one(registerdata)
      return f"Thanks for signing up for {ctfname}! Login into your new <a href='/login'>account here</a>!"

    except:
      return "ERROR: Username already exists."
  else:
    return "Please complete the captcha."

@app.route('/discord')
def discord():
  return redirect(discordinvite)

@app.route('/challenges')
def challenges():
  signed_id = hashlib.md5(flask_login.current_user.id.encode()).hexdigest() + flask_login.current_user.id
  authtoken = aes256.encrypt(signed_id, str(aeskey))
  authtoken = str(authtoken)
  authtoken = authtoken[:-1]
  authtoken = authtoken[2:]
  authtoken = xorCrypt(str(authtoken), 938123)
  authtoken = str(authtoken)
  authtoken = authtoken.encode("utf-8").hex()

  challs = open("challenges.txt", "r")
  challs = challs.read()
  challs = ast.literal_eval(challs)




  return render_template("challenges.html", challs=challs, authtoken=authtoken)


@app.route('/leaderboard')
@flask_login.login_required
def leaderboard():
  users = []
  all_users = []
  sorted_users = []
  final_users = []
  for doc in maindb.find():
    users.append(doc.get("_id"))
  users.remove('admin')
  for user in users:
    for x in maindb.find({ "_id": str(user)}):
      x["points"] = int(x.get('points'))

      all_users.append(x)
  sorted_users = sorted(all_users, key = lambda i: i['points'],reverse=True)
  
  for user in sorted_users:
    user['placement'] = int(sorted_users.index(user)) + 1
    final_users.append(user)
  
  signed_id = hashlib.md5(flask_login.current_user.id.encode()).hexdigest() + flask_login.current_user.id
  authtoken = aes256.encrypt(signed_id, str(aeskey))
  authtoken = str(authtoken)
  authtoken = authtoken[:-1]
  authtoken = authtoken[2:]
  authtoken = xorCrypt(str(authtoken), 938123)
  authtoken = str(authtoken)
  authtoken = authtoken.encode("utf-8").hex()



  return render_template('leaderboard.html', final_users=final_users, username=flask_login.current_user.id, authtoken=authtoken)

#admin panel
@app.route('/admin')
@flask_login.login_required
def admin():
  if flask_login.current_user.id != "admin":
    return "UNAUTHORIZED"
  elif flask_login.current_user.id == "admin":
    signed_id = hashlib.md5(flask_login.current_user.id.encode()).hexdigest() + flask_login.current_user.id
    authtoken = aes256.encrypt(signed_id, str(aeskey))
    authtoken = str(authtoken)
    authtoken = authtoken[:-1]
    authtoken = authtoken[2:]
    authtoken = xorCrypt(str(authtoken), 938123)
    authtoken = str(authtoken)
    authtoken = authtoken.encode("utf-8").hex()
    
    challconf = open("challenges.txt", "r")
    challconf = challconf.read()
    challconf = str(challconf)


    return render_template('admin.html', username=flask_login.current_user.id, authtoken=authtoken, challconf=challconf)

@app.route('/admin', methods=['POST'])
def admin_SS():
  user_auth = request.headers.get('user-auth-token')
  user_auth = bytes(user_auth, 'utf-8')
  user_auth=binascii.unhexlify(user_auth)
  user_auth = str(user_auth, "utf-8")
  user_auth = xorCrypt(str(user_auth), 938123)

  user = aes256.decrypt(user_auth, str(aeskey))
  user = user[32:].decode()

  #List of users
  users = []
  alluserobj = []
  if user != str(adminusername):
    return "UNAUTHORIZED"
  elif user == str(adminusername):

    action = request.headers.get('action')
    if action == "get-challenges":
      challconf = open("challenges.txt", "r")
      challconf = challconf.read()

      return str(challconf)





#Submit
@app.route('/submit', methods=['POST'])
def submit():
    flag = request.headers.get('submitted-flag')
    user_auth = request.headers.get('user-auth-token')
    #Making bytes
    user_auth = bytes(user_auth, 'utf-8')

    #unhexed
    user_auth=binascii.unhexlify(user_auth)

    user_auth = str(user_auth, "utf-8")
    user_auth = xorCrypt(str(user_auth), 938123)
    #decrypting AES
    user = aes256.decrypt(user_auth, str(aeskey))
    user = user[32:].decode()

    #whoknows
    challenges = open("challenges.txt", "r")
    challenges = challenges.read()
    challenges = ast.literal_eval(challenges)

    for potflag in challenges:
      if potflag.get('Valid') == flag:
        for userobj in maindb.find({ "_id": str(user)}):
          solved = userobj.get('solved')
          if potflag.get('Chall_Name') in solved:
            return f"You already solved {potflag.get('Chall_Name')}!"
          


          points = int(userobj.get('points'))
          points = points + int(potflag.get('Points'))

          newpoints = { "$set": { "points": str(points) } }

          maindb.update_one(userobj, newpoints)



          maindb.update({'_id': str(user)}, {'$push': {'solved': str(potflag.get('Chall_Name'))}})

        return f"You solved \"{str(potflag.get('Chall_Name'))}\" and got {str(potflag.get('Points'))} points!"

    return "Your flag was incorrect."

@app.route('/solves')
@flask_login.login_required
def solves():
  signed_id = hashlib.md5(flask_login.current_user.id.encode()).hexdigest() + flask_login.current_user.id
  authtoken = aes256.encrypt(signed_id, str(aeskey))
  authtoken = str(authtoken)
  authtoken = authtoken[:-1]
  authtoken = authtoken[2:]
  authtoken = xorCrypt(str(authtoken), 938123)
  authtoken = str(authtoken)
  authtoken = authtoken.encode("utf-8").hex()

  users = []
  challenges = open("challenges.txt", "r")
  challenges = challenges.read()
  challenges = ast.literal_eval(challenges)
  solved_challenges = []

  for doc in maindb.find():
    users.append(doc.get("_id"))
  users.remove('admin')
  for user in users:

    for x in maindb.find({ "_id": str(user)}):
      solved_by_user = list(x.get('solved'))
      for solved_challenge in solved_by_user:
        for dictionary in challenges:
          if str(dictionary.get('Chall_Name')) == str(solved_challenge):

            dict_of_solved = {"solved": str(solved_challenge), "solved_by": str(x.get('_id')), "points": str(dictionary.get('Points'))}
            solved_challenges.append(dict_of_solved)
  
  random.shuffle(solved_challenges)


  return render_template('solves.html', solved_challenges = solved_challenges, username=flask_login.current_user.id, authtoken=authtoken)


@app.route('/user_control', methods=['GET'])
def user_control():
  users = []
  for doc in maindb.find():
    users.append(str(doc.get("_id")))

  if str(request.headers.get('username')) in users:
    return "true"
  elif not str(request.headers.get('username')) in users:
    return "false"


@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
      my_cat = cat_by_code(int(e.code))
      code = str(e.code)
      cat = my_cat.url
      return render_template('error.html', code=code, cat=cat, error=my_cat.name)
 
app.run(host='0.0.0.0', port=80)

