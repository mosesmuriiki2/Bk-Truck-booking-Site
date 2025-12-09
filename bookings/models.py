from django.db import models
from django.conf import settings
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)

    truck = models.ForeignKey('trucks.Truck', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()

    route_start = models.CharField(max_length=150)
    route_end = models.CharField(max_length=150)
    route_notes = models.TextField(blank=True)

    purpose = models.CharField(max_length=200, blank=True)

    extras = models.ManyToManyField('trucks.Extra', blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.truck.name} ({self.start_date} → {self.end_date})"

    @property
    def days(self):
        return (self.end_date - self.start_date).days + 1

    def overlaps(self, start, end):
        return not (self.end_date < start or self.start_date > end)
