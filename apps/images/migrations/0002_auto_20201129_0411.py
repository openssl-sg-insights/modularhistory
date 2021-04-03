# Generated by Django 3.1.3 on 2020-11-29 04:11

from django.db import migrations, models

import modularhistory.fields.historic_datetime_field


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='date',
            field=modularhistory.fields.historic_datetime_field.HistoricDateTimeField(
                blank=True, null=True, verbose_name='date'
            ),
        ),
        migrations.AlterField(
            model_name='image',
            name='date_is_circa',
            field=models.BooleanField(
                blank=True, default=False, verbose_name='date is circa'
            ),
        ),
        migrations.AlterField(
            model_name='video',
            name='date',
            field=modularhistory.fields.historic_datetime_field.HistoricDateTimeField(
                blank=True, null=True, verbose_name='date'
            ),
        ),
        migrations.AlterField(
            model_name='video',
            name='date_is_circa',
            field=models.BooleanField(
                blank=True, default=False, verbose_name='date is circa'
            ),
        ),
    ]
