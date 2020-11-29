# Generated by Django 3.1.3 on 2020-11-29 06:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0003_auto_20201129_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='key'),
        ),
    ]
