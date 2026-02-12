from flask import Blueprint, render_template, session
from .models import Product

main = Blueprint("main", __name__)


@main.route("/")
def home():
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    return render_template("home.html", user=session.get("user"), products=products)
