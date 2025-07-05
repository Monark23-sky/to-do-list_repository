from django.db import models
from django.contrib.auth.models import *

# Create your models here.
    
class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password, **extra_fields):
        if not user_name:
            raise ValueError('The user_name field must be set')
        # user_name = self.normalize_user_name(user_name)
        user = self.model(user_name=user_name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Must have is_superuser=True')
        
        return self.create_user(user_name, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin): 
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=50,unique=True,null=True,blank=True)
    user_name = models.CharField(max_length=50,unique=True)
    country_code = models.CharField(max_length=5,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True, blank=True)
    roles = [
        ('USER','USER'),
        ('ADMIN','ADMIN')
    ]
    role = models.CharField(max_length=50,choices=roles,default='USER',null=True,blank=True)
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = []    

    objects = CustomUserManager()   

    def __str__(self):
        return self.user_name


class Task(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    option = [
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Due','Due')
    ]
    status = models.CharField(max_length=20,choices=option,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.title

            