import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CSVproject_main.settings')

app = Celery('CSVproject_main')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
