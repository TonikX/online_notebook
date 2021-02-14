from django.conf import settings
from django.db import models


from courses.models import Course


class Group(models.Model):
    number = models.CharField(unique=True, max_length=20)
    courses = models.ManyToManyField(Course, blank=True, related_name='groups')

    def __str__(self):
        return self.number


class Stream(models.Model):
    number = models.CharField(unique=True, max_length=20)
    groups = models.ManyToManyField(Group, blank=True, related_name='streams')

    def __str__(self):
        return self.number


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.CharField(max_length=1024)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    visits_cnt = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}, {self.group}'


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.user.username
