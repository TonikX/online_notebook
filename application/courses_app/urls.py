from django.urls import path, re_path
from django.conf.urls import url
from .views import StudentStreamListCreateView, StudentStreamRetrieveUpdateView,\
    StudentGroupListCreateView, StudentGroupRetrieveUpdateView, \
    StudentGroupMembersListCreateView, GroupInStreamListCreateView, \
    CourseCreateView, CourseRetrieveUpdateView, LessonCreateView, \
    LessonRetrieveUpdateView, StudentLessonResultCreateView, \
    StudentLessonResultRetrieveUpdateView, CourseListView, \
    LessonListView, StudentLessonResultListView, StudentListView

app_name = "courses_app"

urlpatterns = [
    path('students/', StudentListView.as_view()),

    path('streams/', StudentStreamListCreateView.as_view()),
    path('streams/<int:pk>/', StudentStreamRetrieveUpdateView.as_view()),
    path('streams/<int:pk>/groups/', GroupInStreamListCreateView.as_view()),

    path('groups/', StudentGroupListCreateView.as_view()),
    path('groups/<int:pk>/', StudentGroupRetrieveUpdateView.as_view()),
    path('groups/<int:pk>/members/', StudentGroupMembersListCreateView.as_view()),

    path('courses/add', CourseCreateView.as_view()),
    path('courses/all', CourseListView.as_view()),
    path('courses/<int:pk>', CourseRetrieveUpdateView.as_view()),

    path('lessons/add', LessonCreateView.as_view()),
    path('lessons/all', LessonListView.as_view()),
    path('lessons/<int:pk>', LessonRetrieveUpdateView.as_view()),

    path('lessons/results/add', StudentLessonResultCreateView.as_view()),
    path('lessons/results/all', StudentLessonResultListView.as_view()),
    path('lessons/results/<int:pk>', StudentLessonResultRetrieveUpdateView.as_view()),
]
