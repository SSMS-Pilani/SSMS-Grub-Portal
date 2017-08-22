# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ssms', '0002_auto_20170407_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='FB',
            fields=[
                ('unique_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Unique Feedback Id')),
                ('meal_type', models.CharField(max_length=20)),
                ('batch', models.IntegerField(default=0)),
                ('grub_time', models.CharField(max_length=7, choices=[('1', '08:30 pm'), ('2', '08:45 pm'), ('3', '09:00 pm'), ('4', '09:15 pm'), ('5', '09:30 pm'), ('6', '09:45 pm'), ('7', '10:00 pm'), ('8', '10:15 pm'), ('9', '10:30 pm'), ('10', '10:45 pm'), ('11', '11:00 pm')])),
                ('mess', models.CharField(max_length=30, null=True, choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess')])),
                ('quality', models.IntegerField(default=0)),
                ('hygiene', models.IntegerField(default=0)),
                ('taste', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('dish_most_liked', models.CharField(max_length=50, blank=True)),
                ('others', models.CharField(max_length=500, blank=True)),
                ('gm_id', models.ForeignKey(default='1', verbose_name='Grub Id', to='ssms.Grub')),
                ('s_id', models.ForeignKey(default='1', verbose_name='Grub Student Id', to='ssms.Grub_Student')),
            ],
        ),
    ]
