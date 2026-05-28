import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Faculty
from .serializers import FacultySerializer


class FacultyListView(View):
    def get(self, request):
        faculties = Faculty.objects.all()
        data = FacultySerializer.serialize_many(faculties)
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class FacultyCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            faculty_data = FacultySerializer.deserialize(data)
            faculty = Faculty.objects.create(**faculty_data)
            return JsonResponse(FacultySerializer.serialize(faculty), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class FacultyRetrieveView(View):
    def get(self, request, pk):
        try:
            faculty = Faculty.objects.get(pk=pk)
            return JsonResponse(FacultySerializer.serialize(faculty))
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class FacultyUpdateView(View):
    def put(self, request, pk):
        try:
            faculty = Faculty.objects.get(pk=pk)
            data = json.loads(request.body)
            faculty_data = FacultySerializer.deserialize(data)

            for key, value in faculty_data.items():
                setattr(faculty, key, value)
            faculty.save()

            return JsonResponse(FacultySerializer.serialize(faculty))
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class FacultyDeleteView(View):
    def delete(self, request, pk):
        try:
            faculty = Faculty.objects.get(pk=pk)
            faculty.delete()
            return JsonResponse({"message": "Faculty deleted successfully"}, status=204)
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)
