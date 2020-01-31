# Generated by Django 3.0.1 on 2020-01-29 16:18

from django.db import migrations, models
import django.db.models.deletion
import functools
import history.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0074_auto_20200129_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(history.fields._update_filename, *(), **{'path': 'sources/'})),
        ),
        migrations.CreateModel(
            name='PublicationVolume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('date', history.fields.HistoricDateTimeField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='sources/')),
                ('publication', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sources.Publication')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('date', history.fields.HistoricDateTimeField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='sources/')),
                ('publication', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sources.Publication')),
                ('volume', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sources.PublicationVolume')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='publication_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sources.PublicationNumber'),
        ),
        migrations.AddField(
            model_name='article',
            name='publication_volume',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sources.PublicationVolume'),
        ),
    ]
