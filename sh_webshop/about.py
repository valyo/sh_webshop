from flask import Blueprint, render_template, session

about = Blueprint('about', __name__)

@about.route('/om-oss')
def index():
    return render_template(
        'about.html',
        user=session.get('user'),
        page_title="Om oss"
    ) 