from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model that extends Django's AbstractUser.

    Attributes:
        profile_photo (ImageField): Profile photo of the user, stored in 'profile_photos/' directory.
        first_name (CharField): First name of the user.
        last_name (CharField): Last name of the user.
    """

    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username
