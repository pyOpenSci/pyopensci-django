# pyopensci-django
A repository to migrate the pyOpenSci Jekyll site to Django with Wagtail CMS

## Prerequisites

Before setting up the project locally, make sure you have the following installed:

- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)

## Local Development Setup

### 1. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 3. Set Up Database and Run Server

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional - for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the site.

### 4. Access Wagtail Admin

Visit [http://127.0.0.1:8000/cms/](http://127.0.0.1:8000/cms/) to access the Wagtail admin interface.
