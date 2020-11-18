from django.contrib import admin
from django.apps import apps
from simple_history.admin import SimpleHistoryAdmin

from social import models


@admin.register(models.Log)
class LogAdmin(SimpleHistoryAdmin):
    list_display = ["action", "created_at", "status", "res", "params"]
    readonly_fields = ["created_at"]
    history_list_display = ["result"]


# auto register models
skip_models = []  # ('authtoken.Token.objects', 'account.EmailAddress.objects', 'socialaccount.SocialApp.objects',)
skip_app = ''  # 'social_django'
apps_models = apps.get_models()
for model in apps_models:
    model_objects = str(model.objects)
    if (skip_models and model_objects in skip_models) \
            or (skip_app and model_objects.startswith(skip_app)):
        continue
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
