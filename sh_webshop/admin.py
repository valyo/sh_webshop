from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request,
    current_app,
)
from functools import wraps
from requests_oauthlib import OAuth2Session
from werkzeug.utils import secure_filename
from .models import Admin, AboutSection, Category, Product
from . import db
import re
import os
import uuid

admin = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            flash("Please log in to access this page.", "error")
            return render_template(
                "admin/dashboard.html", user=None, page_title="Admin Dashboard"
            )
        return f(*args, **kwargs)

    return decorated_function


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})


def save_product_image(file):
    """Save an uploaded product image and return the URL path."""
    if file and file.filename and allowed_file(file.filename):
        # Generate a unique filename to avoid collisions
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # Ensure upload folder exists
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if not upload_folder:
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'products')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save the file
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        return url_for("uploads.serve_product", filename=filename)
    return None


def _product_image_filename_from_url(image_url):
    """Return basename for a locally stored product image URL, or None."""
    if not image_url:
        return None
    for marker in ("/uploads/products/", "/static/uploads/products/"):
        if marker in image_url:
            name = image_url.split(marker)[-1].split("?", 1)[0]
            if name and name == os.path.basename(name) and ".." not in name:
                return name
    return None


def delete_product_image(image_url):
    """Delete a product image file if it's a local upload."""
    filename = _product_image_filename_from_url(image_url)
    if not filename:
        return False
    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    if not upload_folder:
        upload_folder = os.path.join(
            current_app.root_path, "static", "uploads", "products"
        )
    filepath = os.path.join(upload_folder, filename)
    legacy_path = os.path.join(
        current_app.root_path, "static", "uploads", "products", filename
    )
    for path in (filepath, legacy_path):
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except OSError:
                pass
    return False


def save_about_image(file):
    """Save an uploaded about-section image and return the URL path."""
    if file and file.filename and allowed_file(file.filename):
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_folder = current_app.config.get("ABOUT_UPLOAD_FOLDER")
        if not upload_folder:
            upload_folder = os.path.join(
                current_app.root_path, "static", "uploads", "about"
            )
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return url_for("uploads.serve_about", filename=filename)
    return None


def _about_image_filename_from_url(image_url):
    """Return basename for a locally stored about image URL, or None."""
    if not image_url:
        return None
    for marker in ("/uploads/about/", "/static/uploads/about/"):
        if marker in image_url:
            name = image_url.split(marker)[-1].split("?", 1)[0]
            if name and name == os.path.basename(name) and ".." not in name:
                return name
    return None


def delete_about_image(image_url):
    """Delete an about-section image file if it's a local upload."""
    filename = _about_image_filename_from_url(image_url)
    if not filename:
        return False
    upload_folder = current_app.config.get("ABOUT_UPLOAD_FOLDER")
    if not upload_folder:
        upload_folder = os.path.join(
            current_app.root_path, "static", "uploads", "about"
        )
    filepath = os.path.join(upload_folder, filename)
    legacy_path = os.path.join(
        current_app.root_path, "static", "uploads", "about", filename
    )
    for path in (filepath, legacy_path):
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except OSError:
                pass
    return False


@admin.route("/admin")
@login_required
def admin_dashboard():
    return render_template(
        "admin/dashboard.html", user=session.get("user"), page_title="Admin Dashboard"
    )


@admin.route("/admin/categories")
@login_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin/categories/index.html",
        user=session.get("user"),
        categories=categories,
        page_title="Manage Categories",
    )


