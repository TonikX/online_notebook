from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from stats import views


router = DefaultRouter()
router.register(r'student_fixed_tests', views.StudentFixedTestSet, basename='student-fixed-tests')
router.register(r'student_random_tests', views.StudentRandomTestSet, basename='student-random-tests')
router.register(
    r'student_fixed_test_questions', views.StudentFixedTestQuestionSet, basename='student-fixed-test-questions'
)
router.register(
    r'student_random_test_questions', views.StudentRandomTestQuestionSet, basename='student-random-test-questions'
)

urlpatterns = [
    url(r'', include(router.urls)),
]
