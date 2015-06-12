# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0002_virtualmachine_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='virtualmachine',
            name='user',
        ),
        migrations.DeleteModel(
            name='VirtualMachine',
        ),
    ]
