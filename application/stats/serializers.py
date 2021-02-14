from django.db import transaction
from django.db.models import Max
from rest_framework import serializers

from stats import models as models


class StudentTestSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field='id', default=serializers.CurrentUserDefault())

    @transaction.atomic
    def create(self, validated_data):
        test = validated_data['test']
        student = self.fields['student'].get_default()

        number_of_new_try = 1

        previous_number_of_try = self.Meta.model.objects.filter(
            test=test.id, student=student
        ).aggregate(prev_try=Max('number_of_try'))['prev_try']
        if previous_number_of_try:
            if previous_number_of_try >= test.max_number_of_tries:
                raise serializers.ValidationError('All tries for this test were used')
            number_of_new_try = previous_number_of_try + 1

        return self.Meta.model.objects.create(test=test, student=student, number_of_try=number_of_new_try)


class StudentFixedTestSerializer(StudentTestSerializer):
    class Meta:
        model = models.StudentFixedTest
        fields = '__all__'
        read_only_fields = (
            'number_of_try', 'started', 'finished', 'correct_answers_count', 'correct_answers_percent', 'is_success'
        )


class StudentRandomTestSerializer(StudentTestSerializer):
    class Meta:
        model = models.StudentRandomTest
        fields = '__all__'
        read_only_fields = (
            'number_of_try', 'started', 'finished', 'correct_answers_count', 'correct_answers_percent', 'is_success'
        )


class StudentTestQuestionSerializer(serializers.ModelSerializer):
    @transaction.atomic
    def create(self, validated_data):
        student_test = validated_data['student_test']
        question = validated_data['question']
        answers = validated_data.pop('answers')

        is_correct = True if question.get_correct_answers_ids() == set(answer.id for answer in answers) else False

        student_test_question = self.Meta.model.objects.create(
            student_test=student_test, question=question, is_correct=is_correct
        )

        for answer in answers:
            student_test_question.answers.add(answer)

        return student_test_question


class StudentFixedTestQuestionSerializer(StudentTestQuestionSerializer):
    class Meta:
        model = models.StudentFixedTestQuestion
        fields = '__all__'
        read_only_fields = ('is_correct', 'submitting_time')


class StudentRandomTestQuestionSerializer(StudentTestQuestionSerializer):
    class Meta:
        model = models.StudentRandomTestQuestion
        fields = '__all__'
        read_only_fields = ('is_correct', 'submitting_time')


class BaseStatsSerializer(serializers.Serializer):
    correct_cnt = serializers.IntegerField()
    total_cnt = serializers.IntegerField()
    correct_percent = serializers.IntegerField()


class QuestionStatsSerializer(BaseStatsSerializer):
    question_id = serializers.IntegerField()


class TestStatsSerializer(BaseStatsSerializer):
    test_id = serializers.IntegerField()


class SectionStatsSerializer(BaseStatsSerializer):
    section_id = serializers.IntegerField()


class CourseStatsSerializer(BaseStatsSerializer):
    course_id = serializers.IntegerField()


class StudentStatsSerializer(BaseStatsSerializer):
    student_id = serializers.IntegerField()


class GroupStatsSerializer(BaseStatsSerializer):
    group_id = serializers.IntegerField()
