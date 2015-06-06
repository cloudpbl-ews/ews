# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmachine',
            name='name',
            field=models.CharField(default=b'your virtual machine', max_length=100),
        ),
    ]
