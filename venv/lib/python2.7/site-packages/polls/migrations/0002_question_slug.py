# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.CharField(default=b'question', unique=True, max_length=10),
            preserve_default=True,
        ),
    ]
