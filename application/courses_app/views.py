from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.contrib.postgres.search import SearchVector

from random import choice

from .models import \
    StudentStream, StudentGroup, GroupInStream, Course, Lesson, StudentLessonResult, \
    ClassmatesCheckedTask, TaskOption, StudentResult, Check, Section, TaskWithTick, \
    TaskWithTickStudentResult, TaskWithKeywordResult, \
    TaskWithTeacherCheckResult, TaskWithKeyword, TaskWithTeacherCheckOption, \
    TaskWithTeacherCheck, TaskWithTeacherCheckCheck, TaskWithKeywordOption, TaskWithTickInStream, StudentInCourse


from .models import ClassmatesCheckedTaskInStream, TaskWithTeacherCheckInStream, TaskWithKeywordInStream


from .serializers import \
    ClassmatesCheckedTaskSerializer, TaskOptionSerializer, StudentResultSerializer, \
    CheckSerializer, TaskWithTeacherCheckSerializer, TaskWithTeacherCheckOptionSerializer, \
    TaskWithTeacherCheckResultSerializer, TaskWithTeacherCheckCheckSerializer, \
    TaskSerializer, UserResultsSerializer
    
from .serializers import StudentStreamSerializer, StudentGroupSerializer, \
    StudentGroupSerializer, GroupMemberSerializer, \
    CourseSerializer, CourseListSerializer, \
    LessonSerializer, StudentLessonResultSerializer, \
    CreateStudentLessonResultSerializer, SectionSerializer, \
    CreateSectionSerializer, TaskWithTickSerializer, CreateTaskWithTickSerializer, \
    TaskWithTickStudentResult, TaskWithTickStudentResultSerializer, \
    CreateTaskWithTickStudentResultSerializer, StudentSerializer, CourseCreateSerializer, \
    TaskWithTeacherCreateCheckSerializer, StudentStreamCreateSerializer, \
    StudentInCourseSerializer, StudentInCourseCreateSerializer

from .serializers import TaskWithKeywordCreateSerializer, TaskWithKeywordSerializer, TaskWithKeywordOptionSerializer, TaskWithKeywordResultSerializer, CourseInStreamSerializer, TaskWithTickInStreamSerializer


from .serializers import TaskWithKeywordInStreamSerializer, TaskWithTeacherCheckInStreamSerializer, ClassmatesCheckedTaskInStreamSerializer, StudentStreamListSerializer


from .utils import get_object_or_none

from rest_framework import filters

from collections import OrderedDict


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

StudentStreamListSerializer


