from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.contrib.postgres.search import SearchVector

from .models import \
    StudentStream, StudentGroup, GroupInStream, Course, Lesson, StudentLessonResult, \
    ClassmatesCheckedTask, TaskOption, StudentResult, Check, Section, TaskWithTick, \
    TaskWithTickOption, TaskWithTickStudentResult, TaskWithKeywordResult, \
    TaskWithClassmatesCheckResult, TaskWithTeacherCheckResult, TaskWithKeyword, \
    TaskWithClassmatesCheck, TaskWithTeacherCheck, TaskWithKeywordOption

from .serializers import \
    ClassmatesCheckedTaskSerializer, TaskOptionSerializer, StudentResultSerializer, \
    CheckSerializer, TaskSerializer, UserResultsSerializer
    
from .serializers import StudentStreamSerializer, StudentGroupSerializer, \
    StudentGroupSerializer, GroupMemberSerializer, CourseSerializer, \
    LessonSerializer, StudentLessonResultSerializer, \
    CreateStudentLessonResultSerializer, SectionSerializer, \
    CreateSectionSerializer, TaskWithTickSerializer, CreateTaskWithTickSerializer, \
    TaskWithTickOptionSerializer, CreateTaskWithTickOptionSerializer, \
    TaskWithTickStudentResult, TaskWithTickStudentResultSerializer, \
    CreateTaskWithTickStudentResultSerializer, StudentSerializer, \
    TaskWithKeywordSerializer, CreateTaskWithKeywordSerializer, \
    TaskWithKeywordOptionSerializer, CreateTaskWithKeywordOptionSerializer, \
    TaskWithKeywordResultSerializer, CreateTaskWithKeywordResultSerializer

from .utils import get_object_or_none


User = get_user_model()


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = User.objects.filter(role='student')
        last_name = self.request.query_params.get('last_name', None)
        group_id = self.request.query_params.get('group_id', None)
        stream_id = self.request.query_params.get('stream_id', None)

        if last_name is not None:
            queryset = queryset.filter(last_name__istartswith=last_name)

        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)

        if stream_id is not None:
            queryset = queryset.filter(group__streams__id=stream_id)

        return queryset


