from django.contrib import admin

from stats import models

admin.site.register(models.StudentRandomTest)
admin.site.register(models.StudentFixedTest)
admin.site.register(models.StudentRandomTestQuestion)
admin.site.register(models.StudentFixedTestQuestion)
