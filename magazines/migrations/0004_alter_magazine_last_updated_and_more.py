# Generated by Django 5.0.4 on 2024-05-31 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazines', '0003_alter_magazine_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazine',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='magazine',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
