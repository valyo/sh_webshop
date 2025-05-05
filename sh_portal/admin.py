from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from functools import wraps

admin = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Please log in to access this page.', 'error')
            return render_template(
                'admin/dashboard.html',
                user=None,
                page_title="Admin Dashboard"
            )
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@login_required
def admin_dashboard():
    return render_template(
        'admin/dashboard.html',
        user=session.get('user'),
        page_title="Admin Dashboard"
    ) 