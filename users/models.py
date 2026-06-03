from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.username