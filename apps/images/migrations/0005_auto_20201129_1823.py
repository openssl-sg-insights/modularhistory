# Generated by Django 3.1.3 on 2020-11-29 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20201129_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='hidden',
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text='Hide this item from search results.',
            ),
        ),
        migrations.AlterField(
            model_name='video',
            name='hidden',
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text='Hide this item from search results.',
            ),
        ),
    ]
