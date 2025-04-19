from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_host = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Property(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
