from django.urls import path, re_path
from django.conf.urls import url
from .views import StudentGroupView

app_name = "courses_app"

urlpatterns = [

    path('student-groups/', StudentGroupView.as_view()),

    ]
