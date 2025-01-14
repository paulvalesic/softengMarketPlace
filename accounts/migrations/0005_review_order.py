# Generated by Django 5.1.5 on 2025-01-28 01:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_order_rating_order_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_review', to='accounts.order'),
            preserve_default=False,
        ),
    ]
