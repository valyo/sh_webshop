from flask import Blueprint, render_template, redirect, url_for, session, request, flash, current_app
from .models import Season
from . import db
import re

lammandel = Blueprint('lammandel', __name__)

def extract_sheet_id(sheet_link):
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_link)
    if match:
        return match.group(1)
    return sheet_link

@lammandel.route('/lammandel/import-bookings', methods=['POST'])
def import_bookings():
    if not session.get('user'):
        return redirect(url_for('main.home'))

    try:
        season_id = request.form.get('season_id')
        sheet_link = request.form.get('sheet_link')
        range_name = request.form.get('range_name', 'Sheet1!A2:K')
        if not season_id or not sheet_link or not range_name:
            flash('Säsong, Google Sheet-länk och range krävs.', 'error')
            return redirect(url_for('lammandel.index'))

        sheet_id = extract_sheet_id(sheet_link)

        # You should reuse your get_sheet_data function from andelsbiodling.py
        from .andelsbiodling import get_sheet_data
        data = get_sheet_data(sheet_id, range_name)
        if not data:
            flash('Kunde inte hämta data från Google Sheet.', 'error')
            return redirect(url_for('lammandel.index'))

        # ... Your import logic here (copy from andelsbiodling) ...

        flash('Bokningar har importerats framgångsrikt!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error importing bookings: {str(e)}")
        flash('Ett fel uppstod vid import av bokningar.', 'error')

    return redirect(url_for('lammandel.index'))

@lammandel.route('/lammandel', methods=['GET', 'POST'])
def index():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    seasons = Season.query.order_by(Season.year.desc()).all()
    selected_season_id = request.form.get('season_id')
    selected_season = None

    if selected_season_id:
        selected_season = Season.query.get(selected_season_id)
    elif seasons:
        selected_season = seasons[0]

    return render_template('lammandel.html',
                         user=session.get('user'),
                         seasons=seasons,
                         selected_season=selected_season) 