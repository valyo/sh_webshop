# Solberg Honung Webshop

A Flask-based e-commerce platform for Solberg Honung, featuring product management, shopping cart functionality, and admin dashboard.

## Features

- 🛍️ Product catalog with categories
- 🛒 Shopping cart functionality
- 👤 User authentication
- 📱 Responsive design
- 🔒 Admin dashboard for product management
- 🖼️ Image upload support
- 💰 Price management
- 📦 Stock tracking

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Database**: SQLite (development)
- **Authentication**: Flask-Login
- **File Storage**: Local storage
- **Icons**: Font Awesome

## Project Structure

```
sh_shop/
├── sh_webshop/           # Main application package
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   ├── __init__.py     # Application factory
│   ├── admin.py        # Admin routes and functionality
│   ├── models.py       # Database models
│   ├── cart.py         # Shopping cart functionality
│   ├── products.py     # Product routes
│   ├── about.py        # About page routes
│   ├── biodling.py     # Biodling routes
│   ├── lammskinn.py    # Lammskinn routes
│   ├── home.py         # Home page routes
│   ├── utils.py        # Utility functions
│   ├── commands.py     # CLI commands
│   └── config.py       # Configuration
├── migrations/          # Database migrations
├── instance/           # Instance-specific files
├── main.py            # Application entry point
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt   # Python dependencies
└── .env              # Environment variables
```

## Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:valyo/sh_webshop.git
   cd sh_webshop
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:5000`

To stop the application:
```bash
docker-compose down
```

For development, you can use:
```bash
docker-compose up --build -d  # Run in detached mode
docker-compose logs -f        # View logs
```

To manage database migrations:
```bash
# Create a new migration
docker-compose exec web flask db migrate -m "migration message"

# Apply migrations
docker-compose exec web flask db upgrade
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