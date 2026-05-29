from django.urls import path

from .department_views import (
    DepartmentCreateView,
    DepartmentDeleteView,
    DepartmentListView,
    DepartmentRetrieveView,
    DepartmentUpdateView,
)
from .faculty_views import (
    FacultyCreateView,
    FacultyDeleteView,
    FacultyListView,
    FacultyRetrieveView,
    FacultyUpdateView,
)

urlpatterns = [
    path("faculties/", FacultyListView.as_view(), name="faculty-list"),
    path("faculties/create/", FacultyCreateView.as_view(), name="faculty-create"),
    path(
        "faculties/<int:pk>/",
        FacultyRetrieveView.as_view(),
        name="faculty-retrieve",
    ),
    path(
        "faculties/<int:pk>/update/",
        FacultyUpdateView.as_view(),
        name="faculty-update",
    ),
    path(
        "faculties/<int:pk>/delete/",
        FacultyDeleteView.as_view(),
        name="faculty-delete",
    ),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path(
        "departments/create/",
        DepartmentCreateView.as_view(),
        name="department-create",
    ),
    path(
        "departments/<int:pk>/",
        DepartmentRetrieveView.as_view(),
        name="department-retrieve",
    ),
    path(
        "departments/<int:pk>/update/",
        DepartmentUpdateView.as_view(),
        name="department-update",
    ),
    path(
        "departments/<int:pk>/delete/",
        DepartmentDeleteView.as_view(),
        name="department-delete",
    ),
]
