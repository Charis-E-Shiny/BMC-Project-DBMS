# Business Model Canvas Application

A Flask-based web application for creating and managing Business Model Canvas (BMC).

## Features

- User authentication (login, signup)
- Role-based access control (admin, business_owner, investor)
- Create, edit, and view business models
- Add and remove components to/from business models
- Dashboard views for different user roles

## Database Schema

The application uses a relational database with the following tables:

- Users: Store user information and credentials
- BusinessModels: Store business model metadata
- Component tables:
  - CustomerSegments
  - CustomerRelationships
  - ValuePropositions
  - Channels
  - RevenueStreams
  - KeyResources
  - KeyActivities
  - KeyPartnerships
  - CostStructure

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- MySQL or PostgreSQL

### Installation

1. Extract the zip file to your desired location
2. Open the folder in VS Code
3. Set up a virtual environment (recommended):
```
python -m venv venv
```

4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

5. Install dependencies:
```
pip install -r package_requirements.txt
```

6. Configure the database:
   - For MySQL:
     - Create a database named "BMCbase"
     - Set user as "root" with password "charis123" (or modify db_config.py for your credentials)
     - Run the setup script: `python setup_db.py`

   - For PostgreSQL:
     - Set environment variables for PostgreSQL connection
     - Run the setup script: `python setup_db.py`

7. Run the application:
```
python run.py
```

8. Access the application at [http://localhost:5000](http://localhost:5000)

## VS Code Setup Guide

### Recommended Extensions

1. **Python**: Official Microsoft Python extension
2. **SQLTools**: Database management and query execution
3. **Jinja2 Template Syntax**: Syntax highlighting for Jinja2 templates
4. **HTML CSS Support**: Enhanced editing for HTML/CSS files

### Running in VS Code

1. Open the folder in VS Code
2. Open the Terminal (Terminal > New Terminal)
3. Make sure your virtual environment is activated
4. Run the application with: `python run.py`
5. For debugging:
   - Set breakpoints in your code
   - Press F5 to start debugging
   - Select "Python" as the debug configuration

### Database Setup in VS Code

1. Install SQLTools extension
2. Connect to your database:
   - Click on the database icon in the sidebar
   - Add a new connection
   - Choose MySQL or PostgreSQL
   - Enter your connection details
   - Test and save the connection

### Working with Templates

All HTML templates are in the `templates/` folder and use Jinja2 templating.

## Files Structure

- `main.py`: Application entry point
- `app.py`: Flask application and routes
- `db_config.py`: Database configuration and connection
- `models.py`: Object models for data entities
- `forms.py`: WTForms form definitions
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static assets
- `setup_db.py`: Script to set up the database tables
- `run.py`: Development server script

## Environment Variables

The application supports the following environment variables:

### MySQL Configuration
- `DB_HOST`: MySQL host (default: localhost)
- `DB_USER`: MySQL username (default: root)
- `DB_PASS`: MySQL password (default: charis123)
- `DB_NAME`: MySQL database name (default: BMCbase)

### PostgreSQL Configuration
- `DATABASE_URL`: Full PostgreSQL connection URL
- `PGHOST`: PostgreSQL host
- `PGUSER`: PostgreSQL username
- `PGPASSWORD`: PostgreSQL password
- `PGDATABASE`: PostgreSQL database name
- `PGPORT`: PostgreSQL port

## User Roles

1. **Admin**: Can view and manage all users and business models
2. **Business Owner**: Can create and manage their own business models
3. **Investor**: Can view all business models but not modify them

## Troubleshooting

### Database Connection Issues

- Ensure your database is running
- Check your connection credentials in db_config.py
- For MySQL users: Make sure the "BMCbase" database exists
- For PostgreSQL users: Ensure environment variables are set correctly

### Package Installation Problems

- Ensure you're using a compatible Python version (3.6+)
- If you encounter issues with mysqlclient, you may need to install MySQL development libraries:
  - Ubuntu/Debian: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`
  - macOS: `brew install mysql-client`
  - Windows: Install MySQL Connector C

### Application Not Starting

- Check logs for detailed error messages
- Ensure the port 5000 is not in use by another application
- Verify all required packages are installed