# Generated by Django 3.2.8 on 2021-10-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='u_user_profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
