"""Celery app."""
import os

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ad_catcher.settings")
celery_app = Celery()
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


celery_app.conf.timezone = 'UTC'
celery_app.conf.update(
    worker_max_tasks_per_child=1,
    broker_pool_limit=None
)