@admin.route("/admin/categories/create", methods=["GET", "POST"])
@login_required
def create_category():
    if request.method == "POST":
        name = request.form.get("name")
        slug = request.form.get("slug")
        description = request.form.get("description")

        if not name:
            flash("Category name is required.", "error")
            return redirect(url_for("admin.create_category"))

        # Create slug from name if not provided
        if not slug:
            slug = slugify(name)
        else:
            slug = slugify(slug)

        # Check if slug already exists
        if Category.query.filter_by(slug=slug).first():
            flash("A category with this name or slug already exists.", "error")
            return redirect(url_for("admin.create_category"))

        category = Category(name=name, slug=slug, description=description)

        try:
            db.session.add(category)
            db.session.commit()
            flash("Category created successfully!", "success")
            return redirect(url_for("admin.categories"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the category.", "error")
            current_app.logger.error(f"Error creating category: {str(e)}")

    return render_template(
        "admin/categories/create.html",
        user=session.get("user"),
        page_title="Create Category",
    )


@admin.route("/admin/categories/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        slug = request.form.get("slug")
        description = request.form.get("description")

        if not name:
            flash("Category name is required.", "error")
            return redirect(url_for("admin.edit_category", id=id))

        # Create slug from name
        if not slug:
            slug = slugify(name)
        else:
            slug = slugify(slug)

        # Check if slug already exists (excluding current category)
        existing = Category.query.filter_by(slug=slug).first()
        if existing and existing.id != id:
            flash("A category with this name or slug already exists.", "error")
            return redirect(url_for("admin.edit_category", id=id))

        category.name = name
        category.slug = slug
        category.description = description

        try:
            db.session.commit()
            flash("Category updated successfully!", "success")
            return redirect(url_for("admin.categories"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the category.", "error")
            current_app.logger.error(f"Error updating category: {str(e)}")

    return render_template(
        "admin/categories/edit.html",
        user=session.get("user"),
        category=category,
        page_title="Edit Category",
    )


@admin.route("/admin/categories/<int:id>/delete", methods=["POST"])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)

    try:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the category.", "error")
        current_app.logger.error(f"Error deleting category: {str(e)}")

    return redirect(url_for("admin.categories"))


@admin.route("/admin/products")
@login_required
def products():
    products = Product.query.order_by(Product.name).all()
    return render_template(
        "admin/products/list.html",
        user=session.get("user"),
        products=products,
        page_title="Manage Products",
    )


@admin.route("/admin/products/create", methods=["GET", "POST"])
@login_required
def create_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        long_description = request.form.get("long_description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        category_id = request.form.get("category_id")
        is_active = bool(request.form.get("is_active"))

        if not all([name, price, category_id]):
            flash("Name, price, and category are required.", "error")
            return redirect(url_for("admin.create_product"))

        try:
            price = float(price)
            stock = int(stock) if stock else 0
        except ValueError:
            flash("Price and stock must be valid numbers.", "error")
            return redirect(url_for("admin.create_product"))

        # Create slug from name
        slug = slugify(name)

        # Check if slug already exists
        if Product.query.filter_by(slug=slug).first():
            flash("A product with this name already exists.", "error")
            return redirect(url_for("admin.create_product"))

        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url = save_product_image(file)
                if not image_url:
                    flash("Invalid image file. Please upload PNG, JPG, GIF, or WebP.", "error")
                    return redirect(url_for("admin.create_product"))

        product = Product(
            name=name,
            slug=slug,
            description=description,
            long_description=long_description,
            price=price,
            stock=stock,
            category_id=category_id,
            image_url=image_url,
            is_active=is_active,
        )

        try:
            db.session.add(product)
            db.session.commit()
            flash("Product created successfully!", "success")
            return redirect(url_for("admin.products"))
        except Exception as e:
            db.session.rollback()
            # Clean up uploaded image if database save fails
            if image_url:
                delete_product_image(image_url)
            flash("An error occurred while creating the product.", "error")
            current_app.logger.error(f"Error creating product: {str(e)}")

    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin/products/create.html",
        user=session.get("user"),
        categories=categories,
        page_title="Create Product",
    )


@admin.route("/admin/products/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        long_description = request.form.get("long_description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        category_id = request.form.get("category_id")
        remove_image = request.form.get("remove_image")
        is_active = bool(request.form.get("is_active"))

        if not all([name, price, category_id]):
            flash("Name, price, and category are required.", "error")
            return redirect(url_for("admin.edit_product", id=id))

        try:
            price = float(price)
            stock = int(stock) if stock else 0
        except ValueError:
            flash("Price and stock must be valid numbers.", "error")
            return redirect(url_for("admin.edit_product", id=id))

        # Create slug from name
        slug = slugify(name)

        # Check if slug already exists (excluding current product)
        existing = Product.query.filter_by(slug=slug).first()
        if existing and existing.id != id:
            flash("A product with this name already exists.", "error")
            return redirect(url_for("admin.edit_product", id=id))

        # Handle image removal
        old_image_url = product.image_url
        if remove_image:
            delete_product_image(old_image_url)
            product.image_url = None
            old_image_url = None  # Don't delete again if new upload fails

        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                new_image_url = save_product_image(file)
                if new_image_url:
                    # Delete old image if it exists and is a local upload
                    if old_image_url:
                        delete_product_image(old_image_url)
                    product.image_url = new_image_url
                else:
                    flash("Invalid image file. Please upload PNG, JPG, GIF, or WebP.", "error")
                    return redirect(url_for("admin.edit_product", id=id))

        product.name = name
        product.slug = slug
        product.description = description
        product.long_description = long_description
        product.price = price
        product.stock = stock
        product.category_id = category_id
        product.is_active = is_active

        try:
            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for("admin.products"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the product.", "error")
            current_app.logger.error(f"Error updating product: {str(e)}")

    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin/products/edit.html",
        user=session.get("user"),
        product=product,
        categories=categories,
        page_title="Edit Product",
    )


@admin.route("/admin/products/<int:id>/delete", methods=["POST"])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    image_url = product.image_url

    try:
        db.session.delete(product)
        db.session.commit()
        # Delete the image file after successful database deletion
        if image_url:
            delete_product_image(image_url)
        flash("Product deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the product.", "error")
        current_app.logger.error(f"Error deleting product: {str(e)}")

    return redirect(url_for("admin.products"))


@admin.route("/admin/about")
@login_required
def about_sections():
    sections = AboutSection.query.order_by(
        AboutSection.sort_order, AboutSection.id
    ).all()
    return render_template(
        "admin/about/list.html",
        user=session.get("user"),
        sections=sections,
        page_title="Manage About Page",
    )


@admin.route("/admin/about/create", methods=["GET", "POST"])
@login_required
def create_about_section():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        sort_order = request.form.get("sort_order")
        is_active = bool(request.form.get("is_active"))

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("admin.create_about_section"))

        try:
            sort_order = int(sort_order) if sort_order not in (None, "") else 0
        except ValueError:
            flash("Sort order must be a valid number.", "error")
            return redirect(url_for("admin.create_about_section"))

        image_url = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename:
                image_url = save_about_image(file)
                if not image_url:
                    flash(
                        "Invalid image file. Please upload PNG, JPG, GIF, or WebP.",
                        "error",
                    )
                    return redirect(url_for("admin.create_about_section"))

        section = AboutSection(
            title=title,
            content=content,
            image_url=image_url,
            sort_order=sort_order,
            is_active=is_active,
        )

        try:
            db.session.add(section)
            db.session.commit()
            flash("About section created successfully!", "success")
            return redirect(url_for("admin.about_sections"))
        except Exception as e:
            db.session.rollback()
            if image_url:
                delete_about_image(image_url)
            flash("An error occurred while creating the about section.", "error")
            current_app.logger.error(f"Error creating about section: {str(e)}")

    return render_template(
        "admin/about/create.html",
        user=session.get("user"),
        page_title="Create About Section",
    )


@admin.route("/admin/about/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_about_section(id):
    section = AboutSection.query.get_or_404(id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        sort_order = request.form.get("sort_order")
        remove_image = request.form.get("remove_image")
        is_active = bool(request.form.get("is_active"))

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("admin.edit_about_section", id=id))

        try:
            sort_order = int(sort_order) if sort_order not in (None, "") else 0
        except ValueError:
            flash("Sort order must be a valid number.", "error")
            return redirect(url_for("admin.edit_about_section", id=id))

        old_image_url = section.image_url
        if remove_image:
            delete_about_image(old_image_url)
            section.image_url = None
            old_image_url = None

        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename:
                new_image_url = save_about_image(file)
                if new_image_url:
                    if old_image_url:
                        delete_about_image(old_image_url)
                    section.image_url = new_image_url
                else:
                    flash(
                        "Invalid image file. Please upload PNG, JPG, GIF, or WebP.",
                        "error",
                    )
                    return redirect(url_for("admin.edit_about_section", id=id))

        section.title = title
        section.content = content
        section.sort_order = sort_order
        section.is_active = is_active

        try:
            db.session.commit()
            flash("About section updated successfully!", "success")
            return redirect(url_for("admin.about_sections"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the about section.", "error")
            current_app.logger.error(f"Error updating about section: {str(e)}")

    return render_template(
        "admin/about/edit.html",
        user=session.get("user"),
        section=section,
        page_title="Edit About Section",
    )


@admin.route("/admin/about/<int:id>/delete", methods=["POST"])
@login_required
def delete_about_section(id):
    section = AboutSection.query.get_or_404(id)
    image_url = section.image_url

    try:
        db.session.delete(section)
        db.session.commit()
        if image_url:
            delete_about_image(image_url)
        flash("About section deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the about section.", "error")
        current_app.logger.error(f"Error deleting about section: {str(e)}")

    return redirect(url_for("admin.about_sections"))


@admin.route("/login")
def login():
    github = OAuth2Session(
        current_app.config["GITHUB_CLIENT_ID"],
        scope=["read:user"],
        redirect_uri=url_for("admin.callback", _external=True),
    )
    authorization_url, state = github.authorization_url(
        current_app.config["GITHUB_AUTHORIZE_URL"]
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@admin.route("/callback")
def callback():
    github = OAuth2Session(
        current_app.config["GITHUB_CLIENT_ID"],
        state=session["oauth_state"],
        redirect_uri=url_for("admin.callback", _external=True),
    )
    token = github.fetch_token(
        current_app.config["GITHUB_TOKEN_URL"],
        client_secret=current_app.config["GITHUB_CLIENT_SECRET"],
        authorization_response=request.url,
    )

    github = OAuth2Session(current_app.config["GITHUB_CLIENT_ID"], token=token)
    user_data = github.get(current_app.config["GITHUB_API_URL"]).json()

    # Check if user is an admin
    admin = Admin.query.filter_by(github_id=user_data["id"]).first()
    if admin:
        session["user"] = {
            "id": user_data["id"],
            "username": user_data["login"],
            "avatar_url": user_data["avatar_url"],
        }
        flash("Successfully logged in!", "success")
        return redirect(url_for("admin.admin_dashboard"))
    else:
        flash("You are not authorized to access this system.", "error")
        return redirect(url_for("admin.admin_dashboard"))


@admin.route("/logout")
def logout():
    session.pop("user", None)
    flash("Successfully logged out!", "success")
    return redirect(url_for("admin.admin_dashboard"))
