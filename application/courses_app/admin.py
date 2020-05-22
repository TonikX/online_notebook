from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, StudentGroup, StudentStream, GroupInStream

admin.site.register(StudentGroup)
admin.site.register(StudentStream)
admin.site.register(GroupInStream)

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role', 'group')}),
admin.site.register(User, UserAdmin)
# admin.site.register(Membership)