class GroupInStreamNewListView(generics.ListAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamListSerializer
    permission_classes = [permissions.AllowAny]


class GroupInStreamNewCreateView(generics.CreateAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamCreateSerializer
    permission_classes = [permissions.AllowAny]


class GroupInStreamNewDetailView(generics.RetrieveAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamListSerializer
    permission_classes = [permissions.AllowAny]


class GroupInStreamNewDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentStream.objects.all()
    serializer_class = StudentStreamCreateSerializer
    permission_classes = [permissions.AllowAny]

class TaskWithTickInStreamCreateView(generics.CreateAPIView):
    queryset = TaskWithTickInStream.objects.all()
    serializer_class = TaskWithTickInStreamSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickInStreamDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithTickInStream.objects.all()
    serializer_class = TaskWithTickInStreamSerializer
    permission_classes = [permissions.AllowAny]


class ClassmatesCheckedTaskInStreamCreateView(generics.CreateAPIView):
    queryset = ClassmatesCheckedTaskInStream.objects.all()
    serializer_class = ClassmatesCheckedTaskInStreamSerializer
    permission_classes = [permissions.AllowAny]


class ClassmatesCheckedTaskInStreamDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassmatesCheckedTaskInStream.objects.all()
    serializer_class = ClassmatesCheckedTaskInStreamSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckInStreamCreateView(generics.CreateAPIView):
    queryset = TaskWithTeacherCheckInStream.objects.all()
    serializer_class = TaskWithTeacherCheckInStreamSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckInStreamDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithTeacherCheckInStream.objects.all()
    serializer_class = TaskWithTeacherCheckInStreamSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordInStreamCreateView(generics.CreateAPIView):
    queryset = TaskWithKeywordInStream.objects.all()
    serializer_class = TaskWithKeywordInStreamSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordInStreamDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithKeywordInStream.objects.all()
    serializer_class = TaskWithKeywordInStreamSerializer
    permission_classes = [permissions.AllowAny]


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


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_class = permissions.AllowAny
    permission_classes = [permissions.AllowAny]


# class CourseCreateAPIView(generics.CreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     #permission_class = permissions.AllowAny
#     permission_classes = [permissions.AllowAny]
#
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    permission_classes = [permissions.AllowAny]


class CourseForStudentListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]


    def list(self, request, **kwargs):
        """
        Вывод курсов, который проходимт этот юзер
        """
        queryset = Course.objects.none()
        group = self.request.user.group
        course_in_streams_titles = {}
        try:
            streams = group.streams.all()
            for stream in streams:
                print (stream.title, stream.course_access.all())
                queryset = queryset.union(stream.course_access.all())
                for course in stream.course_access.all():
                    print (course.id)
                    course_in_streams_titles.update({course.id:stream.title})
        except:
            pass
        print (course_in_streams_titles)
        serializer = CourseInStreamSerializer(queryset, many=True)
        data = []

        for course in serializer.data:
            all_tasks = 0
            student_tasks = 0
            newdata = dict(course)

            try:
                for section in course["sections_in_course"]:
                    for task in section["task_with_tick_in_section"]:
                        all_tasks +=1
                        if TaskWithTickStudentResult.objects.filter(user = self.request.user, task_with_tick_id = task["id"], perform = True):
                            student_tasks +=1

                    for task in section["task_with_keyword_in_section"]:
                        all_tasks +=1
                        if TaskWithKeywordResult.objects.filter(user = self.request.user, option__task_id = task["id"], perform = True):
                            student_tasks +=1


                try:
                    newdata.update({"status": StudentInCourse.objects.get(course = newdata["id"], user = self.request.user).status, "all_tasks": all_tasks, "student_tasks": student_tasks})
                except:
                    newdata.update({"status": "1", "all_tasks": all_tasks, "student_tasks": student_tasks})
                newdata.update({"course_in_streams_title": course_in_streams_titles[course["id"]]})

                del course_in_streams_titles[course["id"]]

            except:
                pass

            group = self.request.user.group
            newdata.update({"stream_id": group.streams.filter(course_access = course["id"])[0].id})
            newdata=OrderedDict(newdata)
            data.append(newdata)
        return Response(data)
        try:
            queryset = Course.objects.none()
            group = self.request.user.group
            streams = group.streams.all()
            for stream in streams:
                queryset = queryset.union(stream.course_access.all())
            serializer = CourseInStreamSerializer(queryset, many=True)
            newdata = dict(serializer.data[0])
            return Response(serializer.data)
        except:
            return Response(status=400)


class CourseForStudentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CourseInStreamSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        course_in_streams_titles = {}
        try:
            instance = self.get_object()
        except (Course.DoesNotExist, KeyError):
            return Response({"error": "Requested Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        print ('her')
        newdata = dict(serializer.data)
        #try:
        for section in newdata["sections_in_course"]:
            tasks_in_sections = 0
            completed_task_in_section = 0
            for task in section["task_with_tick_in_section"]:
                tasks_in_sections +=1
                if TaskWithTickStudentResult.objects.filter(user = self.request.user, task_with_tick_id = task["id"], perform = True):
                    print ("dfdfdftrue")
                    task.update({"status": "1"})
                    task.update({"task_result_id": TaskWithTickStudentResult.objects.filter(user = self.request.user, task_with_tick_id = task["id"], perform = True)[0].id})
                    completed_task_in_section +=1
                elif TaskWithTickStudentResult.objects.filter(user = self.request.user, task_with_tick_id = task["id"], perform = False):
                    task.update({"status": "0"})
                    task.update({"task_result_id": TaskWithTickStudentResult.objects.filter(user = self.request.user, task_with_tick_id = task["id"], perform = False)[0].id})
                else:
                    task.update({"status": None})


            for task in section["task_with_keyword_in_section"]:
                tasks_in_sections +=1
                if TaskWithKeywordResult.objects.filter(user = self.request.user, option__task_id = task["id"], perform = True):
                    print ("dfdfdftrue")
                    task.update({"status": "1"})
                    task.update({"task_result_id": TaskWithKeywordResult.objects.filter(user = self.request.user, option__task_id = task["id"], perform = True)[0].id})
                    completed_task_in_section +=1
                elif TaskWithKeywordResult.objects.filter(user = self.request.user, option__task_id = task["id"], perform = False):
                    task.update({"status": "0"})
                    task.update({"task_result_id": TaskWithKeywordResult.objects.filter(user = self.request.user, option__task_id = task["id"], perform = False)[0].id})
                else:
                    task.update({"status": None})

                """
                Остальные задания кроме галочки
                """

            section.update({"tasks_in_sections": tasks_in_sections})
            section.update({"completed_task_in_section": completed_task_in_section})




        try:
            newdata.update({"status": StudentInCourse.objects.get(course = newdata["id"], user = self.request.user).status})
        except:
            newdata.update({"status": "1"})


        group = self.request.user.group
        newdata.update({"stream_title": group.streams.filter(course_access = serializer.data["id"])[0].title})
        newdata.update({"stream_start_date": group.streams.filter(course_access = serializer.data["id"])[0].start_date})
        newdata.update({"stream_deadline_date": group.streams.filter(course_access = serializer.data["id"])[0].deadline_date})

        # except:
        #     pass



        newdata=OrderedDict(newdata)

        return Response(newdata)



class CourseInStreamsListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]


    def list(self, request, **kwargs):
        """
        Вывод курсов, которые применены в потоках
        """

        try:
            queryset = Course.objects.filter(id__in = StudentStream.objects.all().values('course_access'))
            serializer = CourseInStreamSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(status=400)


class CourseInStreamsByIdListAPIView(generics.ListAPIView):
    serializer_class = CourseInStreamSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]


    def list(self, request, **kwargs):
        """
        Вывод курсов, которые применены в потоках
        """
        queryset = Course.objects.filter(streams_on_a_course__id = self.kwargs['stream_id']).distinct()
        print (queryset)
        serializer = CourseInStreamSerializer(queryset, many = True)
        return Response(serializer.data)
        # try:(
        #     queryset = Course.objects.filter(id__in = StudentStream.objects.all().values('course_access'))
        #     serializer = CourseListSerializer(queryset, many=True)
        #     return Response(serializer.data)
        # except:
        #     return Response(status=400)



class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer
    queryset = Course.objects.all()
    permission_classes = [permissions.AllowAny]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseDestroyView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class CourseDetailsView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]


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


class TaskWithTeacherCheckListCreateView(generics.ListCreateAPIView):
    queryset = TaskWithTeacherCheck.objects.all()
    serializer_class = TaskWithTeacherCreateCheckSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithTeacherCheck.objects.all()
    serializer_class = TaskWithTeacherCheckSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckOptionListCreateView(generics.ListCreateAPIView):
    queryset = TaskWithTeacherCheckOption.objects.all()
    serializer_class = TaskWithTeacherCheckOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckOptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithTeacherCheckOption.objects.all()
    serializer_class = TaskWithTeacherCheckOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckResultListCreateView(generics.ListCreateAPIView):
    queryset = TaskWithTeacherCheckResult.objects.all()
    serializer_class = TaskWithTeacherCheckResultSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckResultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithTeacherCheckResult.objects.all()
    serializer_class = TaskWithTeacherCheckResultSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckCheckListCreateView(generics.ListCreateAPIView):
    queryset = TaskWithTeacherCheckCheck.objects.all()
    serializer_class = TaskWithTeacherCheckCheckSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTeacherCheckCheckRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithTeacherCheckCheck.objects.all()
    serializer_class = TaskWithTeacherCheckCheckSerializer
    permission_classes = [permissions.AllowAny]


class SectionCreateView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = CreateSectionSerializer
    permission_classes = [permissions.AllowAny]


class SectionRetrieveView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]


