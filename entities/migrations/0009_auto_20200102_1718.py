# Generated by Django 3.0.1 on 2020-01-02 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0008_organization_parent_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='founding',
        ),
        migrations.RemoveField(
            model_name='person',
            name='death',
        ),
    ]
