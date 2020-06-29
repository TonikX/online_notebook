from django.urls import path
from .views import StudentStreamListCreateView, StudentStreamRetrieveUpdateView,\
    StudentGroupListCreateView, StudentGroupRetrieveUpdateView, \
    StudentGroupMembersListCreateView, GroupInStreamListCreateView, \
    CourseCreateView, CourseRetrieveUpdateView, LessonCreateView, \
    LessonRetrieveUpdateView, StudentLessonResultCreateView, \
    StudentLessonResultRetrieveUpdateView, CourseListView, \
    LessonListView, StudentLessonResultListView, \
    ClassmatesCheckedTaskListCreateView, ClassmatesCheckedTaskRetrieveUpdateDestroyView, \
    TaskOptionListCreateView, TaskOptionRetrieveUpdateDestroyView, \
    StudentResultListCreateView, StudentResultRetrieveUpdateDestroyView, \
    SectionCreateView, SectionListView, SectionRetrieveView, \
    SectionUpdateView, TaskWithTickCreateView, TaskWithTickListView, \
    TaskWithTickRetrieveView, TaskWithTickUpdateView, \
    TaskWithTickOptionCreateView, TaskWithTickOptionListView, \
    TaskWithTickOptionRetrieveView, TaskWithTickOptionUpdateView, \
    TaskWithTickStudentResultCreateView, TaskWithTickStudentResultRetrieveView, \
    TaskWithTickStudentResultUpdateView, TaskWithTickStudentResultListView, \
    TaskWithTickCheckCreateView, TaskWithTickCheckListView, \
    TaskWithTickCheckRetrieveView, TaskWithTickCheckUpdateView, StudentListView


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

    path('tasks/with_tick/checks/add/', TaskWithTickCheckCreateView.as_view()),
    path('tasks/with_tick/checks/all/', TaskWithTickCheckListView.as_view()),
    path('tasks/with_tick/checks/<int:pk>/', TaskWithTickCheckRetrieveView.as_view()),
    path('tasks/with_tick/checks/update/<int:pk>/', TaskWithTickCheckUpdateView.as_view()),

]
