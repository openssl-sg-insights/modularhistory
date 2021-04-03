# Generated by Django 3.1.3 on 2020-11-29 21:22

from django.db import migrations

import modularhistory.fields
import modularhistory.fields.historic_datetime_field
import modularhistory.fields.html_field


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0008_auto_20201129_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='date',
            field=modularhistory.fields.historic_datetime_field.HistoricDateTimeField(
                blank=True, null=True, verbose_name='Date'
            ),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='description',
            field=modularhistory.fields.HTMLField(
                default='...',
                paragraphed=True,
                processor=modularhistory.fields.html_field.process,
                verbose_name='Description',
            ),
            preserve_default=False,
        ),
    ]
