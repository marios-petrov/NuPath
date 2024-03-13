from django.apps import apps
from django.contrib import admin

app = apps.get_app_config('Users')

# Auto register all models using for loop
for model_name, model in app.models.items():
    admin.site.register(model)