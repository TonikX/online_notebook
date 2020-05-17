from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import StudentStream, StudentGroup

User = get_user_model()


class StudentStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStream
        fields = ("id", "title")


class StudentGroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudentGroup
        fields = ("id", "title", "number", "year_of_receipt", "members")


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "tel")
