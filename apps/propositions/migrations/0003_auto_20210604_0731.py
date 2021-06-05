# Generated by Django 3.1.12 on 2021-06-04 07:21

import django.db.models.deletion
from django.db import migrations, models

import apps.sources.models.model_with_sources
import core.fields.m2m_foreign_key


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        ('sources', '0001_initial'),
        ('propositions', '0002_auto_20210604_0731'),
        ('images', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='sources',
            field=apps.sources.models.model_with_sources.SourcesField(
                blank=True,
                related_name='propositions',
                through='propositions.Citation',
                to='sources.Source',
                verbose_name='sources',
            ),
        ),
        migrations.AddField(
            model_name='proposition',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                related_name='proposition_set',
                to='topics.Topic',
                verbose_name='tags',
            ),
        ),
        migrations.AddField(
            model_name='location',
            name='content_object',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='location_relations',
                to='propositions.proposition',
                verbose_name='proposition',
            ),
        ),
        migrations.AddField(
            model_name='location',
            name='location',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='propositions_location_set',
                to='places.place',
            ),
        ),
        migrations.AddField(
            model_name='imagerelation',
            name='content_object',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='image_relations',
                to='propositions.proposition',
                verbose_name='proposition',
            ),
        ),
        migrations.AddField(
            model_name='imagerelation',
            name='image',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='_propositions_imagerelation_set',
                to='images.image',
            ),
        ),
        migrations.AddField(
            model_name='citation',
            name='content_object',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='citations',
                to='propositions.proposition',
                verbose_name='proposition',
            ),
        ),
        migrations.AddField(
            model_name='citation',
            name='source',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='propositions_citation_set',
                to='sources.source',
            ),
        ),
        migrations.AddField(
            model_name='argumentsupport',
            name='argument',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='_supports',
                to='propositions.argument',
            ),
        ),
        migrations.AddField(
            model_name='argumentsupport',
            name='premise',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='_argument_supports',
                to='propositions.proposition',
            ),
        ),
        migrations.AddField(
            model_name='argument',
            name='conclusion',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='arguments',
                to='propositions.proposition',
                verbose_name='conclusion',
            ),
        ),
        migrations.AddField(
            model_name='argument',
            name='premises',
            field=models.ManyToManyField(
                related_name='supported_arguments',
                through='propositions.ArgumentSupport',
                to='propositions.Proposition',
                verbose_name='premises',
            ),
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.proposition',),
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[],
            options={
                'ordering': ['date'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.proposition',),
        ),
        migrations.AddConstraint(
            model_name='citation',
            constraint=models.UniqueConstraint(
                fields=('source', 'content_object', 'position'),
                name='propositions_citation_unique_positions',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='argumentsupport',
            unique_together={('argument', 'premise')},
        ),
        migrations.CreateModel(
            name='Birth',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.occurrence',),
        ),
        migrations.CreateModel(
            name='Death',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.occurrence',),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.occurrence',),
        ),
        migrations.CreateModel(
            name='Speech',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.occurrence',),
        ),
    ]
