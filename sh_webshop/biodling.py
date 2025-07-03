from flask import Blueprint, render_template, session
from .models import Category, Product

biodling = Blueprint("biodling", __name__)


@biodling.route("/biodling", methods=["GET", "POST"])
def index():
    # Get the biodling category
    category = Category.query.filter_by(slug="biodling").first()

    # Get active products in this category
    products = []
    if category:
        products = (
            Product.query.filter_by(category_id=category.id, is_active=True)
            .order_by(Product.name)
            .all()
        )

    return render_template(
        "biodling.html",
        user=session.get("user"),
        page_title="Biodling",
        products=products,
        category=category,
    )
