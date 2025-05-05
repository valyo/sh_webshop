import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

# Import models
from .models import Season, Admin

# GitHub OAuth settings
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com/user'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

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
    app.config['GOOGLE_SHEET_ID'] = os.getenv('GOOGLE_SHEET_ID')

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Create database tables
    with app.app_context():
        db.create_all()
        print('Database tables created successfully!')

    # Import flask commands - all
    from sh_portal.commands import (
        create_new_admin
    )
    # Add flask commands - general
    app.cli.add_command(create_new_admin)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Register blueprints
    from sh_portal.home import main
    from sh_portal.andelsbiodling import andelsbiodling
    from sh_portal.lammandel import lammandel
    from sh_portal.admin import admin
    from sh_portal.products import products

    app.register_blueprint(main)
    app.register_blueprint(andelsbiodling)
    app.register_blueprint(lammandel)
    app.register_blueprint(admin)
    app.register_blueprint(products)

    return app