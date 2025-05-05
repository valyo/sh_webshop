from flask import Blueprint, render_template, session

biodling = Blueprint('biodling', __name__)

@biodling.route('/biodling', methods=['GET', 'POST'])
def index():
    return render_template(
        'biodling.html',
        user=session.get('user'),
        page_title="Biodling"
    ) 