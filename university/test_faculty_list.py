import json
from django.test import TransactionTestCase
from django.urls import reverse
from .models import Faculty


class FacultyListViewTests(TransactionTestCase):
    def test_get_empty_list(self):
        """Test GET request returns empty list when no faculties exist."""
        url = reverse("faculty-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_get_single_faculty(self):
        """Test GET request returns list with single faculty."""
        faculty = Faculty.objects.create(
            title="Computer Science", description="CS department"
        )
        url = reverse("faculty-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], faculty.id)
        self.assertEqual(data[0]["title"], "Computer Science")
        self.assertEqual(data[0]["description"], "CS department")

    def test_get_multiple_faculties(self):
        """Test GET request returns list with multiple faculties."""
        Faculty.objects.create(title="Computer Science", description="CS department")
        Faculty.objects.create(title="Mathematics", description="Math dept")
        Faculty.objects.create(title="Physics", description="Physics dept")

        url = reverse("faculty-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        titles = {item["title"] for item in data}
        self.assertEqual(titles, {"Computer Science", "Mathematics", "Physics"})

    def test_response_structure(self):
        """Test that response contains all required fields."""
        Faculty.objects.create(title="Engineering", description="Engineering faculty")
        url = reverse("faculty-list")
        response = self.client.get(url)

        data = json.loads(response.content)
        faculty_data = data[0]

        required_fields = {"id", "title", "description", "created_at", "updated_at"}
        self.assertEqual(set(faculty_data.keys()), required_fields)
