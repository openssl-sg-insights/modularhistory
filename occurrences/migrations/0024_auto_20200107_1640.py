# Generated by Django 3.0.1 on 2020-01-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0023_auto_20200107_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='type',
            field=models.CharField(choices=[('publication', 'Publication'), ('delivery', 'Delivery'), ('writing', 'Writing'), ('interview', 'Interview'), ('birth', 'Birth'), ('death', 'Death'), ('founding', 'Founding'), ('battle', 'Battle'), ('other', 'Other')], default='other', max_length=12),
        ),
    ]
