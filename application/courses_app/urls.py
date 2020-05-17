from django.urls import path, re_path
from django.conf.urls import url
from .views import StudentStreamListCreateView, StudentStreamRetrieveUpdateView,\
    StudentGroupListCreateView, StudentGroupRetrieveUpdateView, \
    StudentGroupMembersListCreateView, GroupInStreamListCreateView

app_name = "courses_app"

urlpatterns = [
    path('streams/', StudentStreamListCreateView.as_view()),
    path('streams/<int:pk>/', StudentStreamRetrieveUpdateView.as_view()),
    path('streams/<int:pk>/groups/', GroupInStreamListCreateView.as_view()),

    path('groups/', StudentGroupListCreateView.as_view()),
    path('groups/<int:pk>/', StudentGroupRetrieveUpdateView.as_view()),
    path('groups/<int:pk>/members/', StudentGroupMembersListCreateView.as_view()),
]
