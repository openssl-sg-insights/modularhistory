# Generated by Django 3.0.1 on 2020-01-03 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0020_auto_20200103_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='occurrenceentityinvolvement',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='occurrenceimage',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='occurrencelocation',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='occurrencequoterelation',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='occurrencesourcereference',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='year',
            name='verified',
        ),
    ]
