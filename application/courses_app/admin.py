from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, StudentGroup, StudentStream, GroupInStream, Course, Lesson, StudentLessonResult

admin.site.register(StudentGroup)
admin.site.register(StudentStream)
admin.site.register(GroupInStream)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(StudentLessonResult)

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role', 'group')}),
admin.site.register(User, UserAdmin)
# admin.site.register(Membership)
