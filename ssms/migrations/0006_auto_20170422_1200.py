# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ssms', '0005_auto_20170416_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_name', models.CharField(default='', max_length=32, verbose_name='Batch Name', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])),
                ('color', models.CharField(max_length=10, verbose_name='Batch Color', choices=[('Red', 'Red'), ('Yellow', 'Yellow'), ('Blue', 'Blue'), ('Green', 'Green')])),
                ('timing', models.CharField(max_length=16, verbose_name='Batch Time')),
                ('gm_id', models.ForeignKey(verbose_name='Grub Id', to='ssms.Grub')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('unique_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Unique Stud Id')),
                ('stugm_id', models.CharField(max_length=20, null=True, verbose_name='Student BITS Id', blank=True)),
                ('meal_type', models.CharField(max_length=10, verbose_name='Meal type')),
                ('batch', models.CharField(default='', max_length=18, null=True, verbose_name='Batch', blank=True)),
                ('grub_time_entry', models.CharField(max_length=7, null=True, blank=True)),
                ('mess', models.CharField(max_length=30, null=True, blank=True)),
                ('quality', models.CharField(max_length=2, null=True, blank=True)),
                ('hygiene', models.CharField(max_length=2, null=True, blank=True)),
                ('taste', models.CharField(max_length=2, null=True, blank=True)),
                ('rating', models.CharField(max_length=2, null=True, blank=True)),
                ('most_liked_dish', models.CharField(max_length=50, null=True, blank=True)),
                ('others', models.CharField(max_length=500, null=True, blank=True)),
                ('gm_id', models.ForeignKey(verbose_name='Grub Id', to='ssms.Grub')),
                ('user', models.ForeignKey(verbose_name='User Id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='fb',
            name='gm_id',
        ),
        migrations.RemoveField(
            model_name='items',
            name='meal',
        ),
        migrations.AddField(
            model_name='grub_student',
            name='feedback_given',
            field=models.IntegerField(default=0, verbose_name='Feedback given'),
        ),
        migrations.AlterField(
            model_name='grub_coord',
            name='cg_bitsid',
            field=models.CharField(max_length=32, verbose_name='Coordinator Bits ID'),
        ),
        migrations.DeleteModel(
            name='FB',
        ),
        migrations.DeleteModel(
            name='Items',
        ),
        migrations.DeleteModel(
            name='Meal',
        ),
        migrations.AddField(
            model_name='grub_student',
            name='batch',
            field=models.ForeignKey(default='', verbose_name='Batch', to='ssms.Batch'),
        ),
    ]
