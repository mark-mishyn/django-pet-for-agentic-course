import json

from django.test import TransactionTestCase
from django.urls import reverse

from .models import Faculty


class FacultyCreateViewTests(TransactionTestCase):
    def setUp(self):
        self.url = reverse("faculty-create")

    def test_create_faculty(self):
        """Test POST request creates a new faculty."""
        payload = {"title": "Computer Science", "description": "CS department"}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Computer Science")
        self.assertEqual(data["description"], "CS department")
        self.assertIn("id", data)
        self.assertEqual(Faculty.objects.count(), 1)

    def test_create_faculty_persists_to_database(self):
        """Test that created faculty is saved in the database."""
        payload = {"title": "Mathematics", "description": "Math dept"}
        self.client.post(self.url, json.dumps(payload), content_type="application/json")

        faculty = Faculty.objects.get(title="Mathematics")
        self.assertEqual(faculty.description, "Math dept")

    def test_create_faculty_response_structure(self):
        """Test that response contains all required fields."""
        payload = {"title": "Physics", "description": "Physics dept"}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        data = json.loads(response.content)
        required_fields = {"id", "title", "description", "created_at", "updated_at"}
        self.assertEqual(set(data.keys()), required_fields)

    def test_create_faculty_without_description(self):
        """Test POST request with missing description defaults to empty string."""
        payload = {"title": "Engineering"}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Engineering")
        self.assertEqual(data["description"], "")

    def test_create_faculty_with_invalid_json(self):
        """Test POST request with invalid JSON returns 400."""
        response = self.client.post(
            self.url, "not valid json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_create_faculty_with_empty_body(self):
        """Test POST request with empty body returns 400."""
        response = self.client.post(self.url, "", content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_get_method_not_allowed(self):
        """Test GET request returns 405."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)


class FacultyCreateViewIntegrityTests(TransactionTestCase):
    def setUp(self):
        self.url = reverse("faculty-create")

    def test_create_faculty_without_title(self):
        """Test POST request without title returns 400."""
        payload = {"description": "No title faculty"}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Faculty.objects.count(), 0)

    def test_create_faculty_with_duplicate_title(self):
        """Test POST request with duplicate title returns 400."""
        Faculty.objects.create(title="Computer Science", description="CS department")
        payload = {"title": "Computer Science", "description": "Another CS dept"}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Faculty.objects.count(), 1)
