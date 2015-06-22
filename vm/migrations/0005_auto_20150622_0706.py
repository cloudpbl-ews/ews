# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0004_virtualmachinerecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualmachinerecord',
            name='uuid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='virtualmachinerecord',
            name='vncport',
            field=models.IntegerField(),
        ),
    ]
