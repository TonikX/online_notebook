from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from courses import views


router = DefaultRouter()
router.register(r'courses', views.CourseSet, basename='courses')
router.register(r'course_sections', views.CourseSectionSet, basename='course_sections')

urlpatterns = [
    url(r'', include(router.urls)),
]
