from flask import Blueprint, render_template, session

lammskinn = Blueprint('lammskinn', __name__)

@lammskinn.route('/lammskinn', methods=['GET', 'POST'])
def index():
    return render_template(
        'lammskinn.html',
        user=session.get('user'),
        page_title="Lammskinn"
    ) 