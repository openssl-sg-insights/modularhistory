# Generated by Django 3.0.1 on 2020-01-03 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0011_auto_20200103_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entityimage',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entitytopicrelation',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
