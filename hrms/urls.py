from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'HRMS Lite API is running'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/employees/', include('employees.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/dashboard/', include('employees.dashboard_urls')),
    path('health/', health_check),
]
