# Solberg Honung Webshop

A Flask-based e-commerce platform for Solberg Honung, featuring product management, shopping cart functionality, and admin dashboard.

## Features

- 🛍️ Product catalog with categories
- 🛒 Shopping cart functionality
- 🔐 GitHub OAuth admin authentication
- 📱 Responsive design with Bootstrap 5
- 🔒 Admin dashboard for product and category management
- 🖼️ Product image upload with local storage
- 🔍 Image zoom viewer on product pages
- 💰 Price management in SEK
- 📦 Stock tracking

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Database**: SQLite (development) with Flask-SQLAlchemy
- **Migrations**: Flask-Migrate (Alembic)
- **Authentication**: GitHub OAuth for admin access
- **File Storage**: Local storage for product images
- **Icons**: Font Awesome 6

## Project Structure

```
sh_shop/
├── sh_webshop/              # Main application package
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   └── uploads/
│   │       └── products/    # Uploaded product images
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── categories/  # Category management templates
│   │   │   └── products/    # Product management templates
│   │   ├── cart/
│   │   │   └── view.html    # Shopping cart page
│   │   ├── products/
│   │   │   ├── index.html   # Product listing
│   │   │   └── detail.html  # Product detail with image zoom
│   │   ├── base.html        # Base template
│   │   ├── home.html        # Home page
│   │   ├── about.html       # About page
│   │   ├── biodling.html    # Beekeeping products
│   │   └── far_och_lamm.html # Sheep & lamb products
│   ├── __init__.py          # Application factory
│   ├── admin.py             # Admin routes and image upload
│   ├── models.py            # Database models
│   ├── cart.py              # Shopping cart functionality
│   ├── products.py          # Product routes
│   ├── about.py             # About page routes
│   ├── biodling.py          # Beekeeping category routes
│   ├── far_och_lamm.py      # Sheep & lamb category routes
│   ├── home.py              # Home page routes
│   ├── utils.py             # Utility functions
│   ├── commands.py          # CLI commands
│   └── config.py            # Configuration (uploads, OAuth)
├── migrations/              # Database migrations (Alembic)
├── instance/                # Instance-specific files
│   └── sh_shop.db           # SQLite database
├── main.py                  # Application entry point
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
├── env.example              # Example environment variables
├── VERSION                  # Application version
└── README.md
```

## Setup

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone git@github.com:valyo/sh_webshop.git
   cd sh_webshop
   ```

2. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8088`

To stop the application:
```bash
docker-compose down
```

For development:
```bash
docker-compose up --build -d  # Run in detached mode
docker-compose logs -f        # View logs
```

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

## Database Migrations

Create a new migration:
```bash
# Using Docker
docker-compose exec web flask db migrate -m "migration message"

# Local development
flask db migrate -m "migration message"
```

Apply migrations:
```bash
# Using Docker
docker-compose exec web flask db upgrade

# Local development
flask db upgrade
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `DATABASE_URL` | Database connection URL |
| `GITHUB_CLIENT_ID` | GitHub OAuth client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth client secret |

## Admin Access

Admin authentication uses GitHub OAuth. To grant admin access:

1. Configure GitHub OAuth credentials in `.env`
2. Add admin users to the `Admin` table with their GitHub ID

## Product Image Upload

- Supported formats: PNG, JPG, JPEG, GIF, WebP
- Maximum file size: 16MB
- Images are stored in `sh_webshop/static/uploads/products/`
- Unique filenames are generated to prevent collisions

## Docker Image Versioning

The application uses semantic versioning. The version is stored in the `VERSION` file.

### Version Format
Images are tagged with:
- Full version (e.g., `v1.0.0`)
- Version with Git SHA (e.g., `v1.0.0-a1b2c3d`)
- Latest tag (for main branch)

### Updating Version
1. Update the `VERSION` file following semantic versioning
2. Commit and push the changes
3. GitHub Action will automatically build and tag the new version

### Using Specific Versions
```bash
docker pull ghcr.io/valyo/sh_webshop:v1.0.0
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License

Copyright (c) 2025 Solberg Honung

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

For any inquiries, please contact the repository owner.
