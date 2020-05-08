from django.contrib import admin
from .models import User, StudentGroup
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(StudentGroup)
UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role', 'group_number')}),
admin.site.register(User, UserAdmin)
# admin.site.register(Membership)
