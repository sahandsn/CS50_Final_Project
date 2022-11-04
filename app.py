import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import zip_longest
from flask_login import login_required, current_user
from functools import wraps
from flask_mail import Mail, Message

# Configure application
app = Flask(__name__)
app.secret_key = '*,sanaei#9,#sahand%,!is@,here$?/,2001;'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Config Email
app.config["MAIL_PASSWORD"] = "hvlzzcohwfbcvcoj"
app.config["MAIL_PORT"] = 465
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "YourListsAndNotesApp@gmail.com"

mail = Mail(app)

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
db = SQL("sqlite:///tables.db")

# Different routes
@app.route("/error")
def error(message, code=400):
    return render_template('error.html', message=message), code


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        # DO NOT SAVE PASSWORD
        username = request.form.get('username')
        email = request.form.get('email')

        # check for errors
        if email == '':
            return error('enter email')
        if not username or username == '':
            return error("enter username")
        if not request.form.get('password') or request.form.get('password') == '':
            return error("enter password")
        if not request.form.get('confirmation') or request.form.get('confirmation') == '':
            return error("password not confirmed")
        if not request.form.get('confirmation') == request.form.get('password'):
            return error("password not confirmed")
        emails = db.execute("SELECT email FROM users")
        for dict in emails:
            if dict['email'] == email:
                return error("use a new email.")
        
        # check if the username is taken
        names = db.execute('SELECT username FROM users')

        for dict in names:
            for val in dict.values():
                if val == username:
                    return error("username is taken")

        # hash the password
        hashed = generate_password_hash(request.form.get('password'))

        try:
            # add user to the database
            db.execute('INSERT INTO users (username, hash, email) VALUES(?, ?, ?)', username, hashed, email)
        except:
            return error("something went wrong.")
        
        # msg = Message("YourList", sender = 'noreply@demo.com', recipients=[email])
        # msg.body = "Welcome to your ultimate List app online!"
        # mail.send(msg)
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))[0]['id']
        return redirect('/')

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
            return error("user not found.")

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
    used = []
    lists = []
    for dict in list:
        if dict['tag'] == 'urgent':
            urgents.append(dict)
        if dict['tag'] == 'entry':
            entries.append(dict)
        if dict['tag'] == 'done':
            used.append(dict)    
    lists[len(lists):] = urgents
    lists[len(lists):] = entries
    lists[len(lists):] = used

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
        email = db.execute("SELECT email FROM users WHERE id = ?", session["user_id"])
        # if email[0]['email'] == '':
        #     return redirect('/')
        # msg = Message("YourList", sender = 'noreply@demo.com', recipients=[email[0]['email']])
        # msg.body = "An entry has been added."
        # mail.send(msg)
        return redirect('/')
    else:
        return render_template('entry.html')


@app.route('/delete', methods=['POST'])
@login_required
def delete():

    list = db.execute('SELECT * FROM notes WHERE id = ?', request.form.get('delete')) 
    return render_template('delete.html', list=list)


@app.route('/validate deletion', methods=['post'])
@login_required
def validate():

    id = request.form.get('delete')
    return render_template('validate.html', id=id)
    
    
@app.route('/deleted', methods=['post'])
@login_required
def deleted():
    hash = db.execute('SELECT hash FROM users WHERE id = ?', session["user_id"])
    if check_password_hash(hash[0]['hash'] , request.form.get('password')) == True:
        id = request.form.get('delete')
        db.execute('DELETE FROM notes WHERE id = ?', id)
        # email = db.execute("SELECT email FROM users WHERE id = ?", session["user_id"])
        # if email[0]['email'] == '':
        #     return redirect('/')
        # msg = Message("YourList", sender = 'noreply@demo.com', recipients=[email[0]['email']])
        # msg.body = "An entry has been deleted."
        # mail.send(msg)
        return redirect('/')
    else:
        return error("password was wrong.")


@app.route('/urgentTag', methods=['post'])
@login_required
def urgent():
    id = request.form.get('urgent')
    db.execute('UPDATE notes SET tag = "urgent" WHERE id = ?', id)
    return redirect('/')


@app.route('/doneTag', methods=['post'])
@login_required
def done():
    id = request.form.get('done')
    db.execute('UPDATE notes SET tag = "done" WHERE id = ?', id)
    return redirect('/')


@app.route('/entryTag', methods=['post'])
@login_required
def entrytag():
    id = request.form.get('entry')
    db.execute('UPDATE notes SET tag = "entry" WHERE id = ?', id)
    return redirect('/')


@app.route("/email")
@login_required
def email():
    return render_template("email.html")


@app.route('/validate email', methods=['post'])
@login_required
def validateEmail():
    old = request.form.get("previousEmail")
    new = request.form.get("newEmail")
    check = db.execute("SELECT email FROM users WHERE id = ?", session['user_id'])[0]['email']
    if old == check:
        return render_template("validateEmail.html", old=old, new=new)
    else:
        return error("This is not your current email address.")


@app.route('/email change', methods=['post'])
@login_required
def changeEmail():
    hash = db.execute('SELECT hash FROM users WHERE id = ?', session["user_id"])
    if check_password_hash(hash[0]['hash'] , request.form.get('password')) == True:
        old = request.form.get("old")
        new = request.form.get("new")
        try:
            db.execute("UPDATE users SET email = ? WHERE id = ?", new, session['user_id'])
        except:
            return error("something went wrong.")
        return redirect('/')
    else:
        return error("password was wrong.")


fonts = ['sans-serif', "Audiowide", 'serif', "Sofia", 'monospace', 'cursive', 'fantasy', "Trirong"]
background = ['aaaaaa', '107895', '0d3c55', '0d3c55', '000000', 'fd852e', 'ffffff', '83174b']
foreground = ['000000', 'f1f3f4', 'f1f3f4', 'eed369', 'fd852e', '000000', '83174b', 'ffffff']
size = ['x-small', 'small', 'medium', 'large', 'x-large']

@app.route('/customize', methods=['get', 'post'])
@login_required
def customize():
    if request.method == 'post':
        return render_template('customize.html')
    else:
        return render_template('customize.html', fonts=fonts, background=background, foreground=foreground, size=size)


        