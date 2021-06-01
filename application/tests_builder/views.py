from django_filters import rest_framework as django_filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import permissions
from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tests_builder import models
from tests_builder import serializers


class FixedTestSet(viewsets.ModelViewSet):
    queryset = models.FixedTest.objects.all()
    serializer_class = serializers.FixedTestSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # ordering_fields = ['questions__position']
    # filterset_fields = ('name', 'section')
    # search_fields = ('name', 'section__name', 'created_by__username')

class StudentFixedTestSet(viewsets.ReadOnlyModelViewSet):
    """Получение теста с вопросами(с текстом вопроса) и ответами (без is_correct)"""
    # TODO: возможно сделать другой пермишн
    permission_classes = [permissions.AllowAny]
    queryset = models.FixedTest.objects.all()
    serializer_class = serializers.StudentTestSerializer1

class FixedTestQuestionSet(viewsets.ModelViewSet):
    queryset = models.FixedTestQuestion.objects.all()
    serializer_class = serializers.FixedTestQuestionSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filterset_fields = ('test',)
    # search_fields = ('test__name', 'question__text_question')
    def destroy(self, request, *args, **kwargs):
        question = self.get_object()
        test = question.test
        posStart = question.position + 1
        question.delete()
        questionsByTest = models.FixedTestQuestion.objects.filter(test=test)
        for question in questionsByTest:
            if question.position >= posStart:
                question.position -= 1
                question.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class RandomTestSet(viewsets.ModelViewSet):
    queryset = models.RandomTest.objects.all()
    serializer_class = serializers.RandomTestSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filterset_fields = ('name')
    # search_fields = ('name', 'section__name', 'created_by__username')


class QuestionSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('section', 'section__course')
    # search_fields = ('tags_name', 'text_question')


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class AnswerCreate(generics.CreateAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerCreateSerializer


class TagSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filterset_fields = ('name',)
    # search_fields = ('name',)
