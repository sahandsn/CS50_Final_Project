import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import zip_longest
from flask_login import login_required
from functools import wraps

# Configure application
app = Flask(__name__)
app.secret_key = 'sanaeisahand'

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


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        # DO NOT SAVE PASSWORD
        username = request.form.get('username')

        # check for errors
        if not username or username == '':
            return render_template("error.html")
        if not request.form.get('password') or request.form.get('password') == '':
            return render_template("error.html")
        if not request.form.get('confirmation') or request.form.get('confirmation') == '':
            return render_template("error.html")
        if not request.form.get('confirmation') == request.form.get('password'):
            return render_template("error.html")

        # check if the username is taken
        names = db.execute('SELECT username FROM users')

        for dict in names:
            for val in dict.values():
                if val == username:
                    return render_template("error.html")

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
            return render_template("error.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html")

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
    return render_template('todo.html')