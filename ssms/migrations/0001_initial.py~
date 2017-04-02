# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import ssms.models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Both',
            fields=[
                ('b_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Veg+Non Veg Grub Id')),
                ('veg_venue', models.CharField(max_length=16, verbose_name='Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess')])),
                ('non_veg_venue', models.CharField(max_length=16, verbose_name='Non Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess')])),
                ('veg_price', models.IntegerField(default=0, verbose_name='Veg Price')),
                ('non_veg_price', models.IntegerField(default=0, verbose_name='Non Veg price')),
                ('veg_images', models.ImageField(upload_to=ssms.models.content_album_name2, verbose_name='Veg Meal Image')),
                ('non_veg_images', models.ImageField(upload_to=ssms.models.content_album_name2, verbose_name='Non Veg Image')),
            ],
        ),
        migrations.CreateModel(
            name='DateMailStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('mails', models.IntegerField(default=0, verbose_name='Mails Sent')),
            ],
        ),
        migrations.CreateModel(
            name='Grub',
            fields=[
                ('gm_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Grub UUID')),
                ('name', models.CharField(max_length=32, verbose_name='Grub Name')),
                ('meal', models.CharField(default='Veg', max_length=16, verbose_name='Meal Type', choices=[('Veg', 'Veg'), ('Non Veg', 'Non Veg'), ('Both', 'Both')])),
                ('reg_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Registration Date')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('deadline', models.DateField(default=datetime.datetime.now)),
                ('deadline2', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(default='Active', max_length=128, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])),
                ('excel', models.FileField(upload_to=ssms.models.content_album_name)),
                ('mails', models.CharField(default='Not Sent', max_length=128, choices=[('Sent', 'Sent'), ('Not Sent', 'Not Sent'), ('Sent2', 'Sent2')])),
            ],
        ),
        migrations.CreateModel(
            name='Grub_Coord',
            fields=[
                ('cg_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Coordinator UUID')),
                ('cg_name', models.CharField(max_length=32, verbose_name='Coordinator Name')),
                ('cg_bitsid', models.CharField(unique=True, max_length=32, verbose_name='Coordinator Bits ID')),
                ('assoc_name', models.CharField(max_length=64, verbose_name='Association')),
                ('status', models.CharField(default='Active', max_length=32, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])),
                ('date', models.DateTimeField(auto_now=True)),
                ('reg_by', models.CharField(max_length=32)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grub_Student',
            fields=[
                ('unique_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Unique Student Id')),
                ('name', models.CharField(max_length=32)),
                ('student_id', models.CharField(max_length=32, verbose_name='Bits Id')),
                ('user_id', models.CharField(max_length=32, verbose_name='Bits Email Id', db_index=True)),
                ('mail', models.CharField(default='Not Sent', max_length=128, choices=[('Sent', 'Sent'), ('Not Sent', 'Not Sent')])),
                ('meal', models.CharField(default='Veg', max_length=16, verbose_name='Mealtype Selected', choices=[('Veg', 'Veg'), ('Non Veg', 'Non Veg')])),
                ('status', models.CharField(max_length=128, choices=[('Signed Up', 'Signed Up'), ('Opted Out', 'Opted Out')])),
                ('room', models.CharField(default='303', max_length=32, verbose_name='Room No.')),
                ('bhawan', models.CharField(default='VK', max_length=32, verbose_name='Bhawan')),
                ('gm_id', models.ForeignKey(default='1', verbose_name='Grub Id', to='ssms.Grub')),
            ],
        ),
        migrations.CreateModel(
            name='NonVeg',
            fields=[
                ('n_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Non Veg Grub ID')),
                ('n_venue', models.CharField(max_length=16, verbose_name='Non Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess')])),
                ('n_price', models.IntegerField(default=0, verbose_name='Non Veg Price')),
                ('n_images', models.ImageField(upload_to=ssms.models.content_album_name2, verbose_name='Non Veg Meal image')),
                ('gm_id', models.ForeignKey(verbose_name='Grub Id', to='ssms.Grub')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('unique_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Unique Stud Id')),
                ('name', models.CharField(max_length=32)),
                ('bits_id', models.CharField(unique=True, max_length=32, verbose_name='BITS ID')),
                ('bhawan', models.CharField(max_length=32)),
                ('room_no', models.CharField(max_length=4, verbose_name='Room No.')),
                ('user_id', models.CharField(max_length=32, verbose_name='Bits Email Id', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Veg',
            fields=[
                ('v_id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, verbose_name='Veg Grub ID')),
                ('v_venue', models.CharField(max_length=16, verbose_name='Veg Location', choices=[(b'VKB Mess', b'VKB Mess'), (b'KG Mess', b'KG Mess'), (b'RP Mess', b'RP Mess')])),
                ('v_price', models.IntegerField(default=0, verbose_name='Veg Price')),
                ('v_images', models.ImageField(upload_to=ssms.models.content_album_name2, verbose_name='Veg Meal image')),
                ('gm_id', models.ForeignKey(verbose_name='Grub Id', to='ssms.Grub')),
            ],
        ),
        migrations.AddField(
            model_name='grub',
            name='cg_id',
            field=models.ForeignKey(verbose_name='Coordinator Id', to='ssms.Grub_Coord'),
        ),
        migrations.AddField(
            model_name='both',
            name='gm_id',
            field=models.ForeignKey(verbose_name='Grub Id', to='ssms.Grub'),
        ),
        migrations.AlterUniqueTogether(
            name='grub_student',
            unique_together=set([('student_id', 'gm_id', 'status')]),
        ),
    ]
