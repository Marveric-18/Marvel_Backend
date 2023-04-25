from djongo import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.contrib.auth.models import User


from main_app.custom_func import validate_email, user_directory_path

"""
caption (text)
likes_count (integer)
comments_count (integer)
creation_date (datetime)
hashtags (text)
"""
# Create your models here.
class P_Posts(models.Model):
    post_id = models.CharField(max_length = 150, primary_key = True)
    user_id = models.ForeignKey("auth_app.U_User", on_delete = models.CASCADE)
    media_link = models.CharField(max_length = 500, null= True, blank = True)
    caption = models.CharField(max_length = 900, null= True, blank = True)
    likes_count = models.PositiveIntegerField(default = 0)
    comments_count = models.PositiveIntegerField(default = 0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.post_id} : \nlikes : {self.likes_count} \ncomments : {self.comments_count}"