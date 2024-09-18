from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Set up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database file will be created in your project directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

db = SQLAlchemy(app)  # Initialize SQLAlchemy
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes