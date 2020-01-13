# Generated by Django 3.0.1 on 2020-01-02 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0021_auto_20200101_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('aliases', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MagazineArticle',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sources.Source')),
                ('number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('magazine_name', models.CharField(blank=True, max_length=100, null=True)),
                ('magazine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='magazine_articles', to='sources.Magazine')),
            ],
            options={
                'abstract': False,
            },
            bases=('sources.source',),
        ),
    ]
