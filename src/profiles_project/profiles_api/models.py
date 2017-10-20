# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ValidationError
# Create your models here.

def validate_student_email(value):
    if "@" in value:
        return value
else:
    raise ValidationError("Not a Valid Email.")

class UserProfileManager(BaseUserManager):
    """
    Helps Django work with our custom user model.
    """
    def create_user(self, email, name, password=None):
        """
        Creates a new user profile objects.
        """
        if not email:
            raise ValueError("Users must have an email address.")

        #Normalize the Email Address
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, name, password):
        """
        Create and save new super user with given details.
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    This class is for storing user_profile informations and
    it represents "user_profile".
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a users full name"""

        return self.name

    def get_short_name(self):
        """Used to get a user short name"""

        return self.name

    def __str__(self):
        """Django  uses this when it needs to convert the objects to a string"""

        return self.email


class ProfileFeedItem(models.Model):
    """
    Profile status update.
    """
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string."""

        return self.status_text

class StudentDetails(models.Model):
    """
    Details of students.
    """
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=125, blank=True, null=True)
    #just to check the custom validation.
    email = models.CharField(max_length=125, blank=True, null=True, validators=[validate_student_email])
    age = models.IntegerField(blank=True, null=True)

    #just to check the overridding
    def save(self, *args, **kwargs):
        self.age=18
        super(StudentDetails, self).save(*args, **kwargs)

#signals
def student_details_pre_save_receiver():
    pass

def student_details_post_save_receiver():
    pass
