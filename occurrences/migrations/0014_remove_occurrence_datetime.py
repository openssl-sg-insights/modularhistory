# Generated by Django 3.0.1 on 2020-01-02 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0013_auto_20200102_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence',
            name='datetime',
        ),
    ]
