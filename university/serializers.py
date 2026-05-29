class FacultySerializer:
    @staticmethod
    def serialize(faculty):
        """Serialize a Faculty instance to a dictionary."""
        return {
            "id": faculty.id,
            "title": faculty.title,
            "description": faculty.description,
            "created_at": faculty.created_at.isoformat(),
            "updated_at": faculty.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_many(faculties):
        """Serialize a queryset or list of Faculty instances."""
        return [FacultySerializer.serialize(faculty) for faculty in faculties]

    @staticmethod
    def deserialize(data):
        """Extract and validate data for creating/updating a Faculty."""
        return {"title": data.get("title"), "description": data.get("description", "")}


class DepartmentSerializer:
    @staticmethod
    def serialize(department):
        return {
            "id": department.id,
            "title": department.title,
            "description": department.description,
            "faculty": {
                "id": department.faculty_id,
                "title": department.faculty.title,
            },
            "created_at": department.created_at.isoformat(),
            "updated_at": department.updated_at.isoformat(),
        }

    @staticmethod
    def serialize_many(departments):
        return [DepartmentSerializer.serialize(d) for d in departments]

    @staticmethod
    def deserialize(data):
        return {
            "title": data.get("title"),
            "description": data.get("description", ""),
            "faculty_id": data.get("faculty_id"),
        }
