# Generated by Django 3.0.1 on 2019-12-29 17:21

from django.db import migrations, models
import history.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0004_entity_aliases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='aliases',
            field=history.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
    ]
