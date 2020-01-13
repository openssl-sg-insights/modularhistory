# Generated by Django 3.0.1 on 2019-12-28 21:12

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('occurrences', '0001_initial'),
        ('entities', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('places', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('creators', models.CharField(blank=True, max_length=100, null=True)),
                ('editors', models.CharField(blank=True, max_length=100, null=True)),
                ('sponsor', models.CharField(blank=True, max_length=40, null=True)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('text', tinymce.models.HTMLField(blank=True, null=True, unique=True)),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='sources/')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sources.Source')),
                ('journal', models.CharField(blank=True, max_length=100, null=True)),
                ('volume_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('number', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('sources.source',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sources.Source')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('sources.source',),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sources.Source')),
                ('venue', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('sources.source',),
        ),
        migrations.CreateModel(
            name='SourceTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sources.Source')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources_sourcetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourceAttribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(blank=True, default=1)),
                ('attributee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='source_attributions', to='entities.Entity')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sources.Source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='source',
            name='attributees',
            field=models.ManyToManyField(through='sources.SourceAttribution', to='entities.Entity'),
        ),
        migrations.AddField(
            model_name='source',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='publications', to='places.Place'),
        ),
        migrations.AddField(
            model_name='source',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_sources.source_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='source',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='sources.SourceTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='source',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='publications', to='occurrences.Year'),
        ),
        migrations.AlterUniqueTogether(
            name='source',
            unique_together={('text', 'date')},
        ),
    ]
