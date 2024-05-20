from django.db import models
from django.core.validators import (
    RegexValidator, MaxValueValidator, 
    MinValueValidator, MinLengthValidator)
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files.base import File


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
    qr_code = models.ImageField(upload_to='qr_code/')
    
    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://10.50.9.161:3000/{self.username}/")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img)
        fname = f'qr_code-{self.username}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

class Rating(CustomModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_rating')
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],

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

    