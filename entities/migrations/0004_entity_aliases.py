# Generated by Django 3.0.1 on 2019-12-29 15:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0003_auto_20191228_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='aliases',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
    ]
