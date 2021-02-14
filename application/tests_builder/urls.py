from django.urls import path
from tests_builder import views

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'fixed_tests', views.FixedTestSet, basename='fixed-tests')
router.register(r'fixed_test_questions', views.FixedTestQuestionSet, basename='fixed-test-questions')
router.register(r'random_tests', views.RandomTestSet, basename='random-tests')
router.register(r'questions', views.QuestionSet, basename='questions')
router.register(r'tags', views.TagSet, basename='tags')


urlpatterns = [
    path('answers/<int:pk>/', views.AnswerDetail.as_view()),
    url(r'', include(router.urls)),
]
