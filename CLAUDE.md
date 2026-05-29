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
- ALWAYS use the `commit` skill for git commits — but only when explicitly asked to commit, never proactively
- ALWAYS use the `generate-tests` skill when writing tests — never write tests ad-hoc
- ALWAYS use the `crud-endpoints` skill when adding REST endpoints for a model — never scaffold views/urls/serializers ad-hoc
- Always use double quotes for strings (e.g., `"hello"` not `'hello'`)
- Always use modern Python 3.13 type hints (e.g., `str | None` not `Optional[str]`, `list[str]` not `List[str]`)
- Use built-in Django test framework for unit testing — no pytest
- Use `TransactionTestCase` for all test classes that write to the database; use `TestCase` only for read-only tests
- Use class-based views (CBVs) for all views
- Views are JSON REST API endpoints (no templates, no HTML)
- Use custom plain-class serializers (no DRF) with static methods: `serialize(instance)`, `serialize_many(queryset)`, `deserialize(data)`
