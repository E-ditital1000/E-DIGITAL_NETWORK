from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import logging
from vote.models import Notification  # Update the import to match your app's name

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Deletes notifications older than 72 hours'

    def handle(self, *args, **kwargs):
        try:
            older_than = timezone.now() - timedelta(hours=72)
            notifications_to_delete = Notification.objects.filter(created_at__lt=older_than)
            count = notifications_to_delete.count()
            notifications_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} notifications older than 72 hours'))
            logger.info(f'Successfully deleted {count} notifications older than 72 hours')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error deleting notifications: {e}'))
            logger.error(f'Error deleting notifications: {e}', exc_info=True)
