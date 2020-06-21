from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import StudentStream, StudentGroup, Course, Lesson, StudentLessonResult

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "tel", "group")


class StudentStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStream
        fields = ("id", "title")


class StudentGroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudentGroup
        fields = ("id", "title", "number", "year_of_receipt", "members")


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "tel")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'


class StudentLessonResultSerializer(serializers.ModelSerializer):
    mark = serializers.CharField(source='get_mark_display')
    visit = serializers.CharField(source='get_visit_display')

    class Meta:
        model = StudentLessonResult
        fields = '__all__'


class CreateStudentLessonResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLessonResult
        fields = '__all__'
