# Generated by Django 5.0.7 on 2024-07-22 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_country_city_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='api.city'),
        ),
    ]
