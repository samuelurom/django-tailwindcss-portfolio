# Generated by Django 4.2.2 on 2023-06-09 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='featured_image_path',
            new_name='featured_image',
        ),
    ]
