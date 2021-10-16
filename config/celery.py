import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('settings')
app.config_from_object('django.conf:base', namespace='CELERY')
app.autodiscover_tasks()

