# Generated by Django 3.0.4 on 2020-03-18 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sources', '0006_sourcefactderivation_citation_phrase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('position', models.PositiveSmallIntegerField(blank=True, default=1, verbose_name='reference position')),
                ('page_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_page_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('citation_phrase', models.CharField(blank=True, choices=[(None, ''), ('quoted in', 'quoted in'), ('cited in', 'cited in')], default=None, max_length=10, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citation_set', to='sources.Source')),
            ],
            options={
                'verbose_name': 'citation',
                'ordering': ['source', 'page_number'],
                'unique_together': {('source', 'content_type', 'object_id', 'page_number', 'end_page_number', 'position')},
            },
        ),
    ]
