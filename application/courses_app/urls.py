from django.urls import path
from .views import StudentStreamListCreateView, StudentStreamRetrieveUpdateView,\
    StudentGroupListCreateView, StudentGroupRetrieveUpdateView, \
    StudentGroupMembersListCreateView, GroupInStreamListCreateView, StudentListView
from .views import CourseCreateView, CourseRetrieveUpdateView, LessonCreateView, \
    LessonRetrieveUpdateView, StudentLessonResultCreateView, \
    StudentLessonResultRetrieveUpdateView, CourseListView, \
    LessonListView, StudentLessonResultListView
from .views import ClassmatesCheckedTaskListCreateView, ClassmatesCheckedTaskRetrieveUpdateDestroyView
from .views import TaskOptionListCreateView, TaskOptionRetrieveUpdateDestroyView
from .views import StudentResultListCreateView, StudentResultRetrieveUpdateDestroyView
from .views import SectionCreateView, SectionListView, SectionRetrieveView, \
    SectionUpdateView, TaskWithTickCreateView, TaskWithTickListView
from .views import TaskWithTickRetrieveView, TaskWithTickUpdateView, \
    TaskWithTickOptionCreateView, TaskWithTickOptionListView, \
    TaskWithTickOptionRetrieveView, TaskWithTickOptionUpdateView, \
    TaskWithTickStudentResultCreateView, TaskWithTickStudentResultRetrieveView, \
    TaskWithTickStudentResultUpdateView, TaskWithTickStudentResultListView, \
    StatisticsTaskByStudent, StatisticsStudentResults

# task with keyword views
from .views import TaskWithKeywordCreateView, TaskWithKeywordRetrieveView, \
    TaskWithKeywordUpdateView, TaskWithKeywordListView, TaskWithKeywordOptionCreateView, \
    TaskWithKeywordOptionRetrieveView, TaskWithKeywordOptionUpdateView, \
    TaskWithKeywordOptionListView, TaskWithKeywordResultCreateView, \
    TaskWithKeywordResultRetrieveView, TaskWithKeywordResultUpdateView, \
    TaskWithKeywordResultListView


app_name = "courses_app"

urlpatterns = [
    path('students/', StudentListView.as_view()),

    path('streams/', StudentStreamListCreateView.as_view()),
    path('streams/<int:pk>/', StudentStreamRetrieveUpdateView.as_view()),
    path('streams/<int:pk>/groups/', GroupInStreamListCreateView.as_view()),

    path('groups/', StudentGroupListCreateView.as_view()),
    path('groups/<int:pk>/', StudentGroupRetrieveUpdateView.as_view()),
    path('groups/<int:pk>/members/', StudentGroupMembersListCreateView.as_view()),

    path('courses/add/', CourseCreateView.as_view()),
    path('courses/all/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseRetrieveUpdateView.as_view()),

    path('classmates/tasks/', ClassmatesCheckedTaskListCreateView.as_view()),
    path('classmates/tasks/<int:pk>/', ClassmatesCheckedTaskRetrieveUpdateDestroyView.as_view()),

    path('classmates/options/', TaskOptionListCreateView.as_view()),
    path('classmates/options/<int:pk>/', TaskOptionRetrieveUpdateDestroyView.as_view()),

    path('classmates/results/', StudentResultListCreateView.as_view()),
    path('classmates/results/<int:pk>/', StudentResultRetrieveUpdateDestroyView.as_view()),

    path('classmates/checks/', StudentResultListCreateView.as_view()),
    path('classmates/checks/<int:pk>/', StudentResultRetrieveUpdateDestroyView.as_view()),

    path('lessons/add/', LessonCreateView.as_view()),
    path('lessons/all/', LessonListView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveUpdateView.as_view()),

    path('lessons/results/add/', StudentLessonResultCreateView.as_view()),
    path('lessons/results/all/', StudentLessonResultListView.as_view()),
    path('lessons/results/<int:pk>/', StudentLessonResultRetrieveUpdateView.as_view()),

    path('courses/sections/add/', SectionCreateView.as_view()),
    path('courses/sections/all/', SectionListView.as_view()),
    path('courses/sections/<int:pk>/', SectionRetrieveView.as_view()),
    path('courses/sections/update/<int:pk>/', SectionUpdateView.as_view()),

    path('tasks/with_tick/add/', TaskWithTickCreateView.as_view()),
    path('tasks/with_tick/all/', TaskWithTickListView.as_view()),
    path('tasks/with_tick/<int:pk>/', TaskWithTickRetrieveView.as_view()),
    path('tasks/with_tick/update/<int:pk>/', TaskWithTickUpdateView.as_view()),

    path('tasks/with_tick/options/add/', TaskWithTickOptionCreateView.as_view()),
    path('tasks/with_tick/options/all/', TaskWithTickOptionListView.as_view()),
    path('tasks/with_tick/options/<int:pk>/', TaskWithTickOptionRetrieveView.as_view()),
    path('tasks/with_tick/options/update/<int:pk>/', TaskWithTickOptionUpdateView.as_view()),

    path('tasks/with_tick/results/add/', TaskWithTickStudentResultCreateView.as_view()),
    path('tasks/with_tick/results/all/', TaskWithTickStudentResultListView.as_view()),
    path('tasks/with_tick/results/<int:pk>/', TaskWithTickStudentResultRetrieveView.as_view()),
    path('tasks/with_tick/results/update/<int:pk>/', TaskWithTickStudentResultUpdateView.as_view()),

    path('tasks/with_keyword/add/', TaskWithKeywordCreateView.as_view()),
    path('tasks/with_keyword/all/', TaskWithKeywordListView.as_view()),
    path('tasks/with_keyword/<int:pk>/', TaskWithKeywordRetrieveView.as_view()),
    path('tasks/with_keyword/update/<int:pk>/', TaskWithKeywordUpdateView.as_view()),

    path('tasks/with_keyword/options/add/', TaskWithKeywordOptionCreateView.as_view()),
    path('tasks/with_keyword/options/all/', TaskWithKeywordOptionListView.as_view()),
    path('tasks/with_keyword/options/<int:pk>/', TaskWithKeywordOptionRetrieveView.as_view()),
    path('tasks/with_keyword/options/update/<int:pk>/', TaskWithKeywordOptionUpdateView.as_view()),

    path('tasks/with_keyword/results/add/', TaskWithKeywordResultCreateView.as_view()),
    path('tasks/with_keyword/results/all/', TaskWithKeywordResultListView.as_view()),
    path('tasks/with_keyword/results/<int:pk>/', TaskWithKeywordResultRetrieveView.as_view()),
    path('tasks/with_keyword/results/update/<int:pk>/', TaskWithKeywordResultUpdateView.as_view()),

    path('statistics/sections/<int:section_id>/tasks/<str:task_type>/results/', StatisticsTaskByStudent.as_view()),
    path(
        'statistics/sections/<int:section_id>/tasks/<str:task_type>/students/<int:user_id>/results/',
        StatisticsStudentResults.as_view(),
    ),
]
