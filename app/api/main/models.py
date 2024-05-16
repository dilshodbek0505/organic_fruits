from django.db import models
from django.core.validators import (
    RegexValidator, MaxValueValidator, 
    MinValueValidator, MinLengthValidator)


phone_regex = RegexValidator(
    regex=r'^\+998\d{2}\d{3}\d{2}\d{2}$',
    message="Telefon raqamingizni to'g'ri ko'rinishda kiriting, masalan, +998991112233.",
)

class CustomModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(CustomModel):
    full_name = models.CharField(
        max_length=255,
        help_text="Sotuvchining to'liq ismi",
    )
    username = models.CharField(
        max_length=50,
        help_text="Sotuvchining foydalanuvchi nomi",
        unique=True
    )
    description = models.TextField(null=True, blank=True, help_text="Qo'shimcha ma'lumot")
    image = models.ImageField(upload_to='customer/images/',help_text="Foydalanuvchining rasmi")
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],
        help_text="Telfon raqam"
    )
    phone_number_2 = models.CharField(
        max_length=13,
        validators=[phone_regex],
        blank=True,
        null=True,
        help_text="Telfon raqam"

    )
    instagram = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.full_name

class Rating(CustomModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_rating')
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex]
    )
    number = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    def __str__(self) -> str:
        return f"{self.customer.full_name} {self.number}"


class Commend(CustomModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_commend')
    full_name = models.CharField(max_length=255)
    text = models.TextField(
        validators=[MinLengthValidator(20)]
    )

    def __str__(self) -> str:
        return self.full_name

    