from .models import StudentGroup
from rest_framework import serializers


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ("id", "title")
