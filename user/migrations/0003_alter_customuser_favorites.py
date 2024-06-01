# Generated by Django 5.0.4 on 2024-05-31 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazines', '0002_magazine_last_updated_alter_magazine_upload_time'),
        ('user', '0002_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='favorites',
            field=models.ManyToManyField(related_name='saved_users', to='magazines.magazine'),
        ),
    ]
