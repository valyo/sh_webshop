from flask import Blueprint, render_template, redirect, url_for, session, request, flash, current_app
from .models import Season, Bookings
from . import db
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime

andelsbiodling = Blueprint('andelsbiodling', __name__)

def get_sheet_data(sheet_id, range_name):
    """
    Fetch data from Google Sheet using service account
    """
    try:
        # Use service account credentials
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = service_account.Credentials.from_service_account_file(
            'sh-web-portal-f370fff1378a.json',  # You'll need to create this
            scopes=SCOPES
        )

        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=range_name
        ).execute()

        return result.get('values', [])
    except Exception as e:
        current_app.logger.error(f"Error fetching sheet data: {str(e)}")
        return None

@andelsbiodling.route('/andelsbiodling/import-bookings', methods=['POST'])
def import_bookings():
    if not session.get('user'):
        return redirect(url_for('main.home'))

    try:
        # Get the selected season
        season_id = request.form.get('season_id')
        if not season_id:
            flash('Ingen säsong vald.', 'error')
            return redirect(url_for('andelsbiodling.index'))

        # Google Sheet ID and range
        SHEET_ID = current_app.config['GOOGLE_SHEET_ID']  # Add this to your config
        RANGE_NAME = 'import!A2:I'  # Adjust based on your sheet structure

        # Fetch data from Google Sheet
        data = get_sheet_data(SHEET_ID, RANGE_NAME)
        if not data:
            flash('Kunde inte hämta data från Google Sheet.', 'error')
            return redirect(url_for('andelsbiodling.index'))

        # Convert to DataFrame for easier handling
        df = pd.DataFrame(data, columns=[
            'timestamp', 'email', 'name', 'telephone', 
            'address', 'postnummer', 'ort', 'message', 'number'
        ])

        # Process each row
        for _, row in df.iterrows():
            # Convert timestamp from "11/26/2024 16:12:32" to datetime object
            try:
                timestamp_obj = datetime.strptime(row['timestamp'], '%m/%d/%Y %H:%M:%S')
                # No need to convert to string, use the datetime object directly
            except ValueError as e:
                current_app.logger.error(f"Error parsing timestamp: {str(e)}")
                flash(f'Fel format på timestamp för bokning: {row["email"]}', 'error')
                continue

            # Check if booking already exists
            existing_booking = Bookings.query.filter_by(
                email=row['email'],
                season_id=season_id
            ).first()

            if not existing_booking:
                # Create new booking using the datetime object
                booking = Bookings(
                    season_id=season_id,
                    timestamp=timestamp_obj,  # Use the datetime object directly
                    email=row['email'],
                    name=row['name'],
                    telephone=row['telephone'],
                    address=row['address'],
                    postnummer=row['postnummer'],
                    ort=row['ort'],
                    message=row['message'],
                    number=int(row['number'])
                )
                db.session.add(booking)

        db.session.commit()
        flash('Bokningar har importerats framgångsrikt!', 'success')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error importing bookings: {str(e)}")
        flash('Ett fel uppstod vid import av bokningar.', 'error')

    return redirect(url_for('andelsbiodling.index'))

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