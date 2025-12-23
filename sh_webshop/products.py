from flask import Blueprint, render_template, session, abort
from .models import Product, Category

products = Blueprint("products", __name__)


@products.route("/produkter")
def index():
    all_products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    return render_template(
        "products/index.html",
        user=session.get("user"),
        page_title="Alla produkter",
        products=all_products,
    )


@products.route("/produkter/kategori/<slug>")
def by_category(slug):
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        abort(404)
    category_products = (
        Product.query.filter_by(category_id=category.id, is_active=True)
        .order_by(Product.name)
        .all()
    )
    return render_template(
        "products/index.html",
        user=session.get("user"),
        page_title=category.name,
        products=category_products,
        category=category,
    )


@products.route("/produkt/<slug>")
def detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if not product:
        abort(404)
    return render_template(
        "products/detail.html",
        user=session.get("user"),
        page_title=product.name,
        product=product,
    )
