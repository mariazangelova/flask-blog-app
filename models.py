from flask_sqlalchemy import SQLAlchemy
#from app import db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    registered = db.Column(db.DateTime)
    posts = db.relationship("Post", backref='user')

    def __init__(self, first_name=None, last_name=None, email=None, password=None, registered=None, posts=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered = registered
        self.posts = posts
    def __repr__(self):
        return '<User %r>' % self.first_name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    categories = db.relationship("Category", secondary='categories', backref=db.backref('posts', lazy='dynamic'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    # posts = db.relationship("Post", secondary='categories')

categories_table = db.Table('categories', db.Model.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

if __name__ == "__main__":

    print("Creating database tables...")
    db.create_all()
    print("Done!")