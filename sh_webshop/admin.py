from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
from functools import wraps
from requests_oauthlib import OAuth2Session
from .models import Admin, Category, Product
from . import db
import re

admin = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Please log in to access this page.', 'error')
            return render_template(
                'admin/dashboard.html',
                user=None,
                page_title="Admin Dashboard"
            )
        return f(*args, **kwargs)
    return decorated_function

def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text

@admin.route('/admin')
@login_required
def admin_dashboard():
    return render_template(
        'admin/dashboard.html',
        user=session.get('user'),
        page_title="Admin Dashboard"
    )

@admin.route('/admin/categories')
@login_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'admin/categories/index.html',
        user=session.get('user'),
        categories=categories,
        page_title="Manage Categories"
    )

@admin.route('/admin/categories/create', methods=['GET', 'POST'])
@login_required
def create_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Category name is required.', 'error')
            return redirect(url_for('admin.create_category'))
        
        # Create slug from name
        slug = slugify(name)
        
        # Check if slug already exists
        if Category.query.filter_by(slug=slug).first():
            flash('A category with this name already exists.', 'error')
            return redirect(url_for('admin.create_category'))
        
        category = Category(
            name=name,
            slug=slug,
            description=description
        )
        
        try:
            db.session.add(category)
            db.session.commit()
            flash('Category created successfully!', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the category.', 'error')
            current_app.logger.error(f"Error creating category: {str(e)}")
    
    return render_template(
        'admin/categories/create.html',
        user=session.get('user'),
        page_title="Create Category"
    )

@admin.route('/admin/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Category name is required.', 'error')
            return redirect(url_for('admin.edit_category', id=id))
        
        # Create slug from name
        slug = slugify(name)
        
        # Check if slug already exists (excluding current category)
        existing = Category.query.filter_by(slug=slug).first()
        if existing and existing.id != id:
            flash('A category with this name already exists.', 'error')
            return redirect(url_for('admin.edit_category', id=id))
        
        category.name = name
        category.slug = slug
        category.description = description
        
        try:
            db.session.commit()
            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the category.', 'error')
            current_app.logger.error(f"Error updating category: {str(e)}")
    
    return render_template(
        'admin/categories/edit.html',
        user=session.get('user'),
        category=category,
        page_title="Edit Category"
    )

@admin.route('/admin/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the category.', 'error')
        current_app.logger.error(f"Error deleting category: {str(e)}")
    
    return redirect(url_for('admin.categories'))

@admin.route('/admin/products')
@login_required
def products():
    products = Product.query.order_by(Product.name).all()
    return render_template(
        'admin/products/list.html',
        user=session.get('user'),
        products=products,
        page_title="Manage Products"
    )

@admin.route('/admin/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        long_description = request.form.get('long_description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        image_url = request.form.get('image_url')
        is_active = bool(request.form.get('is_active'))
        
        if not all([name, price, category_id]):
            flash('Name, price, and category are required.', 'error')
            return redirect(url_for('admin.create_product'))
        
        try:
            price = float(price)
            stock = int(stock) if stock else 0
        except ValueError:
            flash('Price and stock must be valid numbers.', 'error')
            return redirect(url_for('admin.create_product'))
        
        # Create slug from name
        slug = slugify(name)
        
        # Check if slug already exists
        if Product.query.filter_by(slug=slug).first():
            flash('A product with this name already exists.', 'error')
            return redirect(url_for('admin.create_product'))
        
        product = Product(
            name=name,
            slug=slug,
            description=description,
            long_description=long_description,
            price=price,
            stock=stock,
            category_id=category_id,
            image_url=image_url,
            is_active=is_active
        )
        
        try:
            db.session.add(product)
            db.session.commit()
            flash('Product created successfully!', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the product.', 'error')
            current_app.logger.error(f"Error creating product: {str(e)}")
    
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'admin/products/create.html',
        user=session.get('user'),
        categories=categories,
        page_title="Create Product"
    )

@admin.route('/admin/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        long_description = request.form.get('long_description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        image_url = request.form.get('image_url')
        is_active = bool(request.form.get('is_active'))
        
        if not all([name, price, category_id]):
            flash('Name, price, and category are required.', 'error')
            return redirect(url_for('admin.edit_product', id=id))
        
        try:
            price = float(price)
            stock = int(stock) if stock else 0
        except ValueError:
            flash('Price and stock must be valid numbers.', 'error')
            return redirect(url_for('admin.edit_product', id=id))
        
        # Create slug from name
        slug = slugify(name)
        
        # Check if slug already exists (excluding current product)
        existing = Product.query.filter_by(slug=slug).first()
        if existing and existing.id != id:
            flash('A product with this name already exists.', 'error')
            return redirect(url_for('admin.edit_product', id=id))
        
        product.name = name
        product.slug = slug
        product.description = description
        product.long_description = long_description
        product.price = price
        product.stock = stock
        product.category_id = category_id
        product.image_url = image_url
        product.is_active = is_active
        
        try:
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the product.', 'error')
            current_app.logger.error(f"Error updating product: {str(e)}")
    
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'admin/products/edit.html',
        user=session.get('user'),
        product=product,
        categories=categories,
        page_title="Edit Product"
    )

@admin.route('/admin/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the product.', 'error')
        current_app.logger.error(f"Error deleting product: {str(e)}")
    
    return redirect(url_for('admin.products'))

@admin.route('/login')
def login():
    github = OAuth2Session(
        current_app.config['GITHUB_CLIENT_ID'],
        scope=['read:user'],
        redirect_uri=url_for('admin.callback', _external=True)
    )
    authorization_url, state = github.authorization_url(
        current_app.config['GITHUB_AUTHORIZE_URL']
    )
    session['oauth_state'] = state
    return redirect(authorization_url)

@admin.route('/callback')
def callback():
    github = OAuth2Session(
        current_app.config['GITHUB_CLIENT_ID'],
        state=session['oauth_state'],
        redirect_uri=url_for('admin.callback', _external=True)
    )
    token = github.fetch_token(
        current_app.config['GITHUB_TOKEN_URL'],
        client_secret=current_app.config['GITHUB_CLIENT_SECRET'],
        authorization_response=request.url
    )
    
    github = OAuth2Session(
        current_app.config['GITHUB_CLIENT_ID'],
        token=token
    )
    user_data = github.get(current_app.config['GITHUB_API_URL']).json()
    
    # Check if user is an admin
    admin = Admin.query.filter_by(github_id=user_data['id']).first()
    if admin:
        session['user'] = {
            'id': user_data['id'],
            'username': user_data['login'],
            'avatar_url': user_data['avatar_url']
        }
        flash('Successfully logged in!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    else:
        flash('You are not authorized to access this system.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('admin.admin_dashboard')) 