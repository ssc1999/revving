
from django.db import models

class Invoice(models.Model):
    invoice_number = models.IntegerField()
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    haircut_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=10)
    revenue_source = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    expected_duration = models.IntegerField()
    created_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['invoice_number', 'customer']

class Total(models.Model):
    revenue_source = models.CharField(max_length=255, unique=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expected_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.revenue_source