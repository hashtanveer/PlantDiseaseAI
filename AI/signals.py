from account.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile, Plant
from .apps import prediction_models_manager

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Plant)
def load_new_prediction_models(sender, instance, created, **kwargs):
    prediction_models_manager.update_prediction_models()

@receiver(post_delete, sender=Plant)
def unload_prediction_models(sender, instance, **kwargs):
    prediction_models_manager.update_prediction_models()