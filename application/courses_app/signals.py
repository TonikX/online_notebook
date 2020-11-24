from django.contrib.auth.models import Group


def populate_models(sender, **kwargs):
    list_of_groups = ["teacher", "student"]
    for group in list_of_groups:
        Group.objects.get_or_create(name=group)
