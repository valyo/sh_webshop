# Flask Web Application

A Flask-based web application with SQLite database and Docker support.

## Features

- Flask web framework
- SQLite database
- Docker development environment
- Bootstrap 5 for styling
- Responsive navigation bar

## Setup and Running

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

3. Build and run the application using Docker Compose:
```bash
docker-compose up --build
```

4. Access the application at http://localhost:5000

## Development

- The application uses Flask's development server with hot-reloading
- SQLite database file will be created automatically
- Static files are served from the `static` directory
- Templates are stored in the `templates` directory

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── static/            # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
└── templates/         # HTML templates
    └── home.html
``` 