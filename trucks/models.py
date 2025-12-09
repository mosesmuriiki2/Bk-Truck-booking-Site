from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Q

class Driver(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    license_number = models.CharField(max_length=60, blank=True)
    active = models.BooleanField(default=True)
    # new fields
    profile_picture = models.ImageField(upload_to='drivers/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

class Truck(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    license_plate = models.CharField(max_length=30, blank=True)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="Comma-separated features, e.g. sound, screens")
    image_url = models.URLField(blank=True)
    # new uploaded image field
    image = models.ImageField(upload_to='trucks/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trucks:detail', args=[self.slug])

    def is_available_for(self, start_date, end_date):
        return not self.bookings.filter(
            status__in=['reserved', 'approved'],
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()

class Extra(models.Model):
    CATEGORY_CHOICES = [
        ('sound', 'Sound System'),
        ('screens', 'LED Screens'),
        ('dancers', 'Dance Team'),
        ('crew', 'Support Crew'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
