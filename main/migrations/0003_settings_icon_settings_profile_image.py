# Generated by Django 4.2.2 on 2023-06-14 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_settings_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='icon',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='settings',
            name='profile_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]