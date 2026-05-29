import json

from django.test import TransactionTestCase
from django.urls import reverse

from ...models import Department, Faculty


class DepartmentCreateViewTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Engineering", description="Engineering faculty"
        )
        self.url = reverse("department-create")

    def test_create_department(self):
        """Test POST request creates a new department."""
        payload = {
            "title": "Computer Science",
            "description": "CS department",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Computer Science")
        self.assertEqual(data["description"], "CS department")
        self.assertIn("id", data)
        self.assertEqual(Department.objects.count(), 1)

    def test_create_department_persists_to_database(self):
        """Test that created department is saved in the database."""
        payload = {
            "title": "Mathematics",
            "description": "Math dept",
            "faculty_id": self.faculty.pk,
        }
        self.client.post(self.url, json.dumps(payload), content_type="application/json")

        department = Department.objects.get(title="Mathematics")
        self.assertEqual(department.description, "Math dept")
        self.assertEqual(department.faculty_id, self.faculty.pk)

    def test_create_department_response_structure(self):
        """Test that response contains all required fields."""
        payload = {
            "title": "Physics",
            "description": "Physics dept",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.post(
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

    def test_create_department_without_description(self):
        """Test POST request with missing description defaults to empty string."""
        payload = {"title": "Chemistry", "faculty_id": self.faculty.pk}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Chemistry")
        self.assertEqual(data["description"], "")

    def test_create_department_with_invalid_json(self):
        """Test POST request with invalid JSON returns 400."""
        response = self.client.post(
            self.url, "not valid json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_create_department_with_empty_body(self):
        """Test POST request with empty body returns 400."""
        response = self.client.post(self.url, "", content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_get_method_not_allowed(self):
        """Test GET request returns 405."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)


class DepartmentCreateViewIntegrityTests(TransactionTestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            title="Engineering", description="Engineering faculty"
        )
        self.url = reverse("department-create")

    def test_create_department_without_title(self):
        """Test POST request without title returns 400."""
        payload = {"description": "No title dept", "faculty_id": self.faculty.pk}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Department.objects.count(), 0)

    def test_create_department_without_faculty_id(self):
        """Test POST request without faculty_id returns 400."""
        payload = {"title": "Orphan Dept", "description": "No faculty"}
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Department.objects.count(), 0)

    def test_create_department_with_invalid_faculty_id(self):
        """Test POST request with nonexistent faculty_id returns 400."""
        payload = {
            "title": "Bad Faculty Dept",
            "description": "Invalid FK",
            "faculty_id": 9999,
        }
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Department.objects.count(), 0)

    def test_create_department_with_duplicate_title(self):
        """Test POST request with duplicate title returns 400."""
        Department.objects.create(
            title="Computer Science",
            description="CS department",
            faculty=self.faculty,
        )
        payload = {
            "title": "Computer Science",
            "description": "Another CS dept",
            "faculty_id": self.faculty.pk,
        }
        response = self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Department.objects.count(), 1)
