# Generated by Django 5.0.6 on 2024-05-20 10:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_rating_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='qr_code',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='qr_code/'),
            preserve_default=False,
        ),
    ]
