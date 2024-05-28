# market/models.py
from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MarketData(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    vendor_details = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

class HistoricalMarketData(models.Model):
    market_data = models.ForeignKey(MarketData, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.market_data.product_name} - {self.date}"

class Alert(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    market_data = models.ForeignKey(MarketData, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.user.username} on {self.market_data.product_name}"




