from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobCategoryViewSet, JobTagViewSet, JobStatusViewSet, JobViewSet

router = DefaultRouter()
router.register(r"job-category", JobCategoryViewSet, basename="job-category"),
router.register(r"job-tag", JobTagViewSet, basename="job-tag"),
router.register(r"job-status", JobStatusViewSet, basename="job-status"),
router.register(r"job", JobViewSet, basename="job")

urlpatterns = [
    path("", include(router.urls)),
    
]
