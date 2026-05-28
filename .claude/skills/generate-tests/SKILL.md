---
name: generate-tests
description: Generate Django view tests following project conventions. Use this skill whenever the user asks to write tests, add tests, generate tests, test a view, or anything that implies creating test files for Django views. Always use this skill instead of writing tests ad-hoc.
---

# Generate Tests

A step-by-step workflow for generating Django view tests. Follow these steps exactly in order.

## Step 1: Understand the target

Identify which view(s) need tests. Read the view code to understand:

- The HTTP method(s) it handles
- The URL pattern and route name
- What model it operates on
- Request/response format (JSON payloads, status codes)
- Any validation or error handling

Run these reads in parallel:

1. The view file containing the target view class
2. The URL configuration to get the exact route name
3. The model file to understand fields, constraints, and defaults

## Step 2: Read existing tests for style

Read 1-2 existing test files in the same app to match the project's exact style. Pay attention to:

- Import ordering
- How `setUp` is structured
- Assertion patterns and ordering
- How test data is constructed

If no existing tests exist, follow the conventions below exactly.

## Step 3: Write the test file

### File naming

One test file per view class: `test_<model>_<action>.py`

Examples: `test_faculty_list.py`, `test_faculty_create.py`, `test_faculty_retrieve.py`, `test_faculty_update.py`, `test_faculty_delete.py`

### Imports

```python
import json

from django.test import TransactionTestCase
from django.urls import reverse

from .models import <Model>
```

Only import `json` if the test actually uses `json.loads` or `json.dumps`.

### Test class

- Always use `TransactionTestCase` (never `TestCase`) for classes that write to the database
- Use `TestCase` only for purely read-only tests (rare — even list views typically create fixtures)
- One test class per file, named `<Model><Action>ViewTests` (e.g., `FacultyCreateViewTests`)
- Add a second class `<Model><Action>ViewIntegrityTests` when testing database constraints like unique violations or missing required fields

### setUp

- Create model fixtures needed by most tests
- Build `self.url` using `reverse("<route-name>", kwargs={...})` when the URL has parameters
- For list/create views (no URL params), build the URL inline in each test or in setUp — match existing style

### Test methods

Each test method follows this structure:

1. **Arrange** — set up any test-specific data (beyond setUp)
2. **Act** — make the HTTP request
3. **Assert** — check status code first, then response data, then database state

Separate arrange/act/assert blocks with blank lines for readability.

### Request format

For POST and PUT requests, always send JSON:

```python
payload = {"title": "Computer Science", "description": "CS department"}
response = self.client.post(self.url, json.dumps(payload), content_type="application/json")
```

Never use `self.client.post(url, payload)` without explicit JSON encoding — Django's test client defaults to multipart form encoding.

### What to test per view type

**List view:**
- Empty list returns `[]` with 200
- Single item returns list of one with correct fields
- Multiple items returns all with correct count
- Response structure has all expected fields (`id`, model fields, `created_at`, `updated_at`)

**Create view:**
- Happy path returns 201 with created object data
- Object actually persists in database (query and compare)
- Response structure has all expected fields
- Missing optional fields use defaults
- Missing required fields returns 400 with error details
- Duplicate unique field returns 400
- Invalid JSON body returns 400
- Empty request body returns 400
- Wrong HTTP method (GET) returns 405

**Retrieve view:**
- Happy path returns 200 with correct object data
- Response structure has all expected fields
- Nonexistent PK returns 404 with error in response
- Wrong HTTP method (POST) returns 405

**Update view:**
- Happy path returns 200 with updated data
- Changes actually persist in database (refresh_from_db and compare)
- Response structure has all expected fields
- Nonexistent PK returns 404
- Duplicate unique field returns 400
- Invalid JSON body returns 400
- Wrong HTTP method (GET) returns 405

**Delete view:**
- Happy path returns 204
- Response body is empty (`self.assertEqual(response.content, b"")`)
- Nonexistent PK returns 404 with error in response
- Deleting same object twice returns 404
- Wrong HTTP method (GET) returns 405

These are the baseline tests. Add more if the view has custom logic (filtering, pagination, permissions, etc.).

### Assertion patterns

```python
# Status code — always first
self.assertEqual(response.status_code, 201)

# Content type
self.assertEqual(response["Content-Type"], "application/json")

# Response data
data = json.loads(response.content)
self.assertEqual(data["title"], "Computer Science")

# Database state
self.assertEqual(Faculty.objects.count(), 1)
faculty = Faculty.objects.get(pk=data["id"])
self.assertEqual(faculty.title, "Computer Science")

# Error responses
data = json.loads(response.content)
self.assertIn("error", data)

# Empty body (204 responses)
self.assertEqual(response.content, b"")

# Response structure
required_fields = {"id", "title", "description", "created_at", "updated_at"}
self.assertEqual(set(data.keys()), required_fields)
```

Never assert on the exact error message text — just check the error key exists.

## Step 4: Run tests

```bash
uv run python manage.py test <app_label>.<test_module> -v2
```

Example: `uv run python manage.py test university.test_faculty_create -v2`

If tests fail, read the failure output carefully, fix the test (or identify a view bug), and rerun. Common issues:

- 204 responses have empty body — don't try to parse JSON from them
- `TransactionTestCase` resets the database between tests — don't rely on data from other test methods
- URL route names must match exactly what's in `urls.py`

## Step 5: Lint and format

```bash
uv run ruff check --fix . && uv run ruff format .
```

Fix any remaining ruff errors before considering the tests done.
