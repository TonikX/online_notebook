from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import \
    StudentStream, StudentGroup, Course, Lesson, StudentLessonResult, Section,\
    ClassmatesCheckedTask, TaskOption, StudentResult, Check, Section, TaskWithTick, \
    TaskWithTickStudentResult, TaskWithKeywordResult, \
    TaskWithTeacherCheckResult, TaskWithKeyword, \
    TaskWithTeacherCheck, TaskWithTeacherCheckOption, TaskWithTeacherCheckCheck, \
    TaskWithKeyword, TaskWithKeywordOption, TaskWithTickInStream, \
    ClassmatesCheckedTaskInStream, TaskWithTeacherCheckInStream, \
    TaskWithKeywordInStream, StudentInCourse, CourseNews

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer


User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'access_key')


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        try:
            user.group = StudentGroup.objects.get(access_key = validated_data.get('access_key'))
        except:
            pass
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "tel", "group")


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "tel")


class StudentStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStream
        fields = ("id", "title")


class StudentGroupForStreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentGroup
        fields = ['id']



class StudentStreamCreateSerializer(serializers.ModelSerializer):
    #groups = StudentGroupForStreamSerializer(many=True)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=StudentGroup.objects.all())

    class Meta:
        model = StudentStream
        fields = ("id", "title", "groups", "course_access", 'deadline_date', 'start_date')


class StudentGroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudentGroup
        fields = ("id", "title", "number", "year_of_receipt", "members", "access_key")


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "tel")


class CourseListSerializer(serializers.ModelSerializer):
    owner = TeacherSerializer()


    class Meta:
        model = Course
        fields = '__all__'


class TaskWithTickInSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskWithTick
        fields = '__all__'


class TaskWithTeacherCheckInSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskWithTeacherCheck
        fields = '__all__'


class TaskWithKeywordCheckInSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskWithKeyword
        fields = '__all__'


class SectionInCourseSerializer(serializers.ModelSerializer):
    task_with_tick_in_section = TaskWithTickInSectionSerializer(many = True)
    task_with_teacher_check_in_section = TaskWithTeacherCheckInSectionSerializer(many = True)
    task_with_keyword_in_section = TaskWithKeywordCheckInSectionSerializer(many = True)
    class Meta:
        model = Section
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    owner = TeacherSerializer()
    sections_in_course = SectionInCourseSerializer(many = True)


    class Meta:
        model = Course
        fields = '__all__'


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name']


class LessonSerializer(serializers.ModelSerializer):
    #course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'


class StudentLessonResultSerializer(serializers.ModelSerializer):
    mark = serializers.CharField(source='get_mark_display')
    visit = serializers.CharField(source='get_visit_display')

    class Meta:
        model = StudentLessonResult
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    students_in_lesson = StudentLessonResultSerializer(many = True)

    class Meta:
        model = Lesson
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
        fields = '__all__'


class TaskWithTeacherOptionForCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskWithTeacherCheckOption
        fields = ['pk','title','description']


class TaskWithTeacherCreateCheckSerializer(serializers.ModelSerializer):
    option_for_task_with_teacher = TaskWithTeacherOptionForCreateSerializer(many = True)


    def create(self, validated_data):
        # Create instance
        task = TaskWithTeacherCheck.objects.create(title=validated_data['title'], description=validated_data['description'], section=validated_data['section'])

        # Create or update each page instance
        for option in validated_data['option_for_task_with_teacher']:
            task_with_teacher_option = TaskWithTeacherCheckOption(description=option['description'], title = option['title'], task=task)
            task_with_teacher_option.save()

        return task


    class Meta:
        model = TaskWithTeacherCheck
        fields = '__all__'
        extra_kwargs = {
            'option_for_task_with_teacher': {'required': False}
        }


class TaskWithTeacherCheckOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTeacherCheckOption
        fields = '__all__'


class TaskWithTeacherCheckSerializer(serializers.ModelSerializer):
    option_for_task_with_teacher = TaskWithTeacherCheckOptionSerializer(many = True)

    class Meta:
        model = TaskWithTeacherCheck
        fields = '__all__'


class TaskWithTeacherCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTeacherCheckResult
        fields = '__all__'


class TaskWithTeacherCheckCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTeacherCheckCheck
        fields = '__all__'

        
class CreateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['title', 'course']


class TaskWithTickSerializer(serializers.ModelSerializer):


    class Meta:
        model = TaskWithTick
        fields = '__all__'


class CreateTaskWithTickSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithTick
        fields = '__all__'


# class TaskWithTickOptionSerializer(serializers.ModelSerializer):
#     task_with_tick = TaskWithTickSerializer()
#
#     class Meta:
#         model = TaskWithTickOption
#         fields = '__all__'
#
#
# class CreateTaskWithTickOptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskWithTickOption
#         fields = '__all__'


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


