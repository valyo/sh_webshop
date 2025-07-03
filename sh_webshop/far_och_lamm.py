from flask import Blueprint, render_template, session

far_och_lamm = Blueprint("far_och_lamm", __name__)


@far_och_lamm.route("/far-och-lamm", methods=["GET", "POST"])
def index():
    return render_template(
        "far_och_lamm.html", user=session.get("user"), page_title="Får och lamm produkter"
    ) 