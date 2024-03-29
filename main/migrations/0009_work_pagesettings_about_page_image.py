# Generated by Django 4.2.2 on 2023-06-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_experiece_description_pagesettings_experience_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, max_length=255, null=True, upload_to='')),
                ('company', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('from_year', models.CharField(max_length=4)),
                ('to_year', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pagesettings',
            name='about_page_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]
