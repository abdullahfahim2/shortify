from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone

import random
import string

# custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return f"{self.id}-{self.email}-{self.first_name}"