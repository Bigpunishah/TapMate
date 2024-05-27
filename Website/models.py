# from django.db import models
from djongo import models

# Create your models here.
# Dont worry about the conversion python will automatically convert to DB language
class TapTag(models.Model):
    # Keeps track of when a 'Record' was created
    created_at = models.DateTimeField(auto_now_add=True)
    tag_name = models.CharField(max_length=50)
    tag_location = models.CharField(max_length=50)
    email_assigned_to = models.CharField(max_length=50)
    initialized = models.CharField(max_length=10) # Initialized yet or not
    gaurdian = models.CharField(max_length=25)
    enabled = models.CharField(max_length=10)
    # items to adding
    # Data point/ points

    def __str__(self):
        return (f"{self.tag_name} - {self.tag_location}")
    
    # ! After creating, run 
    # todo - `python manage.py makemigrations`
    # then to send to the DB
    # todo - `python manage.py migrate`

    # ! Implement users to admin page by going to admin.py & put
    # todo - `from .models import ActiveUser`

    # If a mistake was made after migrating the model -
    # run `python manage.py migrate Website zero` 
    # zero for no migrations otherwise put which migration
    #  `python manage.py migrate Website 0001_initial`

    #`python manage.py createsuperuser` name: admin psswd: admin (Whatever you want super user to be)