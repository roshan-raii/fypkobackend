from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    USER_TYPES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    USERNAME_FIELD = 'email'
    otp = models.CharField(max_length=6,null=True);
    is_accepted = models.BooleanField(null=True,default=False);
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True,upload_to='uploads/img/')
    
    objects = UserManager()
    # def save(self,*args,**kwargs):
    #     super(BaseUser,self).save(*args,**kwargs)
    def __str__(self):
        return self.email + f" {self.id}"