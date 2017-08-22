# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssms', '0006_auto_20170422_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='grub_time_entry',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='mess',
        ),
        migrations.AlterField(
            model_name='both',
            name='non_veg_venue',
            field=models.CharField(max_length=16, verbose_name='Non Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess'), (b'RB Mess', b'RB Mess'), (b'SV Mess', b'SV Mess')]),
        ),
        migrations.AlterField(
            model_name='both',
            name='veg_venue',
            field=models.CharField(max_length=16, verbose_name='Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess'), (b'RB Mess', b'RB Mess'), (b'SV Mess', b'SV Mess')]),
        ),
        migrations.AlterField(
            model_name='grub_student',
            name='batch',
            field=models.ForeignKey(default='', blank=True, to='ssms.Batch', null=True, verbose_name='Batch'),
        ),
        migrations.AlterField(
            model_name='nonveg',
            name='n_venue',
            field=models.CharField(max_length=16, verbose_name='Non Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess'), (b'RB Mess', b'RB Mess'), (b'SV Mess', b'SV Mess')]),
        ),
        migrations.AlterField(
            model_name='veg',
            name='v_venue',
            field=models.CharField(max_length=16, verbose_name='Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess'), (b'RB Mess', b'RB Mess'), (b'SV Mess', b'SV Mess')]),
        ),
    ]
