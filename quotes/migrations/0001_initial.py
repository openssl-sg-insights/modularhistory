# Generated by Django 3.0.1 on 2019-12-28 21:12

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', tinymce.models.HTMLField()),
                ('slug', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('context', tinymce.models.HTMLField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.Quote')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes_quotetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuoteSourceReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(blank=True, default=1, verbose_name='reference position')),
                ('page_number', models.CharField(blank=True, max_length=15, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_references', to='quotes.Quote')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
