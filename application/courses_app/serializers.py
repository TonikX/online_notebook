from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import \
    StudentStream, StudentGroup, Course, Lesson, StudentLessonResult, Section,\
    ClassmatesCheckedTask, TaskOption, StudentResult, Check, Section, TaskWithTick, \
    TaskWithTickOption, TaskWithTickStudentResult, TaskWithKeywordResult, \
    TaskWithTeacherCheckResult, TaskWithClassmatesCheckResult, TaskWithKeyword, \
    TaskWithClassmatesCheck, TaskWithTeacherCheck, TaskWithKeywordOption


User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "tel", "group", "username")


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
    task_with_tick = TaskWithTickSerializer()
    user = GroupMemberSerializer()

    class Meta:
        model = TaskWithTickStudentResult
        fields = '__all__'


class CreateTaskWithTickStudentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTickStudentResult
        fields = '__all__'


class TaskWithKeywordSerializer(serializers.ModelSerializer):
    section = SectionSerializer()

    class Meta:
        model = TaskWithKeyword
        fields = '__all__'


class CreateTaskWithKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithKeyword
        fields = '__all__'


class TaskWithKeywordOptionSerializer(serializers.ModelSerializer):
    task = TaskWithKeywordSerializer()

    class Meta:
        model = TaskWithKeywordOption
        fields = '__all__'


class CreateTaskWithKeywordOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithKeywordOption
        fields = '__all__'


class TaskWithKeywordResultSerializer(serializers.ModelSerializer):
    user = StudentSerializer()
    option = TaskWithKeywordOptionSerializer()

    class Meta:
        model = TaskWithKeywordResult
        fields = '__all__'


class CreateTaskWithKeywordResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithKeywordResult
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    RESULT_BY_TASK = {
        TaskWithKeyword: TaskWithKeywordResult,
        TaskWithClassmatesCheck: TaskWithClassmatesCheckResult,
        TaskWithTeacherCheck: TaskWithTeacherCheckResult,
    }

    results = serializers.SerializerMethodField()

    def get_results(self, task):
        task_result_model = self.RESULT_BY_TASK[task.__class__]
        results = task_result_model.objects.filter(option__task_id=task.id)
        serializer = TaskResultSerializer(results, task_result_model=task_result_model, many=True)

        return serializer.data

    class Meta:
        model = None
        fields = ('id', 'title', 'results')


class TaskResultSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        task_result_model = kwargs.pop('task_result_model')
        fields = kwargs.pop('fields', None)

        self.Meta.model = task_result_model

        if fields is not None:
            self.Meta.fields = fields

        super(TaskResultSerializer, self).__init__(*args, **kwargs)

    task_id = serializers.SerializerMethodField()

    def get_task_id(self, task_result):
        return task_result.option.task.id

    class Meta:
        model = None
        fields = ('user', 'perform')


class UserResultsSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.task_result_model = kwargs.pop('task_result_model')
        self.section_id = kwargs.pop('section_id')

        super(UserResultsSerializer, self).__init__(*args, **kwargs)

    def get_results(self, user):
        field_to_retrieve = ('perform', 'task_id')
        results = self.task_result_model.objects.filter(user=user, option__task__section_id=self.section_id)
        serializer = TaskResultSerializer(results, many=True, task_result_model=self.task_result_model,
                                          fields=field_to_retrieve)

        return serializer.data

    class Meta:
        model = User
        fields = ('id', 'first_name', 'username', 'results')
