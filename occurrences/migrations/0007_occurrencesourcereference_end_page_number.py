# Generated by Django 3.0.1 on 2019-12-31 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0006_auto_20191229_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrencesourcereference',
            name='end_page_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
