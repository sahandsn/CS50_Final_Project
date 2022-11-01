import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import zip_longest
from flask_login import login_required, current_user
from functools import wraps

# Configure application
app = Flask(__name__)
app.secret_key = '*,sanaei#9,#sahand%,!is@,here$?/,2001;'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Config login decorator
def login_required(f):
   """
   Decorate routes to require login.
   http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
   """
   @wraps(f)
   def decorated_function(*args, **kwargs):
       if session.get("user_id") is None:
           return redirect("/login")
       return f(*args, **kwargs)
   return decorated_function

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Different routes
@app.route("/error")
def error(message):
    return render_template('error.html', message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        # DO NOT SAVE PASSWORD
        username = request.form.get('username')

        # check for errors
        if not username or username == '':
            return error("enter username")
        if not request.form.get('password') or request.form.get('password') == '':
            return error("enter password")
        if not request.form.get('confirmation') or request.form.get('confirmation') == '':
            return error("password not confirmed")
        if not request.form.get('confirmation') == request.form.get('password'):
            return error("password not confirmed")

        # check if the username is taken
        names = db.execute('SELECT username FROM users')

        for dict in names:
            for val in dict.values():
                if val == username:
                    return error("username is taken")

        # hash the password
        hashed = generate_password_hash(request.form.get('password'))

        # add user to the database
        db.execute('INSERT INTO users (username, hash) VALUES(?, ?)', username, hashed)

        return render_template('login.html')

    if request.method == 'GET':
        return render_template("register.html")
  

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("enter username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return error("enter password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("password not confirmed")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
@login_required
def index():
    # get this user's entries and 
    list = db.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY time DESC', session['user_id'])
    # sort them in time order: urgent->entry->done
    urgents = []
    entries = []
    dones = []
    lists = []
    for dict in list:
        if dict['tag'] == 'urgent':
            urgents.append(dict)
        if dict['tag'] == 'entry':
            entries.append(dict)
        if dict['tag'] == 'done':
            dones.appned(dict)      
    lists[len(lists):] = urgents
    lists[len(lists):] = entries
    lists[len(lists):] = dones

    return render_template('index.html', list=lists)


@app.route('/entry', methods=['POST', 'GET'])
@login_required
def entry():
    if request.method == 'POST':
        # if the tag is not defined
        if request.form.get('tag') not in ['urgent', 'entry']:
            return error('invalid entry')
        # insert the new entry in the notes table
        db.execute("INSERT INTO notes (user_id, head, body, tag) VALUES (?,?,?,?)", session["user_id"], request.form.get('head'), request.form.get('body'), request.form.get('tag'))
        return redirect('/')
    else:
        return render_template('entry.html')


@app.route('/delete', methods=['post'])
@login_required
def delete():

    id = request.form.get('delete')
    db.execute('DELETE FROM notes WHERE id = ?', id)
    return redirect('/')


@app.route('/check', methods=['POST'])
@login_required
def check():

    list = db.execute('SELECT * FROM notes WHERE id = ?', request.form.get('delete')) 
    return render_template('check.html', list=list)


