# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssms', '0003_fb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fb',
            name='unique_id',
        ),
        migrations.AddField(
            model_name='fb',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
