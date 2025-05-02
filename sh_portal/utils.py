from datetime import datetime
from flask import current_app, flash
import pandas as pd

def import_bookings_from_sheet(
    db,
    BookingsModel,
    season_id,
    sheet_data,
    column_map=None
):
    """
    Imports bookings from Google Sheet data into the specified BookingsModel.
    - db: SQLAlchemy db object
    - BookingsModel: The model class to use (Bookings or BookingsLamm)
    - season_id: The season to associate bookings with
    - sheet_data: List of rows from Google Sheets
    - column_map: Optional dict to map sheet columns to model fields
    """
    if not sheet_data:
        flash('No data to import.', 'error')
        return False

    # Default column order
    columns = [
        'timestamp', 'email', 'name', 'telephone',
        'address', 'postnummer', 'ort', 'message', 'number'
    ]
    if column_map:
        columns = [column_map.get(col, col) for col in columns]

    df = pd.DataFrame(sheet_data, columns=columns)

    imported_count = 0
    for _, row in df.iterrows():
        # Parse timestamp
        try:
            timestamp_obj = datetime.strptime(row['timestamp'], '%m/%d/%Y %H:%M:%S')
        except Exception as e:
            current_app.logger.error(f"Error parsing timestamp: {str(e)}")
            flash(f'Invalid timestamp format for booking: {row["email"]}', 'error')
            continue

        # Check for existing booking
        existing_booking = BookingsModel.query.filter_by(
            email=row['email'],
            season_id=season_id
        ).first()

        if not existing_booking:
            booking = BookingsModel(
                season_id=season_id,
                timestamp=timestamp_obj,
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
            imported_count += 1

    try:
        db.session.commit()
        flash(f'{imported_count} bookings have been imported successfully!', 'success')
        return True
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error committing bookings: {str(e)}")
        flash('An error occurred while importing bookings.', 'error')
        return False 