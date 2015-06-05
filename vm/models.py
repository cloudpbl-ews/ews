from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VirtualMachine(models.Model):
    uuid = models.CharField(max_length=100)
    user = models.ForeignKey(User)

