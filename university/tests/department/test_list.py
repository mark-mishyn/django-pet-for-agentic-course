import json

from django.test import TransactionTestCase
from django.urls import reverse

from ...models import Department, Faculty


class DepartmentListViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Engineering", description="Engineering faculty"
        )

    def test_get_empty_list(self):
        """Test GET request returns empty list when no departments exist."""
        url = reverse("department-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_get_single_department(self):
        """Test GET request returns list with single department."""
        department = Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        url = reverse("department-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], department.id)
        self.assertEqual(data[0]["title"], "Computer Science")
        self.assertEqual(data[0]["description"], "CS department")

    def test_get_multiple_departments(self):
        """Test GET request returns list with multiple departments."""
        Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        Department.objects.create(
            title="Mathematics",
            description="Math dept",
            faculty=self.faculty,
        )
        Department.objects.create(
            title="Physics",
            description="Physics dept",
            faculty=self.faculty,
        )

        url = reverse("department-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        titles = {item["title"] for item in data}
        self.assertEqual(titles, {"Computer Science", "Mathematics", "Physics"})

    def test_response_structure(self):
        """Test that response contains all required fields including faculty."""
        Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        url = reverse("department-list")
        response = self.client.get(url)

        data = json.loads(response.content)
        department_data = data[0]

        required_fields = {
            "id",
            "title",
            "description",
            "faculty",
            "created_at",
            "updated_at",
        }
        self.assertEqual(set(department_data.keys()), required_fields)
        self.assertEqual(set(department_data["faculty"].keys()), {"id", "title"})
