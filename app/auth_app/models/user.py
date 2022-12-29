from enum import unique
from djongo import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver



from main_app.custom_func import validate_email, user_directory_path


# Create your models here.
class U_User(AbstractUser):
    user_id = models.AutoField(primary_key= True)
    email = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    two_way_auth = models.BooleanField(default=False)
    recovery_email = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class U_User_Profile(models.Model):
    id = models.AutoField(primary_key= True)
    user = models.ForeignKey(U_User, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.CharField(max_length=100, unique=True, validators= [validate_email])
    profile_img = models.FileField(upload_to="user_directory_path",null=True, blank=True)
    first_name = models.CharField(max_length=25, default="Firstname")
    last_name = models.CharField(max_length=25, default="Lastname")
    username = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    bio = models.CharField(max_length=250, null=True, blank=True)
    weblink = models.CharField(max_length=100, null=True, blank=True)
    is_social = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "U_User_Profile"

# def post_save_create_user(sender, instance, **kwargs):