class SectionUpdateView(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = CreateSectionSerializer
    permission_classes = [permissions.AllowAny]


class SectionDeleteView(generics.DestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = CreateSectionSerializer
    permission_classes = [permissions.AllowAny]


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]


class SectionInCourseListView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]


    def list(self, request, **kwargs):
        """
        Вывод всех результатов для одной рабочей программы по id
        """
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Section.objects.filter(course__id=self.kwargs['course_id'])
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)


class TaskWithTickCreateView(generics.CreateAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = CreateTaskWithTickSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = TaskWithTickSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickUpdateView(generics.UpdateAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = CreateTaskWithTickSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickDeleteView(generics.DestroyAPIView):
    queryset = TaskWithTick.objects.all()
    serializer_class = CreateTaskWithTickSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickListView(generics.ListAPIView):
    serializer_class = TaskWithTickSerializer
    permission_classes = [permissions.AllowAny]

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


# class TaskWithTickOptionCreateView(generics.CreateAPIView):
#     queryset = TaskWithTickOption.objects.all()
#     serializer_class = CreateTaskWithTickOptionSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# class TaskWithTickOptionRetrieveView(generics.RetrieveAPIView):
#     queryset = TaskWithTickOption.objects.all()
#     serializer_class = TaskWithTickOptionSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# class TaskWithTickOptionUpdateView(generics.UpdateAPIView):
#     queryset = TaskWithTickOption.objects.all()
#     serializer_class = CreateTaskWithTickOptionSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# class TaskWithTickOptionListView(generics.ListAPIView):
#     queryset = TaskWithTickOption.objects.all()
#     serializer_class = TaskWithTickOptionSerializer
#     permission_classes = [permissions.AllowAny]


class TaskWithTickStudentResultCreateView(generics.CreateAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = CreateTaskWithTickStudentResultSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickStudentResultRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = TaskWithTickStudentResultSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickStudentResultUpdateView(generics.UpdateAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = CreateTaskWithTickStudentResultSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithTickStudentResultListView(generics.ListAPIView):
    queryset = TaskWithTickStudentResult.objects.all()
    serializer_class = TaskWithTickStudentResultSerializer
    permission_classes = [permissions.AllowAny]


class StatisticsTaskByStudent(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    MODEL_BY_TYPE = {
        'with_keyword': TaskWithKeyword,
        'with_teacher_check': TaskWithTeacherCheck,
        'with_classmates_check': ClassmatesCheckedTask,
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
        'with_classmates_check': ClassmatesCheckedTask,
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


"""
Задания с ключевым словом
"""


class TaskWithKeywordCreateView(generics.CreateAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordCreateSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordUpdateView(generics.UpdateAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordCreateSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordDeleteView(generics.DestroyAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordCreateSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordListView(generics.ListAPIView):
    queryset = TaskWithKeyword.objects.all()
    serializer_class = TaskWithKeywordSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordOptionCreateView(generics.CreateAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = TaskWithKeywordOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordOptionListView(generics.ListAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = TaskWithKeywordOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordOptionRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = TaskWithKeywordOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordOptionUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskWithKeywordOption.objects.all()
    serializer_class = TaskWithKeywordOptionSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordStudentResultListView(generics.ListAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = TaskWithKeywordResultSerializer
    permission_classes = [permissions.AllowAny]


class TaskWithKeywordStudentResultUpdateView(generics.UpdateAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = TaskWithKeywordResultSerializer
    permission_classes = [permissions.AllowAny]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.option.keyword)
        if instance.option.keyword == request.data["user_keyword"]:
            instance.perform = True
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "solution is correct"})
            else:
                return Response({"message": "wrong_data"})

        else:
            return Response({"message": "solution is not correct"})


class TaskWithKeywordStudentResultCreateView(generics.CreateAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = TaskWithKeywordResultSerializer
    permission_classes = [permissions.AllowAny]


    def create(self, request, *args, **kwargs):
        options = TaskWithKeywordOption.objects.all()
        options_ids = [friend.id for friend in options]
        request.data.update({"option": choice(options_ids),"user":request.user.id})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print (request.data["option"])
        options = TaskWithKeywordOption.objects.get(id = request.data["option"])
        serializer_for_option = TaskWithKeywordOptionSerializer(options)
        print (serializer_for_option.data)
        return Response(serializer_for_option.data, status=status.HTTP_201_CREATED, headers=headers)


class TaskWithKeywordStudentResultRetrieveView(generics.RetrieveAPIView):
    queryset = TaskWithKeywordResult.objects.all()
    serializer_class = TaskWithKeywordResultSerializer
    permission_classes = [permissions.AllowAny]
"""
Конец блока заданий с ключевым словом
"""

"""
Блок студента в курсе
"""

class StudentInCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentInCourseCreateSerializer
    queryset = StudentInCourse.objects.all()
    permission_classes = [permissions.AllowAny]


    def create(self, request, *args, **kwargs):
        request.data.update({"user":request.user.id})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        for task in TaskWithKeyword.objects.filter(section__course = request.data["course"]):
            options = TaskWithKeywordOption.objects.filter(task = task)
            options_ids = [friend.id for friend in options]
            TaskWithKeywordResult.objects.create(option_id = choice(options_ids),user = self.request.user)
            print ('1')

        for task in TaskWithTick.objects.filter(section__course = request.data["course"]):
            TaskWithTickStudentResult.objects.create(user = self.request.user, task_with_tick = task)
            print ('1')

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




class StudentInCourseListView(generics.ListAPIView):
    queryset = StudentInCourse.objects.all()
    serializer_class = StudentInCourseSerializer
    permission_classes = [permissions.AllowAny]


class StudentInCourseDestroyView(generics.DestroyAPIView):
    queryset = StudentInCourse.objects.all()
    serializer_class = StudentInCourseSerializer
    permission_classes = [permissions.AllowAny]


class StudentInCourseUpdateView(generics.UpdateAPIView):
    queryset = StudentInCourse.objects.all()
    serializer_class = StudentInCourseSerializer
    permission_classes = [permissions.AllowAny]


class StudentInCourseDetailsView(generics.RetrieveAPIView):
    queryset = StudentInCourse.objects.all()
    serializer_class = StudentInCourseSerializer
    permission_classes = [permissions.AllowAny]

"""
Блок студента в курса
"""