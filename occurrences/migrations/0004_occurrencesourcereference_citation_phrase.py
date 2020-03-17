# Generated by Django 3.0.4 on 2020-03-17 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0003_auto_20200317_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrencesourcereference',
            name='citation_phrase',
            field=models.CharField(blank=True, choices=[(None, ''), ('quoted in', 'quoted in'), ('cited in', 'cited in')], default=None, max_length=10, null=True),
        ),
    ]
