from flask import Blueprint, render_template, session
from .models import Category, Product

far_och_lamm = Blueprint("far_och_lamm", __name__)


@far_och_lamm.route("/far-och-lamm", methods=["GET", "POST"])
def index():
    # Get the far-och-lamm category
    category = Category.query.filter_by(slug="far-och-lamm").first()

    # Get active products in this category
    products = []
    if category:
        products = (
            Product.query.filter_by(category_id=category.id, is_active=True)
            .order_by(Product.name)
            .all()
        )

    return render_template(
        "far_och_lamm.html",
        user=session.get("user"),
        page_title="Får och lamm produkter",
        products=products,
        category=category,
    ) 