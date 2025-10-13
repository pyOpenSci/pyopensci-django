# pyopensci-django

A repository to migrate the pyOpenSci Jekyll site to Django with Wagtail CMS.

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Prerequisites

Before setting up the project locally, make sure you have the following installed:

- First, install **uv** - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- Then make sure you have **Python 3.12+** installed. You can install it using uv:

```shell
$ uv python install 3.12
```
- **Node.js** - [Download from nodejs.org](https://nodejs.org/) (for TailwindCSS)

## Local Development Setup

### 1. Set Up Python Environment with uv

```bash
# Install all dependencies and create virtual environment
uv sync

# Install Node.js packages for TailwindCSS
npm install
```

If you are running a development server locally and you have set things up previously, you may want to delete your existing 
database and start from scratch. To do this, delete the `db.sqlite3` file in the project root:

```bash
rm db.sqlite3
```

### 2. Build CSS and Set Up Database

```bash
# Build TailwindCSS stylesheets
npm run build-prod

# Run migrations using uv
uv run python manage.py migrate
```

### 3. Create an admin user (optional)

If you want to try out the Django Admin dashboard or Wagtail dashboard,
create a superuser (admin) account which can be used for Django Admin and Wagtail:

```bash
# Create superuser (optional - for admin access)
uv run python manage.py createsuperuser
```

### 4. Generate Test Data (optional but recommended)

To see how blog and events pages look with content,
generate dummy blog posts and events:

```bash
# Generate default test data (25 blog posts, 20 events)
uv run python manage.py create_dummy_posts

# Or specify custom amounts
uv run python manage.py create_dummy_posts --blog-posts=30 --events=25

# Delete any existing dummy data
uv run python manage.py create_dummy_posts --delete
```

This command creates:
- Blog posts distributed across multiple years (for testing the drop down, year filters)
- Events with both past and upcoming dates
- Random tags, authors, and excerpts
- All posts are automatically published and visible

### 5. Run Development Server

```bash
# Start Django development server
uv run python manage.py runserver
```

## Available Pages

- **Homepage (Django)**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Blog Index**: [http://127.0.0.1:8000/blog/](http://127.0.0.1:8000/blog/)
- **Events Index**: [http://127.0.0.1:8000/events/](http://127.0.0.1:8000/events/)
- **Wagtail Admin**: [http://127.0.0.1:8000/cms/](http://127.0.0.1:8000/cms/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Running Tests

```bash
# Run all tests
uv run python manage.py test

# Run tests with verbose output (shows each test name)
uv run python manage.py test -v 2

# Run tests with coverage
uv run coverage run --source='.' manage.py test
uv run coverage report

# Generate HTML coverage report
uv run coverage html
```

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
