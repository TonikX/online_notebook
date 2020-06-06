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
    StudentResultListCreateView, StudentResultRetrieveUpdateDestroyView

app_name = "courses_app"

urlpatterns = [
    path('streams/', StudentStreamListCreateView.as_view()),
    path('streams/<int:pk>/', StudentStreamRetrieveUpdateView.as_view()),
    path('streams/<int:pk>/groups/', GroupInStreamListCreateView.as_view()),

    path('groups/', StudentGroupListCreateView.as_view()),
    path('groups/<int:pk>/', StudentGroupRetrieveUpdateView.as_view()),
    path('groups/<int:pk>/members/', StudentGroupMembersListCreateView.as_view()),

    path('courses/add/', CourseCreateView.as_view()),
    path('courses/all/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseRetrieveUpdateView.as_view()),

    path('lessons/add/', LessonCreateView.as_view()),
    path('lessons/all/', LessonListView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveUpdateView.as_view()),

    path('lessons/results/add/', StudentLessonResultCreateView.as_view()),
    path('lessons/results/all/', StudentLessonResultListView.as_view()),
    path('lessons/results/<int:pk>/', StudentLessonResultRetrieveUpdateView.as_view()),

    path('classmates/tasks/', ClassmatesCheckedTaskListCreateView.as_view()),
    path('classmates/tasks/<int:pk>/', ClassmatesCheckedTaskRetrieveUpdateDestroyView.as_view()),

    path('classmates/options/', TaskOptionListCreateView.as_view()),
    path('classmates/options/<int:pk>/', TaskOptionRetrieveUpdateDestroyView.as_view()),

    path('classmates/results/', StudentResultListCreateView.as_view()),
    path('classmates/results/<int:pk>/', StudentResultRetrieveUpdateDestroyView.as_view()),

    path('classmates/checks/', StudentResultListCreateView.as_view()),
    path('classmates/checks/<int:pk>/', StudentResultRetrieveUpdateDestroyView.as_view()),
]
