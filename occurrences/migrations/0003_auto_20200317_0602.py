# Generated by Django 3.0.4 on 2020-03-17 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0002_auto_20200313_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrencesourcereference',
            name='occurrence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citations', to='occurrences.Occurrence'),
        ),
    ]
