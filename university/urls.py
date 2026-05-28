from django.urls import path
from . import views

urlpatterns = [
    path('faculties/', views.FacultyListView.as_view(), name='faculty-list'),
    path('faculties/create/', views.FacultyCreateView.as_view(), name='faculty-create'),
    path('faculties/<int:pk>/', views.FacultyRetrieveView.as_view(), name='faculty-retrieve'),
    path('faculties/<int:pk>/update/', views.FacultyUpdateView.as_view(), name='faculty-update'),
    path('faculties/<int:pk>/delete/', views.FacultyDeleteView.as_view(), name='faculty-delete'),
]
