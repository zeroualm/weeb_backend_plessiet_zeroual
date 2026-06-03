from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
 
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(("L'adresse email doit être renseignée."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save()
        return user
 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
 
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Le SuperUtilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Le SuperUtilisateur doit avoir is_superuser=True.'))
 
        return self.create_user(email, password, **extra_fields)
 
class CustomUser(AbstractUser):
 
    username = None
    email = models.EmailField(('adresse email'), unique=True, blank=False)
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
 
    def __str__(self):
        return self.email