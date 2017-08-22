# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssms', '0004_auto_20170416_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fb',
            name='s_id',
            field=models.CharField(default='1', max_length=16),
        ),
    ]
