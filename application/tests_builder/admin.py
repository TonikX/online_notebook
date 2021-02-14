from django.contrib import admin


from tests_builder import models

admin.site.register(models.Tag)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.FixedTestQuestion)
admin.site.register(models.FixedTest)
admin.site.register(models.RandomTest)
