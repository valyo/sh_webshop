import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()

# GitHub OAuth settings
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com/user'

def create_app():
    app = Flask(__name__)

    # Configure the Flask application using environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # GitHub OAuth configuration
    app.config['GITHUB_CLIENT_ID'] = GITHUB_CLIENT_ID
    app.config['GITHUB_CLIENT_SECRET'] = GITHUB_CLIENT_SECRET
    app.config['GITHUB_AUTHORIZE_URL'] = GITHUB_AUTHORIZE_URL
    app.config['GITHUB_TOKEN_URL'] = GITHUB_TOKEN_URL
    app.config['GITHUB_API_URL'] = GITHUB_API_URL

    db.init_app(app)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    from sh_portal.routes import main
    app.register_blueprint(main)

    return app 