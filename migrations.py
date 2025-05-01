from flask_migrate import Migrate, upgrade, init, migrate
from sh_portal import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        init()  # Initialize migrations if they haven't been initialized
        migrate()  # Create a new migration
        upgrade()  # Apply the migration 