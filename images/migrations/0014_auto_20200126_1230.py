# Generated by Django 3.0.1 on 2020-01-26 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0013_remove_image_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='datetime',
            new_name='date',
        ),
    ]
