from flask import Blueprint, render_template, redirect, url_for, session, request
from .models import Season
from . import db

andelsbiodling = Blueprint('andelsbiodling', __name__)

@andelsbiodling.route('/andelsbiodling', methods=['GET', 'POST'])
def index():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    # Get all seasons ordered by year
    seasons = Season.query.order_by(Season.year.desc()).all()

    # Get selected season (either from form submission or most recent)
    selected_season_id = request.form.get('season_id')
    selected_season = None

    if selected_season_id:
        selected_season = Season.query.get(selected_season_id)
    elif seasons:
        selected_season = seasons[0]  # Default to most recent season

    return render_template('andelsbiodling.html',
                         user=session.get('user'),
                         seasons=seasons,
                         selected_season=selected_season)