import json

from django.test import TransactionTestCase
from django.urls import reverse

from ...models import Department, Faculty


class DepartmentRetrieveViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Engineering", description="Engineering faculty"
        )
        self.department = Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        self.url = reverse("department-retrieve", kwargs={"pk": self.department.pk})

    def test_retrieve_department(self):
        """Test GET request returns a single department."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["id"], self.department.pk)
        self.assertEqual(data["title"], "Computer Science")
        self.assertEqual(data["description"], "CS department")
        self.assertEqual(data["faculty"]["id"], self.faculty.pk)
        self.assertEqual(data["faculty"]["title"], "Engineering")

    def test_retrieve_department_response_structure(self):
        """Test that response contains all required fields."""
        response = self.client.get(self.url)

        data = json.loads(response.content)
        required_fields = {
            "id",
            "title",
            "description",
            "faculty",
            "created_at",
            "updated_at",
        }
        self.assertEqual(set(data.keys()), required_fields)

    def test_retrieve_nonexistent_department(self):
        """Test GET request for nonexistent department returns 404."""
        url = reverse("department-retrieve", kwargs={"pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_post_method_not_allowed(self):
        """Test POST request returns 405."""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)
