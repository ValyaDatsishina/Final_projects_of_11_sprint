# Generated by Django 3.0.5 on 2021-06-17 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
    ]