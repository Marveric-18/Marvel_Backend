from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('activity/', include('user_activity.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
