# Generated by Django 3.0.1 on 2020-01-29 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0028_auto_20200124_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrencesourcereference',
            name='source_type',
        ),
    ]
