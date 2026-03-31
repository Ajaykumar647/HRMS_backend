from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r'', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]
