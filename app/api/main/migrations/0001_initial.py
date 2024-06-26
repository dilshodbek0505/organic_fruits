# Generated by Django 5.0.6 on 2024-05-14 20:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(help_text="Sotuvchining to'liq ismi", max_length=255)),
                ('username', models.CharField(help_text='Sotuvchining foydalanuvchi nomi', max_length=50)),
                ('description', models.TextField(blank=True, help_text="Qo'shimcha ma'lumot", null=True)),
                ('image', models.ImageField(help_text='Foydalanuvchining rasmi', upload_to='customer/images/')),
                ('phone_number', models.CharField(help_text='Telfon raqam', max_length=13, validators=[django.core.validators.RegexValidator(message="Telefon raqamingizni to'g'ri ko'rinishda kiriting, masalan, +998991112233.", regex='^\\+998\\d{2}\\d{3}\\d{2}\\d{2}$')])),
                ('phone_number_2', models.CharField(blank=True, help_text='Telfon raqam', max_length=13, null=True, validators=[django.core.validators.RegexValidator(message="Telefon raqamingizni to'g'ri ko'rinishda kiriting, masalan, +998991112233.", regex='^\\+998\\d{2}\\d{3}\\d{2}\\d{2}$')])),
                ('instagram', models.CharField(blank=True, max_length=255, null=True)),
                ('telegram', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('tiktok', models.CharField(blank=True, max_length=255, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Commend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255)),
                ('text', models.TextField(validators=[django.core.validators.MinLengthValidator(20)])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_commend', to='main.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Telefon raqamingizni to'g'ri ko'rinishda kiriting, masalan, +998991112233.", regex='^\\+998\\d{2}\\d{3}\\d{2}\\d{2}$')])),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_rating', to='main.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
