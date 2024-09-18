# app/models.py

from app import db  # Importing SQLAlchemy database instance from app
from flask_login import UserMixin  # Importing UserMixin to integrate with Flask-Login
from app import login_manager  # Importing login manager for session handling

@login_manager.user_loader  # This decorator tells Flask-Login how to load a user from the user ID stored in the session
def load_user(user_id):
    # This function retrieves a user from the database using the user_id from the session
    return User.query.get(int(user_id))

# Defining the User model (the users table in the database)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column, unique for each user
    username = db.Column(db.String(100), unique=True, nullable=False)  # Username, must be unique and non-nullable
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email, must be unique and non-nullable
    password = db.Column(db.String(60), nullable=False)  # Password (hashed), non-nullable

# Defining the Post model (the posts table in the database)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column, unique for each post
    title = db.Column(db.String(100), nullable=False)  # Title of the post, cannot be null
    content = db.Column(db.Text, nullable=False)  # Content of the post, cannot be null
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key, linking to a user
    # Defining the relationship between the Post model and the User model
    user = db.relationship('User', backref='posts', lazy=True)  # Establishes a relationship with the User who authored the post

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for each comment
    content = db.Column(db.Text, nullable=False)  # The content of the comment
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key linking comment to a post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking comment to the author (user)
    post = db.relationship('Post', backref='comments', lazy=True)  # Establish a relationship with the Post model
    user = db.relationship('User', backref='comments', lazy=True)  # Establish a relationship with the User model
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())  # Timestamp for when the comment was made

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key linking like to a post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking like to the user
    post = db.relationship('Post', backref='likes', lazy=True)  # Relationship with Post model
    user = db.relationship('User', backref='likes', lazy=True)  # Relationship with User model