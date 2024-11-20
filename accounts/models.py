from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class AdminManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username, 
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, first_name, last_name, password, **extra_fields)

class Admin(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = AdminManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'