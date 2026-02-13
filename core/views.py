from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer

class EmployeeListCreateView(APIView):

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDeleteView(APIView):

    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response({"message": "Employee deleted"}, status=200)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)


class AttendanceCreateView(APIView):

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

from django.db.models import Count, Q

class AttendanceListView(APIView):

    def get(self, request):
        employee_id = request.query_params.get("employee")

        if not employee_id:
            return Response(
                {"error": "Employee parameter required"},
                status=400
            )

        attendance = Attendance.objects.filter(employee_id=employee_id)
        serializer = AttendanceSerializer(attendance, many=True)

        present_count = attendance.filter(status="Present").count()

        return Response({
            "records": serializer.data,
            "total_present_days": present_count
        })
