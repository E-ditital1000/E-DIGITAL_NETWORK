from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from vote.models import Profile

# Signal to create a profile for newly created users, including superusers
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name or '',
            last_name=instance.last_name or '',
            district='',
            county='',
            age=18,  # Default age or any other default value
        )

# Signal to handle profile recreation on deletion
@receiver(post_delete, sender=Profile)
def recreate_profile_on_delete(sender, instance, **kwargs):
    if hasattr(instance, 'user'):
        Profile.objects.create(
            user=instance.user,
            first_name=instance.first_name,
            last_name=instance.last_name,
            district=instance.district,
            county=instance.county,
            age=instance.age,
        )

# Ensure the signals are connected
post_save.connect(create_user_profile, sender=User)
post_delete.connect(recreate_profile_on_delete, sender=Profile)