class StudentStreamListCreateView(generics.ListCreateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamSerializer
    permission_classes = [permissions.AllowAny]


class StudentStreamRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamSerializer
    permission_classes = [permissions.AllowAny]


class GroupInStreamListCreateView(generics.ListCreateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        stream = get_object_or_none(StudentStream, {'id': pk})

        if stream is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(stream.groups, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        stream = get_object_or_none(StudentStream, {'id': pk})

        if stream is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if 'group_id' not in request.data:
            return Response({'group_id': ['Отсутствует обязательное поле group_id']},
                            status=status.HTTP_400_BAD_REQUEST)

        group = get_object_or_none(StudentGroup, {'id': request.data['group_id']})

        if group is None:
            return Response({'group_id': ['Группа с указанным group_id не была найдена']},
                            status=status.HTTP_404_NOT_FOUND)

        group_in_stream = GroupInStream(group=group, stream=stream)
        group_in_stream.save()

        serializer = self.serializer_class(stream.groups, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentGroupListCreateView(generics.ListCreateAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny]


class StudentGroupRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny]


class StudentGroupMembersListCreateView(generics.ListCreateAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        student_group = self.queryset.get(id=pk)
        members = student_group.members.all()
        serializer = self.serializer_class(members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        student_group = self.queryset.get(id=pk)

        if 'user_id' not in request.data:
            return Response({'user_id': ['Отсутствует обязательное поле user_id']},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            student_group.add_member(request.data['user_id'])
        except ObjectDoesNotExist:
            return Response({'user_id': ['Пользователь с указанным user_id не был найден']},
                            status=status.HTTP_404_NOT_FOUND)

        members = student_group.members.all()
        serializer = self.serializer_class(members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_class = permissions.AllowAny


class CourseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_class = permissions.AllowAny


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_class = permissions.AllowAny


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_class = permissions.AllowAny


class LessonRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_class = permissions.AllowAny


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_class = permissions.AllowAny


class StudentLessonResultCreateView(generics.CreateAPIView):
    queryset = StudentLessonResult.objects.all()
    serializer_class = CreateStudentLessonResultSerializer
    permission_class = permissions.AllowAny


class StudentLessonResultRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentLessonResult.objects.all()
    serializer_class = StudentLessonResultSerializer
    permission_class = permissions.AllowAny


class StudentLessonResultListView(generics.ListAPIView):
    queryset = StudentLessonResult.objects.all()
    serializer_class = StudentLessonResultSerializer


class ClassmatesCheckedTaskListCreateView(generics.ListCreateAPIView):
    queryset = ClassmatesCheckedTask.objects.all()
    serializer_class = ClassmatesCheckedTaskSerializer
    permission_classes = [permissions.AllowAny]


class ClassmatesCheckedTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassmatesCheckedTask.objects.all()
    serializer_class = ClassmatesCheckedTaskSerializer
    permission_classes = [permissions.AllowAny]


class TaskOptionListCreateView(generics.ListCreateAPIView):
    queryset = TaskOption.objects.all()
    serializer_class = TaskOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskOptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskOption.objects.all()
    serializer_class = TaskOptionSerializer
    permission_classes = [permissions.AllowAny]


class StudentResultListCreateView(generics.ListCreateAPIView):
    queryset = StudentResult.objects.all()
    serializer_class = StudentResultSerializer


class StudentResultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentResult.objects.all()
    serializer_class = StudentResultSerializer
    permission_classes = [permissions.AllowAny]


class CheckListCreateView(generics.ListCreateAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [permissions.AllowAny]


class CheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [permissions.AllowAny]
    permission_class = permissions.AllowAny


class SectionCreateView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = CreateSectionSerializer
    permission_class = permissions.AllowAny


class SectionRetrieveView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_class = permissions.AllowAny


class SectionUpdateView(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = CreateSectionSerializer
    permission_class = permissions.AllowAny


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_class = permissions.AllowAny


class TaskWithTickCreateView(generics.CreateAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = CreateTaskWithTickSerializer
    permission_class = permissions.AllowAny


class TaskWithTickRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = TaskWithTickSerializer
    permission_class = permissions.AllowAny


class TaskWithTickUpdateView(generics.UpdateAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = CreateTaskWithTickSerializer
    permission_class = permissions.AllowAny


class TaskWithTickListView(generics.ListAPIView):
    serializer_class = TaskWithTickSerializer
    permission_class = permissions.AllowAny

    def get_queryset(self):
        queryset = TaskWithTick.objects.all()
        params = self.request.query_params

        section = params.get('section', None)
        # фильтр по секциям, имеет смысл на фронте получать
        # все секции из соответствующего эндпоинта и
        # класть их в select, в качестве value использовать
        # первичный ключ секции, а в качестве текста внутри
        # опции именно название
        search = params.get('search', None)

        if section:
            queryset = queryset.filter(section__id=section)

        if search:
            queryset = queryset.annotate(
                search=SearchVector('title', 'description'),
            ).filter(search=search)

        return queryset


class TaskWithTickOptionCreateView(generics.CreateAPIView):
    queryset = TaskWithTickOption.objects.all()
    serializer_class = CreateTaskWithTickOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithTickOptionRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithTickOption.objects.all()
    serializer_class = TaskWithTickOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithTickOptionUpdateView(generics.UpdateAPIView):
    queryset = TaskWithTickOption.objects.all()
    serializer_class = CreateTaskWithTickOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithTickOptionListView(generics.ListAPIView):
    queryset = TaskWithTickOption.objects.all()
    serializer_class = TaskWithTickOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithTickStudentResultCreateView(generics.CreateAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = CreateTaskWithTickStudentResultSerializer
    permission_class = permissions.AllowAny


class TaskWithTickStudentResultRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = TaskWithTickStudentResultSerializer
    permission_class = permissions.AllowAny


class TaskWithTickStudentResultUpdateView(generics.UpdateAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = CreateTaskWithTickStudentResultSerializer
    permission_class = permissions.AllowAny


class TaskWithTickStudentResultListView(generics.ListAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = TaskWithTickStudentResultSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordCreateView(generics.CreateAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = CreateTaskWithKeywordSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordUpdateView(generics.UpdateAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = CreateTaskWithKeywordSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordListView(generics.ListAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordOptionCreateView(generics.CreateAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = CreateTaskWithKeywordOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordOptionRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = TaskWithKeywordOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordOptionUpdateView(generics.UpdateAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = CreateTaskWithKeywordOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordOptionListView(generics.ListAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = TaskWithKeywordOptionSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordResultCreateView(generics.CreateAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = CreateTaskWithKeywordResultSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordResultRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = TaskWithKeywordResultSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordResultUpdateView(generics.UpdateAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = CreateTaskWithKeywordResultSerializer
    permission_class = permissions.AllowAny


class TaskWithKeywordResultListView(generics.ListAPIView):
    serializer_class = TaskWithKeywordResultSerializer
    permission_class = permissions.AllowAny

    def get_queryset(self):
        queryset = TaskWithKeywordResult.objects.all()

        params = self.request.query_params

        username = params.get('username', None)
        is_perform = params.get('is_perform', None)

        if username:
            queryset = queryset.filter(user__username=username)

        # if is performed
        if is_perform == '1':
            queryset = queryset.filter(perform=True)

        # if isn't performed
        if is_perform == '0':
            queryset = queryset.filter(perform=False)

        return queryset


class StatisticsTaskByStudent(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    MODEL_BY_TYPE = {
        'with_keyword': TaskWithKeyword,
        'with_teacher_check': TaskWithTeacherCheck,
        'with_classmates_check': TaskWithClassmatesCheck,
    }

    def get_serializer_class(self):
        task_type = self.kwargs['task_type']
        model = self.MODEL_BY_TYPE.get(task_type, None)

        if model is not None:
            TaskSerializer.Meta.model = model
            return TaskSerializer

        raise Exception(f'Unknown type of task: {task_type}')

    def get_queryset(self):
        task_type = self.kwargs['task_type']
        section_id = self.kwargs['section_id']

        model = self.MODEL_BY_TYPE.get(task_type, None)

        if model is None:
            raise Exception(f'Unknown type of task: {task_type}')

        queryset = model.objects.filter(section_id=section_id)

        return queryset


class StatisticsStudentResults(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    MODEL_BY_TYPE = {
        'with_keyword': TaskWithKeywordResult,
        'with_teacher_check': TaskWithTeacherCheckResult,
        'with_classmates_check': TaskWithClassmatesCheckResult,
    }

    def get_serializer(self, data, many):
        task_type = self.kwargs['task_type']
        section_id = self.kwargs['section_id']
        task_result_model = self.MODEL_BY_TYPE.get(task_type, None)

        if task_result_model is None:
            raise Exception(f'Unknown type of task: {task_result_model}')

        return UserResultsSerializer(data, many=many, task_result_model=task_result_model,
                                     section_id=section_id)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = User.objects.filter(id=user_id)

        return queryset
