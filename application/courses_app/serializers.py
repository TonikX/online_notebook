from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import StudentStream, StudentGroup, Course, Lesson, StudentLessonResult, Section, ClassmatesCheckedTask, \
                    TaskOption, StudentResult, Check, \
                    Section, TaskWithTick, TaskWithTickOption, TaskWithTickStudentResult, TaskWithTickCheck


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


class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Section
        fields = '__all__'


class ClassmatesCheckedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassmatesCheckedTask
        fields = '__all__'


class TaskOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOption
        fields = '__all__'


class StudentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResult
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check

        
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
    task_with_tick_option = TaskWithTickOptionSerializer()
    user = GroupMemberSerializer()

    class Meta:
        model = TaskWithTickStudentResult
        fields = '__all__'


class CreateTaskWithTickStudentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTickStudentResult
        fields = '__all__'


class TaskWithTickCheckSerializer(serializers.ModelSerializer):
    task_with_tick_student_result = TaskWithTickStudentResultSerializer()
    user = GroupMemberSerializer()

    class Meta:
        model = TaskWithTickCheck
        fields = '__all__'


class CreateTaskWithTickCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTickCheck
        fields = '__all__'
