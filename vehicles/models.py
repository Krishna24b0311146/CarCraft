from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20, blank=True)
    kilometers = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    seller_name = models.CharField(
        max_length=100,
        default="CarCraft Seller"
    )

    seller_phone = models.CharField(
        max_length=15,
        default="9999999999"
    )

    def __str__(self):
        return self.name


class ServiceBooking(models.Model):
    SERVICE_TYPES = [
        ('general', 'General Service'),
        ('oil', 'Oil and Filter Change'),
        ('repair', 'Repair'),
        ('inspection', 'Vehicle Inspection'),
        ('other', 'Other'),
    ]
    STATUSES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    car_model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer_name} - {self.car_model} ({self.preferred_date})'