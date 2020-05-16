from django.db import models
from django.contrib.auth.models import AbstractUser


class StudentStream(models.Model):
    title = models.CharField(max_length=60)


class StudentGroup(models.Model):
    title = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    year_of_receipt = models.IntegerField()
    streams = models.ManyToManyField(
        StudentStream, through='GroupInStream', related_name='groups'
    )

    class Meta:
        unique_together = ['number', 'year_of_receipt']

    def __str__(self):
        return self.title


class GroupInStream(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stream.title} {self.group.number}'


class User(AbstractUser):
    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True)
    group_number = models.ForeignKey(
        StudentGroup, on_delete=models.PROTECT, null=True, blank=True
    )

    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'email', 'role', 'tel', 'group_number'
    ]

    def __str__(self):
        return self.username
