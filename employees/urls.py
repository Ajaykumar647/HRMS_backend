from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r'', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
