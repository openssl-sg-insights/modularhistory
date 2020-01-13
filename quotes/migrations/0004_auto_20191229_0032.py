# Generated by Django 3.0.1 on 2019-12-29 00:32

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('quotes', '0003_auto_20191228_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='quotes.QuoteTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
