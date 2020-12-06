from django.contrib.auth.models import Group
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
from courses_app.models import Badge


def populate_models(sender, **kwargs):
    list_of_groups = ["teacher", "student"]
    for group in list_of_groups:
        Group.objects.get_or_create(name=group)
    badge_all_tasks = {"title":"Выполнил все задания", "description":"Выдается тому, кто выполнил все задания"}
    Badge.objects.get_or_create(title = badge_all_tasks["title"], description = badge_all_tasks["description"])
    badge_keyword_tasks = {"title":"Выполнил все задания с ключевым словом", "description":"Выдается тому, кто выполнил все заданияс ключевым словом"}
    Badge.objects.get_or_create(title = badge_keyword_tasks["title"], description = badge_keyword_tasks["description"])

#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
