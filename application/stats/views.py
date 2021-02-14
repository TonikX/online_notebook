from django_filters import rest_framework as django_filters
from django.db.models import Count, Q, F
from rest_framework import generics, views, exceptions, viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from tests_builder import models as tests_models
from tests_builder import serializers as tests_serializers
from stats import models as stats_models
from stats import serializers


class BaseStatsSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    def _format_response(self, stats_data, serializer_class):
        page = self.paginate_queryset(stats_data)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(stats_data, many=True)
        return Response(serializer.data)

    def _get_stats(self, qs_values, serializer_class):
        return self._format_response(self._count_stats(qs_values), serializer_class)

    @action(detail=False)
    def get_sections_stats(self, request):
        return self._get_stats(
            self.queryset.values(section_id=F(self.SECTION_FIELD)), serializers.SectionStatsSerializer
        )

    @action(detail=False)
    def get_courses_stats(self, request):
        return self._get_stats(self.queryset.values(course_id=F(self.COURSE_FIELD)), serializers.CourseStatsSerializer)

    @action(detail=False)
    def get_groups_stats(self, request):
        return self._get_stats(self.queryset.values(group_id=F(self.GROUP_FIELD)), serializers.GroupStatsSerializer)


class StudentTestQuestionSet(BaseStatsSet):
    QUESTION_FIELD = 'question_id'
    #TEST_FIELD = 'student_test__test'
   # SECTION_FIELD = 'student_test__test__section'
   # COURSE_FIELD = 'student_test__test__section__course'
    #STUDENT_FIELD = 'student_test__student'
    #GROUP_FIELD = 'student_test__student__student__group'

    def _count_stats(self, qs_values):
        return qs_values.annotate(
            correct_cnt=Count('id', filter=Q(is_correct=True)),
            total_cnt=Count('id'),
            correct_percent=Count('id', filter=Q(is_correct=True)) * 100 / Count('id')
        ).order_by('correct_percent')

    @action(detail=False)
    def get_questions_stats(self, request):
        return self._get_stats(self.queryset.values(self.QUESTION_FIELD), serializers.QuestionStatsSerializer)

    @action(detail=False)
    def get_tests_stats(self, request):
        return self._get_stats(self.queryset.values(test_id=F(self.TEST_FIELD)), serializers.TestStatsSerializer)

    @action(detail=False)
    def get_students_stats(self, request):
        return self._get_stats(
            self.queryset.values(student_id=F(self.STUDENT_FIELD)), serializers.StudentStatsSerializer
        )


class StudentRandomTestQuestionSet(StudentTestQuestionSet):
    queryset = stats_models.StudentRandomTestQuestion.objects.all()
    serializer_class = serializers.StudentRandomTestQuestionSerializer
    # filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    # filterset_fields = ('student_test',)


class StudentFixedTestQuestionSet(StudentTestQuestionSet):
    queryset = stats_models.StudentFixedTestQuestion.objects.all()
    serializer_class = serializers.StudentFixedTestQuestionSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    # filterset_fields = ('student_test',)


class StudentTestSet(BaseStatsSet):
    TEST_FIELD = 'test_id'
    #STUDENT_FIELD = 'student_id'
    #SECTION_FIELD = 'test__section'
    #COURSE_FIELD = 'test__section__course'
    #GROUP_FIELD = 'student__student__group'

    @action(detail=True, methods=['post'])
    def finish_test(self, request, pk=None):
        try:
            result = self.get_object().finish_test()
        except stats_models.ValidationError as error:
            raise exceptions.ParseError(error)

        return Response(self.serializer_class().to_representation(instance=result))

    def _count_stats(self, qs_values):
        return qs_values.annotate(
            correct_cnt=Count('id', filter=Q(is_success=True)),
            total_cnt=Count('id'),
            correct_percent=Count('id', filter=Q(is_success=True)) * 100 / Count('id')
        ).order_by('correct_percent')

    @action(detail=False)
    def get_tests_stats(self, request):
        return self._get_stats(self.queryset.values(self.TEST_FIELD), serializers.TestStatsSerializer)

    @action(detail=False)
    def get_students_stats(self, request):
        return self._get_stats(self.queryset.values(self.STUDENT_FIELD), serializers.StudentStatsSerializer)


class StudentFixedTestSet(StudentTestSet):
    queryset = stats_models.StudentFixedTest.objects.all()
    serializer_class = serializers.StudentFixedTestSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     filterset_fields = (
#         'student', 'is_success', 'test',
# #        'test__section', 'test__section__course'
#     )
#     search_fields = ('student__username',)


class StudentRandomTestSet(StudentTestSet):
    queryset = stats_models.StudentRandomTest.objects.all()
    serializer_class = serializers.StudentRandomTestSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
 #    filterset_fields = (
 #        'student', 'is_success', 'test',
 # #       'test__section', 'test__section__course', 'test__tags'
 #    )
 #    search_fields = ('student__username', 'test__tags__name')

    @action(detail=True, methods=['get'])
    def get_questions_for_test(self, request, pk=None):
        try:
            questions = self.get_object().test.get_questions_for_test()
        except tests_models.ValidationError as error:
            raise exceptions.ParseError(error)

        return Response([
            tests_serializers.QuestionSerializer().to_representation(instance=question) for question in questions
        ])
