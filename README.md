# University CRM API

A lightweight JSON REST API for managing university entities (faculties, departments), built with Django.

This is a pet project created as part of an **Agentic Engineering** course, exploring AI-assisted software development workflows with Claude Code.

## Tech Stack

- **Python 3.13** / **Django 6.0**
- **SQLite** (default, zero-config)
- **uv** for dependency management
- **ruff** for linting and formatting
- No DRF -- uses plain class-based views and custom serializers

## API Endpoints

All endpoints are prefixed with `/api/`.

### Faculties

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/faculties/` | List all faculties |
| POST | `/api/faculties/create/` | Create a faculty |
| GET | `/api/faculties/<id>/` | Retrieve a faculty |
| PUT | `/api/faculties/<id>/update/` | Update a faculty |
| DELETE | `/api/faculties/<id>/delete/` | Delete a faculty |

### Departments

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/departments/` | List all departments |
| POST | `/api/departments/create/` | Create a department |
| GET | `/api/departments/<id>/` | Retrieve a department |
| PUT | `/api/departments/<id>/update/` | Update a department |
| DELETE | `/api/departments/<id>/delete/` | Delete a department |

## Quick Start

```bash
# Clone and enter the project
git clone <repo-url>
cd django-pet

# Install dependencies
uv sync

# Apply migrations
uv run python manage.py migrate

# Run the dev server
uv run python manage.py runserver
```

## Running Tests

```bash
uv run python manage.py test
```

Tests are organized per model under `university/tests/`, covering all CRUD operations.

## Project Structure

```
config/             Django project settings, urls, wsgi/asgi
university/
  models.py         Faculty, Department models
  serializers.py    Plain-class serializers (no DRF)
  faculty_views.py  Faculty CRUD views (class-based)
  department_views.py  Department CRUD views (class-based)
  urls.py           API route definitions
  tests/
    faculty/        Faculty endpoint tests
    department/     Department endpoint tests
```

## Agentic Engineering

This project is built almost entirely through AI-assisted development using [Claude Code](https://docs.anthropic.com/en/docs/claude-code). The development workflow relies on custom Claude Code skills for:

- **CRUD scaffolding** -- generating views, serializers, URLs, and tests for new models
- **Test generation** -- producing tests that follow project conventions
- **Commit automation** -- linting, formatting, and crafting commit messages
- **Pre-commit hooks** -- running the full test suite before every commit
