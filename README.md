# Django Job Portal Assignment Project

## Quick Start Instructions for macOS

1. Open **Terminal** on your Mac.
2. Unzip the downloaded file and navigate to the project directory:
   ```bash
   cd ~/Downloads/job_portal_project
   ```
3. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. (Optional) Create a superuser to access the Django Admin:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the local development server:
   ```bash
   python manage.py runserver
   ```
8. Open your browser and go to `http://127.0.0.1:8000/`.
