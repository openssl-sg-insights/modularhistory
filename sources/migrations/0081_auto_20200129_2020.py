# Generated by Django 3.0.1 on 2020-01-29 20:20

from django.db import migrations
import functools
import history.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0080_auto_20200129_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='source_file',
            field=history.fields.SourceFileField(blank=True, null=True, upload_to=functools.partial(history.fields._update_filename, *(), **{'path': 'sources/'})),
        ),
    ]
