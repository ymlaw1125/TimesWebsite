# Generated by Django 5.0.4 on 2024-08-26 21:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='community',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='text',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]