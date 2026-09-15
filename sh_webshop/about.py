from flask import Blueprint, render_template, session

from . import db
from .models import AboutSection

about = Blueprint("about", __name__)

DEFAULT_ABOUT_SECTIONS = [
    {
        "title": "Vår historia",
        "content": (
            "Solberg Honung är ett familjeföretag som har drivit biodling och "
            "lammavel i flera generationer. Vi kombinerar traditionell kunskap "
            "med moderna metoder för att producera högkvalitativa produkter."
        ),
        "sort_order": 10,
    },
    {
        "title": "Vårt uppdrag",
        "content": (
            "Vi strävar efter att producera ekologiska och hållbara produkter "
            "samtidigt som vi tar hand om våra bin och lamm. Vår filosofi "
            "bygger på respekt för naturen och djuren."
        ),
        "sort_order": 20,
    },
    {
        "title": "Kontakta oss",
        "content": (
            "Solberg Honung\n"
            "Adress: [Din adress]\n"
            "Telefon: [Ditt telefonnummer]\n"
            "E-post: [Din e-post]"
        ),
        "sort_order": 30,
    },
]


def ensure_default_about_sections():
    """Seed the original about content if no sections exist yet."""
    if AboutSection.query.count() > 0:
        return
    for item in DEFAULT_ABOUT_SECTIONS:
        db.session.add(
            AboutSection(
                title=item["title"],
                content=item["content"],
                sort_order=item["sort_order"],
                is_active=True,
            )
        )
    db.session.commit()


@about.route("/om-oss")
def index():
    ensure_default_about_sections()
    sections = (
        AboutSection.query.filter_by(is_active=True)
        .order_by(AboutSection.sort_order, AboutSection.id)
        .all()
    )
    return render_template(
        "about.html",
        user=session.get("user"),
        page_title="Om oss",
        sections=sections,
    )
