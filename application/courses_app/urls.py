from django.urls import path
from .views import StudentStreamListCreateView, StudentStreamRetrieveUpdateView,\
    StudentGroupListCreateView, StudentGroupRetrieveUpdateView, \
    StudentGroupMembersListCreateView, GroupInStreamListCreateView, StudentListView
from .views import LessonCreateView, \
    LessonRetrieveUpdateView, StudentLessonResultCreateView, \
    StudentLessonResultRetrieveUpdateView, \
    LessonListView, StudentLessonResultListView

from .views import CourseCreateAPIView, CourseListAPIView, CourseDetailsView, CourseDestroyView, CourseUpdateView


from .views import ClassmatesCheckedTaskListCreateView, ClassmatesCheckedTaskRetrieveUpdateDestroyView
from .views import TaskOptionListCreateView, TaskOptionRetrieveUpdateDestroyView
from .views import StudentResultListCreateView, StudentResultRetrieveUpdateDestroyView
from .views import CheckListCreateView, CheckRetrieveUpdateDestroyView

from .views import TaskWithTeacherCheckListCreateView, TaskWithTeacherCheckRetrieveUpdateDestroyView
from .views import TaskWithTeacherCheckOptionListCreateView, TaskWithTeacherCheckOptionRetrieveUpdateDestroyView
from .views import TaskWithTeacherCheckResultListCreateView, TaskWithTeacherCheckResultRetrieveUpdateDestroyView
from .views import TaskWithTeacherCheckCheckListCreateView, TaskWithTeacherCheckCheckRetrieveUpdateDestroyView

from .views import SectionCreateView, SectionListView, SectionRetrieveView, SectionInCourseListView, SectionDeleteView, \
    SectionUpdateView, TaskWithTickCreateView, TaskWithTickListView
from .views import TaskWithTickRetrieveView, TaskWithTickUpdateView, TaskWithTickDeleteView, \
    TaskWithTickOptionCreateView, TaskWithTickOptionListView, \
    TaskWithTickOptionRetrieveView, TaskWithTickOptionUpdateView, \
    TaskWithTickStudentResultCreateView, TaskWithTickStudentResultRetrieveView, \
    TaskWithTickStudentResultUpdateView, TaskWithTickStudentResultListView, \
    StatisticsTaskByStudent, StatisticsStudentResults

from .views import TaskWithKeywordRetrieveView, TaskWithKeywordUpdateView, TaskWithKeywordDeleteView, \
    TaskWithKeywordCreateView, TaskWithKeywordListView
    # TaskWithKeywordOptionCreateView, TaskWithKeywordOptionListView, \
    # TaskWithKeywordOptionRetrieveView, TaskWithKeywordOptionUpdateView, \
    # TaskWithKeywordStudentResultCreateView, TaskWithKeywordStudentResultRetrieveView, \
    # TaskWithKeywordStudentResultUpdateView, TaskWithKeywordStudentResultListView, \

app_name = "courses_app"

