from django.contrib import admin

from profiles import models

admin.site.register(models.Group)
admin.site.register(models.Stream)
admin.site.register(models.Student)
admin.site.register(models.Instructor)
