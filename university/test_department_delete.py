import json

from django.test import TransactionTestCase
from django.urls import reverse

from .models import Department, Faculty


class DepartmentDeleteViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Engineering", description="Engineering faculty"
        )
        self.department = Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        self.url = reverse("department-delete", kwargs={"pk": self.department.pk})

    def test_delete_department(self):
        """Test DELETE request removes the department."""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Department.objects.count(), 0)

    def test_delete_department_returns_empty_body(self):
        """Test DELETE response has no content body for 204."""
        response = self.client.delete(self.url)

        self.assertEqual(response.content, b"")

    def test_delete_nonexistent_department(self):
        """Test DELETE request for nonexistent department returns 404."""
        url = reverse("department-delete", kwargs={"pk": 9999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_delete_same_department_twice(self):
        """Test DELETE request for already deleted department returns 404."""
        self.client.delete(self.url)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 404)

    def test_get_method_not_allowed(self):
        """Test GET request returns 405."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
