from flask import Blueprint, render_template, redirect, url_for, session
from . import db

andelsbiodling = Blueprint('andelsbiodling', __name__)

@andelsbiodling.route('/andelsbiodling')
def index():
    if not session.get('user'):
        return redirect(url_for('main.home'))
    
    return render_template('andelsbiodling.html', user=session.get('user')) 