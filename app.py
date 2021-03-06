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
from models import db, User, Post, Category, categories_table

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = "secret key"

#db = SQLAlchemy(app)

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

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/", methods=['GET'])
@app.route('/posts')
@app.route("/<int:page>", methods=['GET'])
def index(page=1):
    #posts = Post.query.join(User).order_by(desc(Post.date_posted)).all() 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page,per_page=5,error_out=False)
    categories = Category.query.all()
    return render_template("index.html", posts=posts, categories=categories)

@app.route('/search', methods=["GET", "POST"])
@app.route('/search/<int:page>', methods=["GET", "POST"])
def search(page=1):
    word = request.form.get("word")
    posts = Post.query.filter(Post.content.contains(word)).paginate(page,per_page=5,error_out=False)
    categories = Category.query.all()
    return render_template("index.html", posts=posts, categories=categories, word=word)

@app.route("/posts/<category>/<int:page>", methods=["GET", "POST"])
@app.route("/posts/<category>", methods=["GET", "POST"])
def categories(category, page=1):
    posts = Post.query.join(User).filter(Post.categories.any(title=category)).order_by(desc(Post.date_posted)).paginate(page,per_page=5,error_out=False)
    allcategories = Category.query.all()
    return render_template("index.html", posts=posts, categories=allcategories, category=category)

@app.route("/myprofile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    posts = Post.query.join(User).filter(Post.user.has(id=user_id)).order_by(desc(Post.date_posted))
    allcategories = Category.query.all()
    return render_template("profile.html", user=user, posts=posts, categories=allcategories)

@app.route("/editprofile", methods=["POST"])
@login_required
def editprofile():
    data = request.get_json("value")
    if not data["value"]:
        return "Client error - no data", 400
    user = User.query.filter_by(id=session.get("user_id")).first()
    if data["type"] == "password":
        new_password = data["value"]
        new_hash = generate_password_hash(new_password)
        user.password = new_hash
    else: 
        new_email = data["value"]
        user.email = new_email
    db.session.commit()
    return "Profile edited successfully", 200

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return "No email", 400

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "No password", 400

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
            raise ValueError(error)
        
        # Check is email is already taken
        is_new = User.query.filter_by(email=email).all()
        if is_new:
            error = "This email has been already registered."
            raise ValueError(error)

        # Ensure password was submitted
        if not password:
            error = "Please provide a password"
            raise ValueError(error)

        # Check if password is long enough, has a letter and a number init
        elif len(password) < 5:
            error = "Password must be at least 5 characters long."
            raise ValueError(error)
        elif re.search('[0-9]', password) is None:
            error = "Password must have a number."
            raise ValueError(error)
        elif re.search('[A-Z]', password) is None:
            error = "Password must have at least one capital letter."
            raise ValueError(error)

        # Ensure the user writes correct password confirmation
        if not password == request.form.get("confirm_password"):
            error = "Passwords do not match"
            raise ValueError(error)

        # Hash the password
        hash = generate_password_hash(password)

        # Insert user into the database
        user = User(first_name=first_name, last_name=last_name, email=email, password=hash, registered=datetime.now(), posts=[])
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        flash('You successfully signed up')
        return redirect("/")
      except ValueError as error:
         return render_template("register.html", error=error)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route('/post/<id>')
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first()
    author = User.query.filter_by(id=post.author).first()
    return render_template("post.html", post=post, author=author)

@app.route('/post/delete/<id>')
@login_required
def delete_post(id):
    post = db.session.query(Post).get(id)
    post.categories = []
    #Post.query.filter_by(id=id).delete()
    db.session.delete(post)
    db.session.commit()
    return redirect("/myprofile")

@app.route('/add-post', methods=["GET", "POST"])
@login_required
def add_post():
    if request.method == "POST":
        error = None
        try:
            # Store post data
            title = request.form.get("title")
            subtitle = request.form.get("subtitle")
            content = request.form.get("content")
            author = session.get("user_id")
            cats = request.form.getlist("category")

            if not title or not content:
                error = "Post must have a title and some content."
                raise ValueError(error)

            # Create a new post with categories
            post = Post(title=title, subtitle=subtitle, content=content, author=author, date_posted=datetime.now())
            db.session.add(post)
            db.session.flush()
            db.session.refresh(post)
            for cat in cats:
                db.session.connection().execute(categories_table.insert().values(post_id=post.id, category_id=cat))
            db.session.commit()
        except ValueError as error:
            return render_template("post_form.html", error=error)
        author_data = User.query.filter_by(id=post.author).first()
        return render_template("post.html", post=post, author=author_data)
    else:
        # category = Category(title="technology")
        # db.session.add(category)
        #Category.query.filter_by(id=4).delete()
        #db.session.commit()
        categ = Category.query.all()
        return render_template("post_form.html", categories=categ)

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')

