# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('meal_type', models.CharField(max_length=30, choices=[('grub', 'GRUB'), ('lunch', 'LUNCH'), ('dinner', 'DINNER'), ('breakfast', 'BREAKFAST')])),
                ('day', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='meal',
            field=models.ForeignKey(to='ssms.Meal'),
        ),
    ]
