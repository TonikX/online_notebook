from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentGroupSerializer
from rest_framework import permissions
from rest_framework import generics
from .models import StudentGroup


class StudentGroupView(generics.ListCreateAPIView):
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return StudentGroup.objects.all()

