# Generated by Django 5.0.6 on 2024-05-16 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_customer_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_rating', to='main.customer'),
        ),
    ]
