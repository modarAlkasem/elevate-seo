# Python Imports
import os

# Third Party Imports
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class CustomCelery(Celery):
    def gen_task_name(self, name: str, module: str):
        if module.endswith("tasks"):
            module = module[:-6]
        return super().gen_task_name(name, module)


app = CustomCelery("elevate_seo")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
