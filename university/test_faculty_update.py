import json

from django.test import TransactionTestCase
from django.urls import reverse

from .models import Faculty


class FacultyUpdateViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Computer Science", description="CS department"
        )
        self.url = reverse("faculty-update", kwargs={"pk": self.faculty.pk})

    def test_update_faculty(self):
        """Test PUT request updates the faculty."""
        payload = {"title": "Data Science", "description": "DS department"}
        response = self.client.put(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Data Science")
        self.assertEqual(data["description"], "DS department")

    def test_update_faculty_persists_to_database(self):
        """Test that updated faculty is saved in the database."""
        payload = {"title": "Mathematics", "description": "Math dept"}
        self.client.put(self.url, json.dumps(payload), content_type="application/json")

        self.faculty.refresh_from_db()
        self.assertEqual(self.faculty.title, "Mathematics")
        self.assertEqual(self.faculty.description, "Math dept")

    def test_update_faculty_response_structure(self):
        """Test that response contains all required fields."""
        payload = {"title": "Physics", "description": "Physics dept"}
        response = self.client.put(
            self.url, json.dumps(payload), content_type="application/json"
        )

        data = json.loads(response.content)
        required_fields = {"id", "title", "description", "created_at", "updated_at"}
        self.assertEqual(set(data.keys()), required_fields)

    def test_update_nonexistent_faculty(self):
        """Test PUT request for nonexistent faculty returns 404."""
        url = reverse("faculty-update", kwargs={"pk": 9999})
        payload = {"title": "Physics", "description": "Physics dept"}
        response = self.client.put(
            url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_update_with_duplicate_title(self):
        """Test PUT request with duplicate title returns 400."""
        Faculty.objects.create(title="Mathematics", description="Math dept")
        payload = {"title": "Mathematics", "description": "Updated"}
        response = self.client.put(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_with_invalid_json(self):
        """Test PUT request with invalid JSON returns 400."""
        response = self.client.put(
            self.url, "not valid json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_get_method_not_allowed(self):
        """Test GET request returns 405."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
