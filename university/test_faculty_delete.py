import json

from django.test import TransactionTestCase
from django.urls import reverse

from .models import Faculty


class FacultyDeleteViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Computer Science", description="CS department"
        )
        self.url = reverse("faculty-delete", kwargs={"pk": self.faculty.pk})

    def test_delete_faculty(self):
        """Test DELETE request removes the faculty."""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Faculty.objects.count(), 0)

    def test_delete_faculty_returns_empty_body(self):
        """Test DELETE response has no content body for 204."""
        response = self.client.delete(self.url)

        self.assertEqual(response.content, b"")

    def test_delete_nonexistent_faculty(self):
        """Test DELETE request for nonexistent faculty returns 404."""
        url = reverse("faculty-delete", kwargs={"pk": 9999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_delete_same_faculty_twice(self):
        """Test DELETE request for already deleted faculty returns 404."""
        self.client.delete(self.url)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 404)

    def test_get_method_not_allowed(self):
        """Test GET request returns 405."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
