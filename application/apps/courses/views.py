from django_filters import rest_framework as django_filters
from rest_framework import generics, viewsets, filters

from courses import models
from courses import serializers


class CourseSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('name', 'created_by')
    search_fields = (
        'name', 'created_by__username', 'created_by__first_name', 'created_by__last_name', 'created_by__email'
    )


class CourseSectionSet(viewsets.ModelViewSet):
    queryset = models.CourseSection.objects.all()
    serializer_class = serializers.CourseSectionSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('name', 'course', 'created_by')
    search_fields = (
        'name', 'course__name', 'created_by__username', 'created_by__first_name', 'created_by__last_name',
        'created_by__email'
    )
