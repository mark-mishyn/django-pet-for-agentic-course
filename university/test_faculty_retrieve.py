import json

from django.test import TransactionTestCase
from django.urls import reverse

from .models import Faculty


class FacultyRetrieveViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Computer Science", description="CS department"
        )
        self.url = reverse("faculty-retrieve", kwargs={"pk": self.faculty.pk})

    def test_retrieve_faculty(self):
        """Test GET request returns a single faculty."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["id"], self.faculty.pk)
        self.assertEqual(data["title"], "Computer Science")
        self.assertEqual(data["description"], "CS department")

    def test_retrieve_faculty_response_structure(self):
        """Test that response contains all required fields."""
        response = self.client.get(self.url)

        data = json.loads(response.content)
        required_fields = {"id", "title", "description", "created_at", "updated_at"}
        self.assertEqual(set(data.keys()), required_fields)

    def test_retrieve_nonexistent_faculty(self):
        """Test GET request for nonexistent faculty returns 404."""
        url = reverse("faculty-retrieve", kwargs={"pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_post_method_not_allowed(self):
        """Test POST request returns 405."""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)
