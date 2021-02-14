from django.conf import settings
from django.db import models
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses')

    def __str__(self):
        return self.name


class CourseSection(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('course', 'name')

    def __str__(self):
        return self.name
