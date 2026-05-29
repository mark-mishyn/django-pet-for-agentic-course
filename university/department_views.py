import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListView(View):
    def get(self, request):
        departments = Department.objects.select_related("faculty").all()
        data = DepartmentSerializer.serialize_many(departments)
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class DepartmentCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            department_data = DepartmentSerializer.deserialize(data)
            department = Department.objects.create(**department_data)
            return JsonResponse(DepartmentSerializer.serialize(department), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class DepartmentRetrieveView(View):
    def get(self, request, pk):
        try:
            department = Department.objects.select_related("faculty").get(pk=pk)
            return JsonResponse(DepartmentSerializer.serialize(department))
        except Department.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class DepartmentUpdateView(View):
    def put(self, request, pk):
        try:
            department = Department.objects.select_related("faculty").get(pk=pk)
            data = json.loads(request.body)
            department_data = DepartmentSerializer.deserialize(data)

            for key, value in department_data.items():
                setattr(department, key, value)
            department.save()

            department.refresh_from_db()
            return JsonResponse(DepartmentSerializer.serialize(department))
        except Department.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class DepartmentDeleteView(View):
    def delete(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            department.delete()
            return JsonResponse(
                {"message": "Department deleted successfully"}, status=204
            )
        except Department.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=404)
