from django.db import transaction
from rest_framework import serializers

from courses import models


class CourseSectionSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.CourseSection
        fields = '__all__'


class InnerCourseSectionSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.CourseSection
        exclude = ('course', 'id')


class CourseSerializer(serializers.ModelSerializer):
    sections = InnerCourseSectionSerializer(many=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Course
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        sections_data = validated_data.pop('sections')
        instructors_data = validated_data.pop('instructors')

        course = models.Course.objects.create(**validated_data)

        for section_data in sections_data:
            models.CourseSection.objects.create(course=course, **section_data)

        for instructor_data in instructors_data:
            course.instructors.add(instructor_data)

        return course

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instructors_data = validated_data.pop('instructors')

        for instructor_data in instructors_data:
            instance.instructors.add(instructor_data)

        instance.save()

        return instance
