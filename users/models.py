from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class Advisors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="Advisors/")
    objects = models.Manager()
    


class Bookings(models.Model):
    id = models.AutoField(primary_key=True)
    booking_time = models.DateTimeField(null=True)
    advisor = models.ForeignKey(Advisors,on_delete = models.DO_NOTHING ,null=True)
    user = models.ForeignKey(User,on_delete = models.DO_NOTHING ,null=True)
    objects = models.Manager()
