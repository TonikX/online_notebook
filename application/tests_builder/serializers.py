from django.db import transaction
from rest_framework import serializers

from tests_builder import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    is_correct = serializers.BooleanField()

    class Meta:
        model = models.Answer
        fields = ('id', 'text_answer', 'is_correct')


class AnswerCreateSerializer(serializers.ModelSerializer):
    is_correct = serializers.BooleanField()

    class Meta:
        model = models.Answer
        fields = ('id', 'text_answer', 'is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    # tags = serializers.SlugRelatedField(required=False, many=True, slug_field='name', queryset=models.Tag.objects.all())

    class Meta:
        model = models.Question
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')


        question = models.Question.objects.create(**validated_data)

        for answer_data in answers_data:
            models.Answer.objects.create(question=question, **answer_data)

        # try:
        #     tags_data = validated_data.pop('tags')
        #     for tag_data in tags_data:
        #         question.tags.add(tag_data)
        # except:
        #     pass

        return question

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.text_question = validated_data.get('text_question', instance.text_question)
        # tags_data = validated_data.pop('tags')
        #
        # for tag_data in tags_data:
        #     instance.tags.add(tag_data)

        instance.save()

        return instance


class FixedTestQuestionSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer()

    class Meta:
        model = models.FixedTestQuestion
        fields = '__all__'


class CreateFixedTestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FixedTestQuestion
        fields = ('id', 'position', 'question')


class FixedTestSerializer(serializers.ModelSerializer):
    questions = CreateFixedTestQuestionSerializer(source='test_to_question', many=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FixedTest
        fields = '__all__'
        read_only_fields = ('created',)

    def to_representation(self, instance):
            response = super().to_representation(instance)
            response["questions"] = sorted(response["questions"], key=lambda x: x["position"])
            return response

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('test_to_question')

        fixed_test = models.FixedTest.objects.create(**validated_data)

        positions = {question_data['position'] for question_data in questions_data}
        if len(positions) != len(questions_data):
            raise serializers.ValidationError('Questions positions are supposed to be unique in one test')

        models.FixedTestQuestion.objects.bulk_create([
            models.FixedTestQuestion(
                test=fixed_test, question=data['question'], position=data['position']
            ) for data in questions_data
        ])

        return fixed_test

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.section = validated_data.get('section', instance.section)
        instance.max_number_of_tries = validated_data.get('max_number_of_tries', instance.max_number_of_tries)
        instance.time_limit_for_try = validated_data.get('time_limit_for_try', instance.time_limit_for_try)
        instance.min_percent_for_success = validated_data.get('min_percent_for_success', instance.min_percent_for_success)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()

        return instance


class RandomTestSerializer(serializers.ModelSerializer):
    # tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=models.Tag.objects.all())
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.RandomTest
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')

        random_test = models.RandomTest.objects.create(**validated_data)

        for tag_data in tags_data:
            random_test.tags.add(tag_data)

        return random_test





class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'text_answer')

class StudentQuestionSerializer(serializers.ModelSerializer):
    answers = StudentAnswerSerializer(many=True)
    class Meta:
        model = models.Question
        fields = ('id', 'text_question', 'answers')

class StudentTestQuestionSerializer(serializers.ModelSerializer):
    question = StudentQuestionSerializer()
    class Meta:
        model = models.FixedTestQuestion
        fields = ('id', 'position', 'question')

class StudentTestSerializer1(serializers.ModelSerializer):
    questions = StudentTestQuestionSerializer(source='test_to_question', many=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FixedTest
        fields = '__all__'

    def to_representation(self, instance):
            response = super().to_representation(instance)
            response["questions"] = sorted(response["questions"], key=lambda x: x["position"])
            return response
