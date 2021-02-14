from django_filters import rest_framework as django_filters
from rest_framework import generics, viewsets, filters

from profiles import models
from profiles import serializers


class GroupSet(viewsets.ModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('number',)


class StreamSet(viewsets.ModelViewSet):
    queryset = models.Stream.objects.all()
    serializer_class = serializers.StreamSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('number',)


class StudentSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('group',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')


class InstructorSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all()
    serializer_class = serializers.InstructorSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
