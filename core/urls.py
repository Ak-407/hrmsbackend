from django.urls import path
from .views import *

urlpatterns = [
    path("employees/", EmployeeListCreateView.as_view()),
    path("employees/<int:pk>/", EmployeeDeleteView.as_view()),
    path("attendance/", AttendanceCreateView.as_view()),
    path("attendance/list/", AttendanceListView.as_view()),
]
