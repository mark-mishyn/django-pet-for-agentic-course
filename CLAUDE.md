# Django Pet Project

## Commands
- Run server: `uv run python manage.py runserver`
- Run tests: `uv run python manage.py test`
- Add dependency: `uv add <package>`
- Django management: `uv run python manage.py <command>`

## Project Structure
- `config/` — Django project settings, urls, wsgi/asgi
- SQLite database (default, no setup needed)

## Conventions
- Minimal setup: no admin, no auth, no sessions, no messages
- Add these back only when explicitly requested
- Use uv for all Python/dependency commands (not pip)
- ALWAYS run `uv run ruff check --fix . && uv run ruff format .` before commits. If ruff check fails, fix all issues before proceeding — never commit code that doesn't pass ruff
