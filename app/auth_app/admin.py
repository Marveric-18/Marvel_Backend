from django.contrib import admin

from auth_app.models import U_User, U_User_Profile, U_Config

# Register your models here.
admin.site.register(U_User)
admin.site.register(U_User_Profile)

admin.site.register(U_Config)