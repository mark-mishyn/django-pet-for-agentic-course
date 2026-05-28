---
name: crud-endpoints
description: Scaffold full CRUD endpoints (List, Create, Retrieve, Update, Delete) for a Django model. Use this skill whenever the user asks to add endpoints, add CRUD, create API for a model, wire up a model, or anything that implies creating REST views for a model. One model per invocation.
---

# CRUD Endpoints

Scaffolds a complete set of five JSON REST API endpoints for a single Django model: List, Create, Retrieve, Update, Delete. Each endpoint is a separate class-based view.

The user provides a model (either an existing one or describes what they need). You produce four things: the serializer, the views, the URL patterns, and the root URL include (if it's a new app).

## Step 1: Understand the model

If the model already exists, read it. If the user describes a new model, create it first (with migration), then proceed.

Identify:

- Model name (e.g., `Faculty`)
- All user-facing fields (exclude `id`, `created_at`, `updated_at`)
- Which fields are required vs. optional (have defaults or `blank=True`)
- Which fields have unique constraints
- The plural form for URL paths (e.g., `faculties`, `students`, `courses`)

## Step 2: Create the serializer

Add a serializer class to the app's `serializers.py` (create the file if it doesn't exist).

The serializer is a plain class with three static methods — no DRF, no base class.

```python
class <Model>Serializer:
    @staticmethod
    def serialize(<instance_var>):
        return {
            "id": <instance_var>.id,
            # all model fields...
            "created_at": <instance_var>.created_at.isoformat(),
            "updated_at": <instance_var>.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_many(<plural_var>):
        return [<Model>Serializer.serialize(item) for item in <plural_var>]

    @staticmethod
    def deserialize(data):
        return {
            # only writable fields, using data.get()
            # required fields: data.get("<field>")
            # optional fields: data.get("<field>", <default>)
        }
```

Rules:

- `serialize` returns all fields including `id`, `created_at`, `updated_at`
- `serialize_many` delegates to `serialize` in a list comprehension
- `deserialize` returns only writable fields (no `id`, `created_at`, `updated_at`)
- Use `data.get("<field>")` for required fields (no default — lets the DB constraint raise)
- Use `data.get("<field>", <default>)` for optional fields
- DateTime fields use `.isoformat()` in serialize

## Step 3: Create the views

Add five view classes to the app's `views.py` (create the file if it doesn't exist).

Every view inherits from `django.views.View`. State-changing views (Create, Update, Delete) get `@method_decorator(csrf_exempt, name="dispatch")`.

### ListView

```python
class <Model>ListView(View):
    def get(self, request):
        items = <Model>.objects.all()
        data = <Model>Serializer.serialize_many(items)
        return JsonResponse(data, safe=False)
```

### CreateView

```python
@method_decorator(csrf_exempt, name="dispatch")
class <Model>CreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            item_data = <Model>Serializer.deserialize(data)
            item = <Model>.objects.create(**item_data)
            return JsonResponse(<Model>Serializer.serialize(item), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
```

### RetrieveView

```python
class <Model>RetrieveView(View):
    def get(self, request, pk):
        try:
            item = <Model>.objects.get(pk=pk)
            return JsonResponse(<Model>Serializer.serialize(item))
        except <Model>.DoesNotExist:
            return JsonResponse({"error": "<Model> not found"}, status=404)
```

### UpdateView

```python
@method_decorator(csrf_exempt, name="dispatch")
class <Model>UpdateView(View):
    def put(self, request, pk):
        try:
            item = <Model>.objects.get(pk=pk)
            data = json.loads(request.body)
            item_data = <Model>Serializer.deserialize(data)

            for key, value in item_data.items():
                setattr(item, key, value)
            item.save()

            return JsonResponse(<Model>Serializer.serialize(item))
        except <Model>.DoesNotExist:
            return JsonResponse({"error": "<Model> not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
```

### DeleteView

```python
@method_decorator(csrf_exempt, name="dispatch")
class <Model>DeleteView(View):
    def delete(self, request, pk):
        try:
            item = <Model>.objects.get(pk=pk)
            item.delete()
            return JsonResponse({"message": "<Model> deleted successfully"}, status=204)
        except <Model>.DoesNotExist:
            return JsonResponse({"error": "<Model> not found"}, status=404)
```

### Imports at the top of views.py

```python
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import <Model>
from .serializers import <Model>Serializer
```

When appending to an existing `views.py`, add only the missing imports.

## Step 4: Create the URL patterns

Add URL patterns to the app's `urls.py` (create the file if it doesn't exist).

```python
from django.urls import path
from . import views

urlpatterns = [
    path("<plural>/", views.<Model>ListView.as_view(), name="<model>-list"),
    path("<plural>/create/", views.<Model>CreateView.as_view(), name="<model>-create"),
    path("<plural>/<int:pk>/", views.<Model>RetrieveView.as_view(), name="<model>-retrieve"),
    path("<plural>/<int:pk>/update/", views.<Model>UpdateView.as_view(), name="<model>-update"),
    path("<plural>/<int:pk>/delete/", views.<Model>DeleteView.as_view(), name="<model>-delete"),
]
```

Rules:

- URL path prefix is the lowercase plural form (e.g., `faculties/`, `students/`, `courses/`)
- Route names are `<model>-<action>` in kebab-case (e.g., `faculty-list`, `student-create`)
- When appending to an existing `urls.py`, add the new patterns to the existing `urlpatterns` list

## Step 5: Wire up root URLs (if new app)

If this is a new app that isn't yet included in `config/urls.py`, add:

```python
path("api/", include("<app_name>.urls")),
```

All API endpoints live under the `/api/` prefix. If the app is already included, skip this step.

## Step 6: Run migrations (if model is new)

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## Step 7: Verify

Start the dev server and smoke-test one endpoint to confirm it works:

```bash
uv run python manage.py runserver &
sleep 2
curl -s http://localhost:8000/api/<plural>/ | python -m json.tool
```

Kill the server after verification. If there's an error, fix it before considering the task done.

## Step 8: Generate tests

Use the `generate-tests` skill to create tests for all five views.