urlpatterns = [
    path('students/', StudentListView.as_view()),

    path('streams/', StudentStreamListCreateView.as_view()),
    path('streams/<int:pk>/', StudentStreamRetrieveUpdateView.as_view()),
    path('streams/<int:pk>/groups/', GroupInStreamListCreateView.as_view()),

    path('groups/', StudentGroupListCreateView.as_view()),
    path('groups/<int:pk>/', StudentGroupRetrieveUpdateView.as_view()),
    path('groups/<int:pk>/members/', StudentGroupMembersListCreateView.as_view()),

    path('Course', CourseListAPIView.as_view()),
    path('Course/create', CourseCreateAPIView.as_view()),
    path('Course/detail/<int:pk>', CourseDetailsView.as_view()),
    path('Course/delete/<int:pk>', CourseDestroyView.as_view()),
    path('Course/update/<int:pk>', CourseUpdateView.as_view()),

    path('tasks/classmates/tasks/', ClassmatesCheckedTaskListCreateView.as_view()),
    path('tasks/classmates/tasks/<int:pk>/', ClassmatesCheckedTaskRetrieveUpdateDestroyView.as_view()),

    path('tasks/classmates/options/', TaskOptionListCreateView.as_view()),
    path('tasks/classmates/options/<int:pk>/', TaskOptionRetrieveUpdateDestroyView.as_view()),

    path('tasks/classmates/results/', StudentResultListCreateView.as_view()),
    path('tasks/classmates/results/<int:pk>/', StudentResultRetrieveUpdateDestroyView.as_view()),

    path('tasks/classmates/checks/', CheckListCreateView.as_view()),
    path('tasks/classmates/checks/<int:pk>/', CheckRetrieveUpdateDestroyView.as_view()),

    path('tasks/teacher', TaskWithTeacherCheckListCreateView.as_view()),
    path('tasks/teacher/detail/<int:pk>/', TaskWithTeacherCheckRetrieveUpdateDestroyView.as_view()),

    path('tasks/teacher/options/', TaskWithTeacherCheckOptionListCreateView.as_view()),
    path('tasks/teacher/options/<int:pk>/', TaskWithTeacherCheckOptionRetrieveUpdateDestroyView.as_view()),

    path('tasks/teacher/results/', TaskWithTeacherCheckResultListCreateView.as_view()),
    path('tasks/teacher/results/<int:pk>/', TaskWithTeacherCheckResultRetrieveUpdateDestroyView.as_view()),

    path('tasks/teacher/checks/', TaskWithTeacherCheckCheckListCreateView.as_view()),
    path('tasks/teacher/checks/<int:pk>/', TaskWithTeacherCheckCheckRetrieveUpdateDestroyView.as_view()),

    path('lessons/add/', LessonCreateView.as_view()),
    path('lessons/all/', LessonListView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveUpdateView.as_view()),

    path('lessons/results/add/', StudentLessonResultCreateView.as_view()),
    path('lessons/results/all/', StudentLessonResultListView.as_view()),
    path('lessons/results/<int:pk>/', StudentLessonResultRetrieveUpdateView.as_view()),

    path('courses/sections/add/', SectionCreateView.as_view()),
    path('courses/sections/all/', SectionListView.as_view()),
    path('courses/sections/detail/<int:pk>/', SectionRetrieveView.as_view()),
    path('courses/sections/update/<int:pk>/', SectionUpdateView.as_view()),
    path('courses/sections/<int:course_id>/', SectionInCourseListView.as_view()),
    path('courses/sections/delete/<int:pk>', SectionDeleteView.as_view()),

    path('tasks/with_tick/add/', TaskWithTickCreateView.as_view()),
    path('tasks/with_tick/all/', TaskWithTickListView.as_view()),
    path('tasks/with_tick/<int:pk>/', TaskWithTickRetrieveView.as_view()),
    path('tasks/with_tick/update/<int:pk>/', TaskWithTickUpdateView.as_view()),
    path('tasks/with_tick/delete/<int:pk>/', TaskWithTickDeleteView.as_view()),

    path('tasks/with_tick/options/add/', TaskWithTickOptionCreateView.as_view()),
    path('tasks/with_tick/options/all/', TaskWithTickOptionListView.as_view()),
    path('tasks/with_tick/options/<int:pk>/', TaskWithTickOptionRetrieveView.as_view()),
    path('tasks/with_tick/options/update/<int:pk>/', TaskWithTickOptionUpdateView.as_view()),

    path('tasks/with_tick/results/add/', TaskWithTickStudentResultCreateView.as_view()),
    path('tasks/with_tick/results/all/', TaskWithTickStudentResultListView.as_view()),
    path('tasks/with_tick/results/<int:pk>/', TaskWithTickStudentResultRetrieveView.as_view()),
    path('tasks/with_tick/results/update/<int:pk>/', TaskWithTickStudentResultUpdateView.as_view()),

    path('statistics/sections/<int:section_id>/tasks/<str:task_type>/results/', StatisticsTaskByStudent.as_view()),
    path(
        'statistics/sections/<int:section_id>/tasks/<str:task_type>/students/<int:user_id>/results/',
        StatisticsStudentResults.as_view(),
    ),

    path('tasks/with_keyword/add/', TaskWithKeywordCreateView.as_view()),
    path('tasks/with_keyword/all/', TaskWithKeywordListView.as_view()),
    path('tasks/with_keyword/<int:pk>/', TaskWithKeywordRetrieveView.as_view()),
    path('tasks/with_keyword/update/<int:pk>/', TaskWithKeywordUpdateView.as_view()),
    path('tasks/with_keyword/delete/<int:pk>/', TaskWithKeywordDeleteView.as_view()),

    # path('tasks/with_keyword/options/add/', TaskWithKeywordOptionCreateView.as_view()),
    # path('tasks/with_keyword/options/all/', TaskWithKeywordOptionListView.as_view()),
    # path('tasks/with_keyword/options/<int:pk>/', TaskWithKeywordOptionRetrieveView.as_view()),
    # path('tasks/with_keyword/options/update/<int:pk>/', TaskWithKeywordOptionUpdateView.as_view()),
    #
    # path('tasks/with_keyword/results/add/', TaskWithKeywordStudentResultCreateView.as_view()),
    # path('tasks/with_keyword/results/all/', TaskWithKeywordStudentResultListView.as_view()),
    # path('tasks/with_keyword/results/<int:pk>/', TaskWithKeywordStudentResultRetrieveView.as_view()),
    # path('tasks/with_keyword/results/update/<int:pk>/', TaskWithKeywordStudentResultUpdateView.as_view()),

]
