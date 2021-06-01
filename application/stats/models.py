from datetime import datetime
from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from tests_builder.models import Test, Question, Answer, RandomTest, FixedTest


class ValidationError(Exception):
    pass


class StudentTest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    number_of_try = models.PositiveSmallIntegerField()
    started = models.DateTimeField(blank=True, default=timezone.now)
    finished = models.DateTimeField(blank=True, null=True)
    correct_answers_count = models.PositiveSmallIntegerField(blank=True, null=True)
    correct_answers_percent = models.PositiveSmallIntegerField(blank=True, null=True)
    is_success = models.BooleanField(blank=True, null=True)

    class Meta:
        abstract = True

    @transaction.atomic
    def _finish_test(self, questions):
        if self.finished:
            raise ValidationError('Test has already been finished')

        all_count = questions.count()
        if all_count == 0:
            raise ValidationError('There are no questions in this test')

        correct_count = questions.filter(is_correct=True).count()

        correct_percent = round(correct_count * 100 / all_count)
        is_success = True if correct_percent >= self.test.min_percent_for_success else False

        self.finished = datetime.now()
        self.correct_answers_count = correct_count
        self.correct_answers_percent = correct_percent
        self.is_success = is_success
        self.save()

        return self


class StudentRandomTest(StudentTest):
    test = models.ForeignKey(RandomTest, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('test', 'student', 'number_of_try')

    @transaction.atomic
    def finish_test(self):
        return self._finish_test(StudentRandomTestQuestion.objects.filter(student_test=self))


class StudentFixedTest(StudentTest):
    test = models.ForeignKey(FixedTest, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'student', 'number_of_try')

    @transaction.atomic
    def finish_test(self):
        return self._finish_test(StudentFixedTestQuestion.objects.filter(student_test=self))


class StudentTestQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answers = models.ManyToManyField(Answer, blank=True)
    is_correct = models.BooleanField(blank=True, null=True)
    submitting_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class StudentRandomTestQuestion(StudentTestQuestion):
    student_test = models.ForeignKey(StudentRandomTest, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('student_test', 'question')


class StudentFixedTestQuestion(StudentTestQuestion):
    student_test = models.ForeignKey(StudentFixedTest, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student_test', 'question')
