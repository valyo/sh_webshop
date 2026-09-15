import os

from flask import Blueprint, abort, current_app, send_from_directory
from werkzeug.utils import secure_filename

uploads_bp = Blueprint("uploads", __name__)


def _allowed_image_filename(filename: str) -> bool:
    if not filename or filename != os.path.basename(filename):
        return False
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    allowed = current_app.config.get(
        "ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "gif", "webp"}
    )
    return ext in allowed


def _serve_upload(folder_key: str, filename: str):
    safe = secure_filename(filename)
    if not safe or safe != filename or not _allowed_image_filename(safe):
        abort(404)
    folder = current_app.config.get(folder_key)
    if not folder:
        abort(404)
    filepath = os.path.join(folder, safe)
    if not os.path.isfile(filepath):
        abort(404)
    return send_from_directory(folder, safe)


@uploads_bp.route("/uploads/products/<filename>")
def serve_product(filename):
    """Serve product images from UPLOAD_FOLDER (bind-mount friendly)."""
    return _serve_upload("UPLOAD_FOLDER", filename)


@uploads_bp.route("/uploads/about/<filename>")
def serve_about(filename):
    """Serve about-page images from ABOUT_UPLOAD_FOLDER."""
    return _serve_upload("ABOUT_UPLOAD_FOLDER", filename)
