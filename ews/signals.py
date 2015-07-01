from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib import messages

@receiver(user_logged_in, sender=User)
def logged_in_callback(sender, **kwargs):
    messages.success(kwargs['request'], 'Loged in successfully.')

@receiver(user_logged_out, sender=User)
def logged_out_callback(sender, **kwargs):
    messages.success(kwargs['request'], 'Loged out successfully.')
