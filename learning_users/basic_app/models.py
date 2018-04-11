from django.db import models
from django.contrib.auth.models import User
# Check this website it will gives the fields in the model User
# https://docs.djangoproject.com/en/2.0/ref/contrib/auth/
# Create your models here.

class UserProfileInfo(models.Model):

    #Inherits from the User model that is in django.contrib.auth.models
    user = models.OneToOneField(User)

    #additional fields
    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
