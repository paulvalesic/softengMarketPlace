# Generated by Django 5.1.5 on 2025-01-28 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_item_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]
