from flask import Blueprint, render_template, redirect, url_for, session, request, current_app, flash
from .models import Season
from . import db

seasons = Blueprint('seasons', __name__)

@seasons.route('/seasons')
def list_seasons():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    seasons = Season.query.order_by(Season.year.desc()).all()
    return render_template('seasons.html', seasons=seasons, user=session.get('user'))

@seasons.route('/seasons/create', methods=['POST'])
def create_season():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    year = request.form.get('year')
    
    # Check if season already exists
    existing_season = Season.query.filter_by(year=year).first()
    if existing_season:
        flash('En säsong med detta år finns redan.', 'error')
        return redirect(url_for('seasons.list_seasons'))
    
    # Create new season
    new_season = Season(year=year)
    db.session.add(new_season)
    db.session.commit()
    
    flash('Ny säsong skapad!', 'success')
    return redirect(url_for('seasons.list_seasons')) 