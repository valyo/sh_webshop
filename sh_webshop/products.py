from flask import Blueprint, render_template, session
from .models import Product

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
