# Generated by Django 5.0.4 on 2024-05-14 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='UserLib',
        ),
    ]
