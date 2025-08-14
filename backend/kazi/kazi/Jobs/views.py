from django.shortcuts import render
from .models import JobCategories, JobTag, JobStatus, Job, JobImage
from .serializers import JobCategoriesSerializers, JobTagSerializers, JobStatusSerializer, JobSerializer
from rest_framework import viewsets
from rest_framework import permissions
# Create your views here.

# category viewset


class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategories.objects.all()
    serializer_class = JobCategoriesSerializers
    lookup_field = "slug"
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsOwnerOrReadOnly]

# tag viewset


class JobTagViewSet(viewsets.ModelViewSet):
    queryset = JobTag.objects.all()
    serializer_class = JobTagSerializers
    lookup_field = "slug"
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsOwnerOrReadOnly]


# status viewset


class JobStatusViewSet(viewsets.ModelViewSet):
    queryset = JobStatus.objects.all()
    serializer_class = JobStatusSerializer
    lookup_field = "slug"
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsOwnerOrReadOnly]

# job viewset


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = "slug"
