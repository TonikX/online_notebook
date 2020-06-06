from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, StudentGroup, StudentStream, GroupInStream, Course, Lesson, StudentLessonResult, Section, \
    ClassmatesCheckedTask, TaskOption, StudentResult, Check

admin.site.register(StudentGroup)
admin.site.register(StudentStream)
admin.site.register(GroupInStream)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(StudentLessonResult)
admin.site.register(Section)
admin.site.register(ClassmatesCheckedTask)
admin.site.register(TaskOption)
admin.site.register(StudentResult)
admin.site.register(Check)

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role', 'group')}),
admin.site.register(User, UserAdmin)
# admin.site.register(Membership)
