from flask import Blueprint, render_template, session

products = Blueprint("products", __name__)


@products.route("/produkter")
def index():
    return render_template(
        "products/index.html", user=session.get("user"), page_title="Produkter"
    )
