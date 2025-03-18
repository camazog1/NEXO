from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, user_type='final', **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, user_type='admin', **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('final', 'Final'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='final')

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"