from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from profiles import views


router = DefaultRouter()
router.register(r'groups', views.GroupSet, basename='groups')
router.register(r'streams', views.StreamSet, basename='streams')
router.register(r'students', views.StudentSet, basename='students')
router.register(r'instructors', views.InstructorSet, basename='instructors')


urlpatterns = [
    url(r'', include(router.urls)),
]
