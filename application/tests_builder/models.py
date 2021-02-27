import random
from typing import List, Optional

from django.conf import settings
from django.db import models
from django.utils import timezone


from courses_app.models import Section, Course


class ValidationError(Exception):
    pass


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    text_question = models.CharField(max_length=2555)
    tags = models.ManyToManyField(Tag, blank = True, null = True, related_name='questions')
    section = models.ForeignKey(Section, blank = True, null = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text_question

    def get_correct_answers_ids(self):
        return {answer.id for answer in self.answers.all() if answer.is_correct}

    @classmethod
    def get_questions_by_tags(cls, tags: List, count: Optional[int] = None):
        if count is not None and count < 0:
            raise ValidationError('Count is supposed to be empty or more than zero')

        question_ids = list({question.id for question in cls.objects.filter(tags__in=tags)})

        if count is not None and count > len(question_ids):
            raise ValidationError('There are not enough questions in this test')

        random.shuffle(question_ids)

        question_ids = question_ids if count is None else question_ids[:count]

        return cls.objects.filter(id__in=question_ids).order_by('?')


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text_answer


class Test(models.Model):
    name = models.CharField(unique=True, max_length=50)
    # section = models.ForeignKey(CourseSection, on_delete=models.PROTECT)
    # section_in_test = models.ForeignKey(Section, on_delete=models.CASCADE, related_name = 'all_tests_for_section')
    max_number_of_tries = models.PositiveSmallIntegerField(default=1)
    time_limit_for_try = models.PositiveSmallIntegerField(null=True, blank=True)
    min_percent_for_success = models.PositiveSmallIntegerField(default=60)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class FixedTestQuestion(models.Model):
    test = models.ForeignKey('FixedTest', on_delete=models.CASCADE, related_name='test_to_question')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_to_test')
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('test', 'question'), ('test', 'position'))

    def __str__(self):
        return f'{self.question.text_question}'


class FixedTest(Test):
    questions = models.ManyToManyField(Question, through=FixedTestQuestion, related_name='fixed_tests')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name = 'fixed_tests_for_section')

class RandomTest(Test):
    questions_cnt = models.PositiveSmallIntegerField()
    tags = models.ManyToManyField(Tag, related_name='random_tests')

    def get_questions_for_test(self):
        return Question.get_questions_by_tags([tag.id for tag in self.tags.all()], self.questions_cnt)
