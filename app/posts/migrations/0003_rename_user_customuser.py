# Generated by Django 4.2.4 on 2023-08-03 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_user_password'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
    ]
