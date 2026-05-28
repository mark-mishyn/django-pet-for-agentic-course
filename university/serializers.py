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
