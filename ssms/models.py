from __future__ import unicode_literals

import os
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from ssms import venue

def content_album_name(instance, filename):
    return os.path.join(instance.name, filename)


def content_album_name2(instance, filename):
    return os.path.join(instance.gm_id.name, filename)


batch_allocation_choices = (('Yes', 'Yes'), ('No', 'No'))


class Grub_Coord(models.Model):
    stype = (('Active', 'Active'), ('Inactive', 'Inactive'))
    user = models.OneToOneField(User)
    cg_id = models.UUIDField("Coordinator UUID", primary_key=True,
                             default=uuid.uuid4, editable=False)
    cg_name = models.CharField("Coordinator Name", max_length=64, blank=False)
    cg_bitsid = models.CharField("Coordinator Bits ID", max_length=32, unique=False)
    assoc_name = models.CharField("Association", max_length=64, blank=False)
    status = models.CharField(choices=stype, max_length=32, default='Active')
    date = models.DateTimeField(auto_now=True)
    reg_by = models.CharField(max_length=32)

    def __str__(self):
        return self.cg_name + "-" + self.user.username


class Grub(models.Model):
    mtype = (('Veg', 'Veg'), ('Non Veg', 'Non Veg'), ('Both', 'Both'))
    stype = (('Active', 'Active'), ('Inactive', 'Inactive'))
    emtype = (('Sent', 'Sent'), ('Not Sent', 'Not Sent'), ('Sent2', 'Sent2'))
    spot_signing_choices = (('Yes', 'Yes'), ('No', 'No'))
    gm_id = models.UUIDField("Grub UUID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Grub Name", max_length=32)
    meal = models.CharField("Meal Type", choices=mtype, max_length=16, default='Veg')
    cg_id = models.ForeignKey(Grub_Coord, verbose_name="Coordinator Id")
    reg_date = models.DateTimeField("Registration Date", default=datetime.now, blank=False)
    date = models.DateField(default=datetime.now, blank=False)
    deadline = models.DateField(default=datetime.now, blank=False)
    deadline2 = models.DateField(default=datetime.now, blank=False)
    status = models.CharField(choices=stype, max_length=128, default='Active')
    excel = models.FileField(upload_to=content_album_name, blank=False)
    mails = models.CharField(choices=emtype, max_length=128, default='Not Sent', blank=False)
    spot_signing = models.CharField(
        "Spot Signing Available", choices=spot_signing_choices, max_length=6, default="Yes", blank=False)
    batch_allocated = models.CharField(
        "Batch Allocated", choices=batch_allocation_choices, max_length=6, default='No')
    no_batch = models.IntegerField("No. of batches", default=0)

    def __str__(self):
        return self.name


class Batch(models.Model):
    mtype = (('Veg', 'Veg'), ('Non Veg', 'Non Veg'))
    batch_choices = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"))
    color_choices = (("Pink", "Pink"), ("Yellow", "Yellow"), ("Blue", "Blue"), ("Green", "Green"))
    gm_id = models.ForeignKey(Grub, verbose_name="Grub Id")
    meal = models.CharField("Meal Type", choices=mtype, max_length=16, default='Veg')
    batch_name = models.CharField("Batch Name", default="",
                                  choices=batch_choices, max_length=32, blank=False)  # batch name
    color = models.CharField("Batch Color", max_length=10, choices=color_choices)
    timing = models.CharField("Batch Time", max_length=16, blank=False)

    def __str__(self):
        return self.batch_name + "-" + self.meal + "- " + self.gm_id.name


class Grub_Student(models.Model):
    unique_id = models.UUIDField("Unique Student Id", primary_key=True,
                                 default=uuid.uuid4, editable=False)
    stype = (('Signed Up', 'Signed Up'), ('Opted Out', 'Opted Out'), ('Member', 'Member'))
    mtype = (('Veg', 'Veg'), ('Non Veg', 'Non Veg'))
    emtype = (('Sent', 'Sent'), ('Not Sent', 'Not Sent'), ('Sent2', 'Sent2'))
    name = models.CharField(max_length=64)
    student_id = models.CharField("Bits Id", max_length=32, blank=False)
    user_id = models.CharField("Bits Email Id", db_index=True, max_length=32, blank=False)
    gm_id = models.ForeignKey(Grub, default='1', verbose_name="Grub Id")
    mail = models.CharField(choices=emtype, max_length=128, default='Not Sent', blank=False)
    meal = models.CharField("Mealtype Selected", choices=mtype,
                            max_length=16, default='Veg', blank=False)
    status = models.CharField(choices=stype, max_length=128, blank=False)
    room = models.CharField("Room No.", max_length=32, default='303')
    bhawan = models.CharField("Bhawan", max_length=32, default='VK')
    batch = models.ForeignKey(Batch, verbose_name="Batch", blank=True, null=True)
    feedback_given = models.IntegerField("Feedback given", default=0, null=False)

    class Meta:
        unique_together = ('student_id', 'gm_id', 'status')  # add meal

    def __str__(self):
        return self.student_id


class Grub_Member(models.Model):
    mtype = (('Veg', 'Veg'), ('Non Veg', 'Non Veg'))
    student_id = models.CharField("Bits Id", max_length=32, blank=False)
    meal = models.CharField("Mealtype Selected", choices=mtype,
                            max_length=16, default='Veg', blank=False)
    gm_id = models.ForeignKey(Grub, default='1', verbose_name="Grub Id")

    def __str__(self):
        return self.student_id


