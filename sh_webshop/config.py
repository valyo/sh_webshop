import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root (parent of sh_webshop package)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _default_shop_data_dir():
    return os.path.join(_PROJECT_ROOT, "instance")


def _sqlite_uri_absolute(db_path: str) -> str:
    """Build a SQLite URI with an absolute filesystem path (CWD-independent)."""
    abs_path = os.path.abspath(db_path)
    return "sqlite:///" + abs_path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    # All durable files (SQLite DB, uploaded images) live under this directory.
    _shop_data_env = os.getenv("SHOP_DATA_DIR", "").strip()
    SHOP_DATA_DIR = os.path.abspath(
        _shop_data_env if _shop_data_env else _default_shop_data_dir()
    )

    _database_url = os.getenv("DATABASE_URL", "").strip()
    SQLALCHEMY_DATABASE_URI = (
        _database_url
        if _database_url
        else _sqlite_uri_absolute(os.path.join(SHOP_DATA_DIR, "app.db"))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration (under SHOP_DATA_DIR, not under package static/)
    UPLOAD_FOLDER = os.path.join(SHOP_DATA_DIR, "uploads", "products")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # GitHub OAuth configuration
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_API_URL = "https://api.github.com/user"

    # Google Sheets configuration
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
