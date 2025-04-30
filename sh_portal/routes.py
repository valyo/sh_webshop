from flask import Blueprint, render_template, redirect, url_for, session, request, current_app, flash
from requests_oauthlib import OAuth2Session
import os
from .models import Admin, Season
from . import db
main = Blueprint('main', __name__)

def get_oauth():
    return OAuth2Session(
        client_id=current_app.config['GITHUB_CLIENT_ID'],
        redirect_uri='http://localhost:8087/callback',
        scope=['user:email']
    )

@main.route('/')
def home():
    current_app.logger.info(f"Session: {session.get('user')}")
    return render_template('home.html', user=session.get('user'))

@main.route('/login')
def login():
    oauth = get_oauth()
    authorization_url, state = oauth.authorization_url(current_app.config['GITHUB_AUTHORIZE_URL'])
    session['oauth_state'] = state
    return redirect(authorization_url)

@main.route('/callback')
def callback():
    oauth = get_oauth()
    token = oauth.fetch_token(
        current_app.config['GITHUB_TOKEN_URL'],
        client_secret=current_app.config['GITHUB_CLIENT_SECRET'],
        authorization_response=request.url
    )

    # Get user info from GitHub
    resp = oauth.get(current_app.config['GITHUB_API_URL'])
    user_info = resp.json()

    # Check if user already exists in database
    existing_user = Admin.query.filter_by(github_id=user_info['id']).first()
    #if not, redirect to login page
    if not existing_user:
        return render_template('home.html', message=f"Hello Sulyoipulyo, you've nothing to do here!")
    else:
        # Store user info in session
        session['user'] = {
        'username': user_info['login'],  # GitHub username is in the 'login' field
        'name': user_info.get('name', ''),
        'avatar_url': user_info.get('avatar_url', ''),
        'id': user_info['id']
        }
        current_app.logger.info(f"User info: {user_info}")
        return redirect(url_for('main.home'))

@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))

@main.route('/seasons')
def seasons():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    seasons = Season.query.order_by(Season.year.desc()).all()
    return render_template('seasons.html', seasons=seasons, user=session.get('user'))

@main.route('/seasons/create', methods=['POST'])
def create_season():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    year = request.form.get('year')
    
    # Check if season already exists
    existing_season = Season.query.filter_by(year=year).first()
    if existing_season:
        flash('En säsong med detta år finns redan.', 'error')
        return redirect(url_for('main.seasons'))
    
    # Create new season
    new_season = Season(year=year)
    db.session.add(new_season)
    db.session.commit()
    
    flash('Ny säsong skapad!', 'success')
    return redirect(url_for('main.seasons'))