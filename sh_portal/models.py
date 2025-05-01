from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(10))
    
    def __repr__(self):
        return f'<Season {self.year}>'


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.Integer, unique=True)
    github_name = db.Column(db.String(150))
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    # password = db.Column(db.String(150))


class Bookings(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    email = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    telephone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    postnummer = db.Column(db.String(10), nullable=False)
    ort = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text)
    number = db.Column(db.Integer, nullable=False)

    # Relationship with Season
    season = db.relationship('Season', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Bookings {self.name} - {self.season.year}>'