class Student(models.Model):
    unique_id = models.UUIDField("Unique Stud Id", primary_key=True,
                                 default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    bits_id = models.CharField("BITS ID", max_length=32, unique=True)
    bhawan = models.CharField(max_length=32)
    room_no = models.CharField("Room No.", max_length=4)
    user_id = models.CharField("Bits Email Id", db_index=True, max_length=32, blank=False)

    def __str__(self):
        return self.user_id


class Veg(models.Model):
    gm_id = models.ForeignKey(Grub, verbose_name="Grub Id")
    v_id = models.UUIDField("Veg Grub ID", primary_key=True, default=uuid.uuid4, editable=False)
    v_venue = models.CharField("Veg Location", choices=venue.place, max_length=16, blank=False)
    v_price = models.IntegerField("Veg Price", default=0, null=False)
    v_images = models.ImageField("Veg Meal image", upload_to=content_album_name2, blank=False)
    batch_allocated = models.CharField(choices=batch_allocation_choices, max_length=6, default='No')

    def __str__(self):
        return self.gm_id.name


class NonVeg(models.Model):
    gm_id = models.ForeignKey(Grub, verbose_name="Grub Id")
    n_id = models.UUIDField("Non Veg Grub ID", primary_key=True, default=uuid.uuid4, editable=False)
    n_venue = models.CharField("Non Veg Location", choices=venue.place, max_length=16, blank=False)
    n_price = models.IntegerField("Non Veg Price", default=0, null=False)
    n_images = models.ImageField("Non Veg Meal image", upload_to=content_album_name2, blank=False)
    batch_allocated = models.CharField(choices=batch_allocation_choices, max_length=6, default='No')

    def __str__(self):
        return self.gm_id.name


class Both(models.Model):
    gm_id = models.ForeignKey(Grub, verbose_name="Grub Id")
    b_id = models.UUIDField("Veg+Non Veg Grub Id", primary_key=True,
                            default=uuid.uuid4, editable=False)
    veg_venue = models.CharField("Veg Location", choices=venue.place, max_length=16, blank=False)
    non_veg_venue = models.CharField(
        "Non Veg Location", choices=venue.place, max_length=16, blank=False)
    veg_price = models.IntegerField("Veg Price", default=0, null=False)
    non_veg_price = models.IntegerField("Non Veg price", default=0, null=False)
    veg_images = models.ImageField("Veg Meal Image", upload_to=content_album_name2, blank=False)
    non_veg_images = models.ImageField("Non Veg Image", upload_to=content_album_name2, blank=False)
    veg_batch_allocated = models.CharField(
        choices=batch_allocation_choices, max_length=6, default='No')
    nonveg_batch_allocated = models.CharField(
        choices=batch_allocation_choices, max_length=6, default='No')

    def __str__(self):
        return self.gm_id.name


class DateMailStatus(models.Model):
    date = models.DateField(default=datetime.now, blank=False)
    mails = models.IntegerField("Mails Sent", default=0)

    def __str__(self):
        return self.date.strftime('%m/%d/%Y')


class Feedback(models.Model):
    unique_id = models.UUIDField("Unique Stud Id", primary_key=True,
                                 default=uuid.uuid4, editable=False)
    gm_id = models.ForeignKey(Grub, verbose_name="Grub Id")
    stugm_id = models.CharField("Student BITS Id", max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="User Id")
    meal_type = models.CharField("Meal type", max_length=10)
    quality = models.CharField(max_length=2, null=True, blank=True)
    hygiene = models.CharField(max_length=2, null=True, blank=True)
    taste = models.CharField(max_length=2, null=True, blank=True)
    rating = models.CharField(max_length=2, null=True, blank=True)
    most_liked_dish = models.CharField(max_length=50, null=True, blank=True)
    others = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.gm_id.name + "-" + self.stugm_id


class Meal(models.Model):
    # meal_choices = (('grub','GRUB-LUNCH'),('lunch', 'LUNCH') , ('dinner','DINNER'), ('breakfast','BREAKFAST'))
    date = models.DateField(null=False, blank=False)
    day = models.CharField(max_length=20, null=False, default="0")
    breakfast = models.CharField(max_length=512, blank=False, default="0")
    lunch = models.CharField(max_length=512, blank=False, default="0")
    dinner = models.CharField(max_length=512, blank=False, default="0")
    lunchgrub = models.CharField(max_length=5, blank=True, default="0")  # 1 if grub
    dinnergrub = models.CharField(max_length=5, blank=True, default="0")  # 1 if grub

    def __unicode__(self):
        return str(self.date)


class Grub_Invalid_Students(models.Model):
    mtype = (('Veg', 'Veg'), ('Non Veg', 'Non Veg'))
    student_id = models.CharField("Bits Id", max_length=32, blank=False)
    gm_id = models.ForeignKey(Grub, default='1', verbose_name="Grub Id")
    meal = models.CharField("Mealtype Selected", choices=mtype,
                            max_length=16, default='Veg', blank=False)

    class Meta:
        unique_together = ('student_id', 'gm_id')  # add meal

    def __str__(self):
        return self.student_id
