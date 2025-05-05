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
    return render_template('home.html', user=session.get('user'))

@main.route('/login')
def login():
    github = OAuth2Session(
        current_app.config['GITHUB_CLIENT_ID'],
        scope=['read:user'],
        redirect_uri=url_for('main.callback', _external=True)
    )
    authorization_url, state = github.authorization_url(
        current_app.config['GITHUB_AUTHORIZE_URL']
    )
    session['oauth_state'] = state
    return redirect(authorization_url)

@main.route('/callback')
def callback():
    github = OAuth2Session(
        current_app.config['GITHUB_CLIENT_ID'],
        state=session['oauth_state'],
        redirect_uri=url_for('main.callback', _external=True)
    )
    token = github.fetch_token(
        current_app.config['GITHUB_TOKEN_URL'],
        client_secret=current_app.config['GITHUB_CLIENT_SECRET'],
        authorization_response=request.url
    )
    
    github = OAuth2Session(
        current_app.config['GITHUB_CLIENT_ID'],
        token=token
    )
    user_data = github.get(current_app.config['GITHUB_API_URL']).json()
    
    # Check if user is an admin
    admin = Admin.query.filter_by(github_id=user_data['id']).first()
    if admin:
        session['user'] = {
            'id': user_data['id'],
            'username': user_data['login'],
            'avatar_url': user_data['avatar_url']
        }
        flash('Successfully logged in!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    else:
        flash('You are not authorized to access this system.', 'error')
        return redirect(url_for('main.home'))

@main.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('admin.admin_dashboard'))