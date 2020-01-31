# Generated by Django 3.0.1 on 2020-01-29 20:20

from django.db import migrations, models
import functools
import history.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0079_source_source_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='source_file',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(history.fields._update_filename, *(), **{'path': 'sources/'})),
        ),
    ]
