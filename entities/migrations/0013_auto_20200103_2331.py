# Generated by Django 3.0.1 on 2020-01-03 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0012_auto_20200103_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='entityimage',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='entitytopicrelation',
            name='verified',
        ),
    ]
