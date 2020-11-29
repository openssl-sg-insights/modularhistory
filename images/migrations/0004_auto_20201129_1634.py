# Generated by Django 3.1.3 on 2020-11-29 16:34

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20201129_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, null=True, populate_from='get_slug', unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, null=True, populate_from='get_slug', unique=True, verbose_name='slug'),
        ),
    ]
