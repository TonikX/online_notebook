from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import StudentStream, StudentGroup, Course, Lesson, StudentLessonResult, \
                    Section, TaskWithTick, TaskWithTickOption, TaskWithTickStudentResult


User = get_user_model()


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


class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Section
        fields = '__all__'


class CreateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class TaskWithTickSerializer(serializers.ModelSerializer):
    section = SectionSerializer()

    class Meta:
        model = TaskWithTick
        fields = '__all__'


class CreateTaskWithTickSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTick
        fields = '__all__'


class TaskWithTickOptionSerializer(serializers.ModelSerializer):
    task_with_tick = TaskWithTickSerializer()

    class Meta:
        model = TaskWithTickOption
        fields = '__all__'


class CreateTaskWithTickOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTickOption
        fields = '__all__'


class TaskWithTickStudentResultSerializer(serializers.ModelSerializer):
    task_with_tick = TaskWithTickSerializer()
    user = GroupMemberSerializer()

    class Meta:
        model = TaskWithTickStudentResult
        fields = '__all__'


class CreateTaskWithTickStudentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTickStudentResult
        fields = '__all__'
