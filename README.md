# pyopensci-django

A repository to migrate the pyOpenSci Jekyll site to Django with Wagtail CMS

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Prerequisites

Before setting up the project locally, make sure you have the following installed:

- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
- **Node.js** - [Download from nodejs.org](https://nodejs.org/) (for TailwindCSS)

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

# Install Node.js packages for TailwindCSS
npm install
```

### 3. Build CSS and Set Up Database

```bash
# Build TailwindCSS stylesheets
npm run build-prod

# Run migrations
python manage.py migrate

# Create superuser (optional - for admin access)
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
# Start Django development server
python manage.py runserver
```

## Testing the Homepage Migration

- **Homepage (Django)**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Blog (Wagtail)**: [http://127.0.0.1:8000/blog/](http://127.0.0.1:8000/blog/)
- **Wagtail Admin**: [http://127.0.0.1:8000/cms/](http://127.0.0.1:8000/cms/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.philipnarteh.me/"><img src="https://avatars.githubusercontent.com/u/43896066?v=4?s=100" width="100px;" alt="Philip Narteh"/><br /><sub><b>Philip Narteh</b></sub></a><br /><a href="https://github.com/pyOpenSci/pyopensci-django/commits?author=Phinart98" title="Code">💻</a> <a href="https://github.com/pyOpenSci/pyopensci-django/pulls?q=is%3Apr+reviewed-by%3APhinart98" title="Reviewed Pull Requests">👀</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

