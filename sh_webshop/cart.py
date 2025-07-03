from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from .models import Product
from . import db

cart = Blueprint("cart", __name__)


def get_cart():
    """Get the current session cart or create a new one."""
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


def get_cart_count():
    """Get the total number of items in the cart."""
    cart = get_cart()
    return sum(item["quantity"] for item in cart.values())


@cart.route("/cart/add", methods=["POST"])
def add_item():
    """Add an item to the cart."""
    cart = get_cart()
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")

    if not all([product_id, quantity]):
        flash("Invalid request.", "error")
        return redirect(url_for("biodling.index"))

    try:
        product_id = str(product_id)  # Convert to string for session storage
        quantity = int(quantity)
    except ValueError:
        flash("Invalid quantity.", "error")
        return redirect(url_for("biodling.index"))

    product = Product.query.get_or_404(int(product_id))

    if not product.is_active:
        flash("This product is no longer available.", "error")
        return redirect(url_for("biodling.index"))

    if quantity > product.stock:
        flash("Requested quantity exceeds available stock.", "error")
        return redirect(url_for("biodling.index"))

    # Update cart
    if product_id in cart:
        cart[product_id]["quantity"] += quantity
        if cart[product_id]["quantity"] > product.stock:
            cart[product_id]["quantity"] = product.stock
            flash("Quantity adjusted to available stock.", "warning")
    else:
        cart[product_id] = {
            "quantity": quantity,
            "name": product.name,
            "price": float(product.price),
            "image_url": product.image_url,
        }

    session["cart"] = cart
    flash("Product added to cart!", "success")
    return redirect(url_for("biodling.index"))


@cart.route("/cart")
def view_cart():
    """View the current cart."""
    cart = get_cart()
    cart_items = []
    cart_total = 0.0  # Initialize as float

    for product_id, item in cart.items():
        product = Product.query.get(int(product_id))
        if product and product.is_active:
            item_total = float(product.price) * item["quantity"]
            cart_items.append(
                {
                    "id": product_id,
                    "product": product,
                    "quantity": item["quantity"],
                    "item_total": item_total,
                }
            )
            cart_total += item_total

    return render_template(
        "cart/view.html",
        cart_items=cart_items,
        cart_total=cart_total,  # Pass as simple float
        page_title="Shopping Cart",
    )


@cart.route("/cart/update/<product_id>", methods=["POST"])
def update_item(product_id):
    """Update the quantity of an item in the cart."""
    cart = get_cart()
    quantity = request.form.get("quantity")

    try:
        quantity = int(quantity)
        if quantity <= 0:
            cart.pop(product_id, None)
        else:
            product = Product.query.get_or_404(int(product_id))
            if quantity > product.stock:
                quantity = product.stock
                flash("Quantity adjusted to available stock.", "warning")
            cart[product_id]["quantity"] = quantity
    except ValueError:
        flash("Invalid quantity.", "error")
        return redirect(url_for("cart.view_cart"))

    session["cart"] = cart
    flash("Cart updated!", "success")
    return redirect(url_for("cart.view_cart"))


@cart.route("/cart/remove/<product_id>", methods=["POST"])
def remove_item(product_id):
    """Remove an item from the cart."""
    cart = get_cart()
    cart.pop(product_id, None)
    session["cart"] = cart
    flash("Item removed from cart!", "success")
    return redirect(url_for("cart.view_cart"))