class TaskSerializer(serializers.ModelSerializer):
    RESULT_BY_TASK = {
        TaskWithKeyword: TaskWithKeywordResult,
        ClassmatesCheckedTask: StudentResult,
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


class TaskWithKeywordForCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskWithKeywordOption
        fields = ['pk', 'title', 'description', 'keyword']


class TaskWithKeywordCreateSerializer(serializers.ModelSerializer):
    option_for_task_with_keyword = TaskWithKeywordForCreateSerializer(many = True)


    def create(self, validated_data):
        # Create the book instance
        book = TaskWithKeyword.objects.create(title=validated_data['title'], description=validated_data['description'],
                                              section=validated_data['section'])

        # Create or update each page instance
        for item in validated_data['option_for_task_with_keyword']:
            page = TaskWithKeywordOption(description=item['description'], title = item['title'], keyword = item['keyword'], task=book)
            page.save()

        return book


    class Meta:
        model = TaskWithKeyword
        fields = '__all__'


class TaskWithKeywordOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskWithKeywordOption
        fields = '__all__'


class TaskWithKeywordSerializer(serializers.ModelSerializer):
    option_for_task_with_keyword = TaskWithKeywordOptionSerializer(many = True)

    class Meta:
        model = TaskWithKeyword
        fields = '__all__'


class TaskWithKeywordResultSerializer(serializers.ModelSerializer):


    class Meta:
        model = TaskWithKeywordResult
        fields = '__all__'


class TaskWithKeywordResultCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = TaskWithKeywordResult
        fields = '__all__'

"""
Блой дедлайнов
"""


class TaskWithTickInStreamSerializer(serializers.ModelSerializer):


    class Meta:
        model = TaskWithTickInStream
        fields = '__all__'


class TaskWithTickInSectionForStreamSerializer(serializers.ModelSerializer):
    deadline_value = TaskWithTickInStreamSerializer(many = True)

    class Meta:
        model = TaskWithTick
        fields = '__all__'




class TaskWithKeywordInStreamSerializer(serializers.ModelSerializer):


    class Meta:
        model = TaskWithKeywordInStream
        fields = '__all__'


class TaskWithKeywordSectionForStreamSerializer(serializers.ModelSerializer):
    deadline_value = TaskWithKeywordInStreamSerializer(many = True)

    class Meta:
        model = TaskWithKeyword
        fields = '__all__'




class ClassmatesCheckedTaskInStreamSerializer(serializers.ModelSerializer):


    class Meta:
        model = ClassmatesCheckedTaskInStream
        fields = '__all__'


class ClassmatesCheckedTaskForStreamSerializer(serializers.ModelSerializer):
    deadline_value = ClassmatesCheckedTaskInStreamSerializer(many = True)

    class Meta:
        model = ClassmatesCheckedTask
        fields = '__all__'




class TaskWithTeacherCheckInStreamSerializer(serializers.ModelSerializer):


    class Meta:
        model = TaskWithTeacherCheckInStream
        fields = '__all__'


class TaskWithTeacherCheckInSectionForStreamSerializer(serializers.ModelSerializer):
    deadline_value = TaskWithTeacherCheckInStreamSerializer(many = True)

    class Meta:
        model = TaskWithTeacherCheck
        fields = '__all__'

"""
Конец блока дедлайнов
"""


class SectionInCourseForStreamSerializer(serializers.ModelSerializer):
    task_with_tick_in_section = TaskWithTickInSectionForStreamSerializer(many = True)
    # task_with_teacher_check_in_section = TaskWithTeacherCheckInSectionForStreamSerializer(many = True)
    task_with_keyword_in_section = TaskWithKeywordSectionForStreamSerializer(many = True)
    # lassmates_in_section = ClassmatesCheckedTaskForStreamSerializer(many = True)

    class Meta:
        model = Section
        fields = '__all__'


class StudentGroupForStreamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentGroup
        fields = ("id", "title", "number", "year_of_receipt")


class StudentStreamForCourseInStreamSerializer(serializers.ModelSerializer):
    #groups = StudentGroupForStreamSerializer(many=True)
    groups = StudentGroupForStreamsSerializer(
        many=True)

    class Meta:
        model = StudentStream
        fields = ("id", "title", "groups", 'deadline_date', 'start_date')


class CourseInStreamSerializer(serializers.ModelSerializer):
    sections_in_course = SectionInCourseForStreamSerializer(many = True)
    owner = TeacherSerializer()
    #streams_on_a_course = serializers.SerializerMethodField('get_id_of_wpcb')
    #streams_on_a_course = StudentStreamForCourseInStreamSerializer(many = True)

    class Meta:
        model = Course
        fields = '__all__'

    # def get_id_of_wpcb(self, obj):
    #
    #     work_program = StudentStream.objects.filter(work_program_in_change_block = obj.id)
    #     serializers = StudentStreamForCourseInStreamSerializer(work_program, many=True, context={'parent_cb_id': obj.id})
    #     return serializers.data


class StudentStreamListSerializer(serializers.ModelSerializer):
    #groups = StudentGroupForStreamSerializer(many=True)
    groups = StudentGroupForStreamsSerializer(
        many=True)
    course_access = CourseInStreamSerializer(many=True)
    owner = TeacherSerializer()

    class Meta:
        model = StudentStream
        fields = ("id", "title", "groups", "course_access", 'deadline_date', 'start_date', 'owner')


class StudentInCourseCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = StudentInCourse
        fields = '__all__'


class StudentInCourseSerializer(serializers.ModelSerializer):


    class Meta:
        model = StudentInCourse
        fields = '__all__'


"""
Блок новости
"""


class CourseNewsCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = CourseNews
        fields = '__all__'


class CourseNewsSerializer(serializers.ModelSerializer):


    class Meta:
        model = CourseNews
        fields = '__all__'

"""
Конец блока новости
"""