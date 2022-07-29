from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import ParseJob
from apps.user.tasks.ya_papse import parse


@receiver(post_save, sender=ParseJob, dispatch_uid="run_job")
def run_job(sender, instance: ParseJob, created: bool, **kwargs):
    if created:
        parse.delay(instance.id, instance.url)
