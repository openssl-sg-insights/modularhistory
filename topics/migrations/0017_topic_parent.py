# Generated by Django 3.0.1 on 2020-01-04 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0016_auto_20200103_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='topics.Topic'),
        ),
    ]
