from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class AdminManager(BaseUserManager):
    def create_user(self, username, email, firstname, lastname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        if not firstname:
            raise ValueError('First name is required')
        if not lastname:
            raise ValueError('Last name is required')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username, 
            email=email,
            firstname=firstname,
            lastname=lastname,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, firstname, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, firstname, lastname, password, **extra_fields)

class Admin(AbstractUser):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=150, null=False)
    lastname = models.CharField(max_length=150, null=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    objects = AdminManager()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'