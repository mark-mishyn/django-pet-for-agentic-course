import json

from django.test import TransactionTestCase
from django.urls import reverse

from ...models import Department, Faculty


class DepartmentUpdateViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Engineering", description="Engineering faculty"
        )
        self.department = Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        self.url = reverse("department-update", kwargs={"pk": self.department.pk})

    def test_update_department(self):
        """Test PUT request updates the department."""
        payload = {
            "title": "Software Engineering",
            "description": "SE department",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.put(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Software Engineering")
        self.assertEqual(data["description"], "SE department")

    def test_update_department_persists_to_database(self):
        """Test that updated department is saved in the database."""
        payload = {
            "title": "Software Engineering",
            "description": "SE department",
            "faculty_id": self.faculty.pk,
        }
        self.client.put(self.url, json.dumps(payload), content_type="application/json")

        self.department.refresh_from_db()
        self.assertEqual(self.department.title, "Software Engineering")
        self.assertEqual(self.department.description, "SE department")

    def test_update_department_response_structure(self):
        """Test that response contains all required fields."""
        payload = {
            "title": "Updated Dept",
            "description": "Updated desc",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.put(
            self.url, json.dumps(payload), content_type="application/json"
        )

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

    def test_update_nonexistent_department(self):
        """Test PUT request for nonexistent department returns 404."""
        url = reverse("department-update", kwargs={"pk": 9999})
        payload = {
            "title": "Ghost",
            "description": "Nonexistent",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.put(
            url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_update_with_invalid_json(self):
        """Test PUT request with invalid JSON returns 400."""
        response = self.client.put(
            self.url, "not valid json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_update_with_duplicate_title(self):
        """Test PUT request with duplicate title returns 400."""
        Department.objects.create(
            title="Mathematics",
            description="Math dept",
            faculty=self.faculty,
        )
        payload = {
            "title": "Mathematics",
            "description": "Trying to steal title",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.put(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_get_method_not_allowed(self):
        """Test GET request returns 405."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
