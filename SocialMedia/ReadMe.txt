# Flask Social Media App

A simple Flask web application with user login, registration, and a basic posting system using MySQL.

## Project Structure

- `app/`
  - `__init__.py`: Initializes the Flask app, sets up configurations, and connects extensions.
  - `routes.py`: Contains the routes that define the behavior for different URLs.
  - `models.py`: Defines the data models and interaction with the MySQL database.
  - `forms.py`: Defines the forms for login and registration.
  - `templates/`: Stores HTML files for rendering views.
  - `static/`: Stores static files like CSS.
- `config.py`: Holds configuration settings (not fully used in this guide).
- `run.py`: The main entry point to run the application.

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
