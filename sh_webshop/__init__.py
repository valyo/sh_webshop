import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from .config import Config

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

# Import models
from .models import Admin

# GitHub OAuth settings
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com/user"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_cart_count():
    """Get the total number of items in the cart."""
    cart = session.get("cart", {})
    return sum(item["quantity"] for item in cart.values())


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    # Import flask commands - all
    from sh_webshop.commands import create_new_admin

    # Add flask commands - general
    app.cli.add_command(create_new_admin)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Register blueprints
    from .home import main
    from .biodling import biodling
    from .far_och_lamm import far_och_lamm
    from .admin import admin
    from .products import products
    from .about import about
    from .cart import cart

    app.register_blueprint(main)
    app.register_blueprint(biodling)
    app.register_blueprint(far_och_lamm)
    app.register_blueprint(admin)
    app.register_blueprint(products)
    app.register_blueprint(about)
    app.register_blueprint(cart)

    # Add template context processor
    @app.context_processor
    def inject_cart_count():
        return dict(cart_count=get_cart_count())

    return app
