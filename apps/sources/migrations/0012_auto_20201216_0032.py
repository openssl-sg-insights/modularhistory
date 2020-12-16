# Generated by Django 3.1.4 on 2020-12-16 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0011_auto_20201206_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sources.publication',),
        ),
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.CharField(choices=[('sources.journal', 'journal'), ('sources.magazine', 'magazine'), ('sources.newspaper', 'newspaper'), ('sources.website', 'website')], db_index=True, max_length=255),
        ),
    ]
