from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VirtualMachine(models.Model):
    name = models.CharField(max_length=100, default='your virtual machine')
    uuid = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name
