from django.db import transaction
from rest_framework import serializers

from profiles import models
from courses.models import Course


class GroupSerializer(serializers.ModelSerializer):
    courses = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = models.Group
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        courses_data = validated_data.pop('courses')

        group = models.Group.objects.create(**validated_data)

        for course_data in courses_data:
            group.courses.add(course_data)

        return group


class StreamSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='number', queryset=models.Group.objects.all())

    class Meta:
        model = models.Stream
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        groups_data = validated_data.pop('groups')

        stream = models.Stream.objects.create(**validated_data)

        for group_data in groups_data:
            stream.groups.add(group_data)

        return stream


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = '__all__'
