from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import join
from sqlalchemy import desc


import re
from datetime import datetime

from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required
from models import db, User, Post, Category

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#app.config['SECRET_KEY'] = "secret key"

db.init_app(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    posts = Post.query.join(User).order_by(desc(Post.date_posted)).all()
    categories = Category.query.all()
    return render_template("index.html", posts=posts, categories=categories)

@app.route('/posts')
def posts():
    posts = Post.query.join(User).order_by(desc(Post.date_posted)).all()
    categories = Category.query.all()
    return render_template("index.html", posts=posts, categories=categories)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            print("No email")

        # Ensure password was submitted
        elif not request.form.get("password"):
            print("No password")

        # Query database for username
        email=request.form.get("email")
        user = User.query.filter_by(email=email).all()
        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0].password, request.form.get("password")):
            error="No such user or wrong password."
            return render_template("login.html", error=error)

        # Remember which user has logged in
        session["user_id"] = user[0].id

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
      error = None
      try:
        # Store user data
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # Ensure username was submitted
        if not email:
            error = "Please provide an email"
            return render_template("register.html", error=error)
        
        # # Check is username is already taken
        # is_new = "CHECK DATABASE"
        # if is_new:
        #     print("Not a new username")

        # Ensure password was submitted
        if not password:
            print("No passowrd")

        # Check if password is long enough, has a letter and a number init
        elif len(password) < 5:
            print("Password has less than 5 charecters.")
        elif re.search('[0-9]', password) is None:
            print("Passowrd must have a number.")
        elif re.search('[A-Z]', password) is None:
            print("Password must have at least one capital letter.")

        # Ensure the user writes correct password confirmation
        if not password == request.form.get("confirm_password"):
            print("Passwords are not matching")

        # Hash the password
        hash = generate_password_hash(password)

        # Insert user into the database
        user = User(first_name=first_name, last_name=last_name, email=email, password=hash, registered=datetime.now(), posts=[])
        db.session.add(user)
        db.session.commit()
      except:
         error = "Something went wrong"
         return render_template("register.html", error=error)
      finally:
         flash('You successfully signed up')
         return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route('/post/<id>')
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first()
    author = User.query.filter_by(id=post.author).first()
    return render_template("post.html", post=post, author=author)

@app.route('/add-post', methods=["GET", "POST"])
@login_required
def add_post():
    if request.method == "POST":
        try:
            # Store post data
            title = request.form.get("title")
            subtitle = request.form.get("subtitle")
            content = request.form.get("content")
            author = session.get("user_id")

            # Create a new post
            post = Post(title=title, subtitle=subtitle, content=content, author=author, date_posted=datetime.now())
            db.session.add(post)
            db.session.commit()
        except:
            error = "Something went wrong."
            return render_template("post_form.html", error=error)
        author_data = User.query.filter_by(id=post.author).first()
        return render_template("post.html", post=post, author=author_data)
    else:
        return render_template("post_form.html")


# # Create a router for displaying a list of signed up users for an easy check
@app.route('/users')
@login_required
def users():
    users = User.query.all()
    print(users)
    return render_template("list.html", users=users)

if __name__ == '__main__':
   app.run(debug = True)

