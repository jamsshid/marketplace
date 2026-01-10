from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

